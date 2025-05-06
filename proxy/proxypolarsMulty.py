import re
import polars as pl
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time

# Предкомпилированное регулярное выражение
pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line: str) -> list[str]:
    return [
        field if field.startswith('<') and field.endswith('>') else field.strip('"')
        for field in pattern.findall(line)
    ]

def process_full_file(filename: str, max_workers: int = 8) -> pl.DataFrame:
    # Шаг 1: читаем все строки, пропуская строки, начинающиеся с #
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f'Обрабатываем строк: {len(lines)}')

    # Шаг 2: многопоточный разбор строк
    parsed_rows = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_line, line) for line in lines]
        for future in as_completed(futures):
            parsed_rows.append(future.result())
    print("разобрали поля")
    # Шаг 3: определяем максимальное количество полей
    max_len = max(len(row) for row in parsed_rows)
    print("определили макс длину")
    # Шаг 4: выравниваем все строки
    normalized = [row + [''] * (max_len - len(row)) for row in parsed_rows]
    columns = [f'col_{i+1}' for i in range(max_len)]
    print("выровняли. начали заполнять df")
    # Шаг 5: создаём итоговый DataFrame
    parsed_df = pl.DataFrame(normalized, schema=columns)
    return parsed_df

# Пример запуска
start = time()
df = process_full_file("C:\\Projects\\FLV\\input\\proxy.log", max_workers=8)
print(df.head())
print(f'Размерность: {df.shape}')
end = time() - start
print("Парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))