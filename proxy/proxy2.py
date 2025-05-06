import re
from time import time
import polars as pl
from concurrent.futures import ProcessPoolExecutor, as_completed

# Регулярное выражение — вынесено на глобальный уровень, чтобы избежать повторной компиляции
pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line: str) -> list[str]:
    return [
        field if field.startswith('<') and field.endswith('>') else field.strip('"')
        for field in pattern.findall(line)
    ]

def process_full_file(filename: str, max_workers: int = None) -> pl.DataFrame:
    # Шаг 1: читаем все строки, пропуская те, что начинаются с "#"
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith('#')]

    print(f'Обрабатываем строк: {len(lines)}')

    # Шаг 2: многопроцессорный парсинг
    parsed_rows = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_line, line) for line in lines]
        for future in as_completed(futures):
            parsed_rows.append(future.result())

    # Шаг 3: определяем максимальное количество полей
    max_len = max(len(row) for row in parsed_rows)

    # Шаг 4: выравниваем строки
    normalized = [row + [''] * (max_len - len(row)) for row in parsed_rows]
    columns = [f'col_{i+1}' for i in range(max_len)]

    # Шаг 5: создаём итоговый DataFrame
    parsed_df = pl.DataFrame(normalized, schema=columns)
    return parsed_df

# Пример запуска
if __name__ == '__main__':
    start = time()
    #df = process_full_file("C:\\Projects\\FLV\\input\\proxy_s.log", max_workers=8)
    df = process_full_file("C:\\Projects\\FLV\\input\\proxy.log", max_workers=8)
    end = time() - start
    print("Парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
    print(df.head())
    print(f'Размерность: {df.shape}')