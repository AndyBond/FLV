import re
import polars as pl
from time import time

# Предкомпилированное регулярное выражение
pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line: str) -> list[str]:
    return [
        field if field.startswith('<') and field.endswith('>') else field.strip('"')
        for field in pattern.findall(line)
    ]

def process_full_file(filename: str) -> pl.DataFrame:
    # Шаг 1: читаем файл целиком как список строк
    lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.startswith("#"):
                parsed = line.strip()
                lines.append(parsed)
    print("Считали строки")
    # Шаг 2: создаем сырое представление в DataFrame
    raw_df = pl.DataFrame({'raw': lines})
    print("Загружен Frame")

    # Шаг 3: разбиваем каждую строку с помощью list comprehension
    parsed_rows = [parse_line(row) for row in raw_df['raw']]
    print("распарсили данные")
    # Шаг 4: определяем максимальное количество полей
    #max_len = max(len(row) for row in parsed_rows)
    max_len = 18
    # Шаг 5: выравниваем строки
    #normalized = [row + [''] * (max_len - len(row)) for row in parsed_rows]
    columns = [f'col_{i+1}' for i in range(max_len)]

    # Шаг 6: создаем итоговый DataFrame
    parsed_df = pl.DataFrame(parsed_rows, schema=columns)
    return parsed_df

# Пример запуска
start = time()
df = process_full_file("C:\\Projects\\FLV\\input\\proxy.log")
end = time() - start
print("Парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
print(df.head())
print(f'Размерность: {df.shape}')
# Парсинг: 00:01:58.74
# lazy