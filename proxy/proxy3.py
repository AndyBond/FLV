import re
import polars as pl
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # pip install tqdm

pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line: str) -> list[str]:
    return [
        field if field.startswith('<') and field.endswith('>') else field.strip('"')
        for field in pattern.findall(line)
    ]

def process_full_file(filename: str, max_workers: int = None) -> pl.DataFrame:
    # Шаг 1: читаем все строки, исключая комментарии
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith('#')]

    print(f'Обрабатываем строк: {len(lines)}')

    # Шаг 2: многопроцессорная обработка с прогресс-баром
    parsed_rows = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_line, line) for line in lines]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Разбор строк"):
            parsed_rows.append(future.result())

    # Шаг 3: определяем максимальное число полей
    max_len = max(len(row) for row in parsed_rows)

    # Шаг 4: выравнивание
    normalized = [row + [''] * (max_len - len(row)) for row in parsed_rows]
    columns = [f'col_{i+1}' for i in range(max_len)]

    # Шаг 5: создание итогового DataFrame
    parsed_df = pl.DataFrame(normalized, schema=columns)
    return parsed_df

# Запуск
if __name__ == '__main__':
    df = process_full_file("F:\\Documents\\python\\FLV\\input\\proxy.csv", max_workers=8)
    print(df.head())
    print(f'Размерность: {df.shape}')