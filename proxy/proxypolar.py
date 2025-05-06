import re
import polars as pl

def parse_line(line):
    pattern = r'<[^>]*>|"[^"]*"|\S+'
    matches = re.findall(pattern, line)
    cleaned = []
    for field in matches:
        if field.startswith('<') and field.endswith('>'):
            cleaned.append(field)
        else:
            cleaned.append(field.strip('"'))
    return cleaned

def process_file_to_polars(filename):
    rows = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith("#"):
                parsed = parse_line(line.strip())
                rows.append(parsed)

    # Найдём максимальное количество полей среди всех строк
    max_len = max(len(row) for row in rows)

    # Заполним недостающие элементы пустыми строками
   # normalized_rows = [row + [''] * (max_len - len(row)) for row in rows]

    # Создаём имена столбцов: col_1, col_2, ...
    columns = [f'col_{i+1}' for i in range(max_len)]

    # Создаём Polars DataFrame
    df = pl.DataFrame(rows, schema=columns)
    return df

# Пример использования
df = process_file_to_polars("F:\\Documents\\python\\FLV\\input\\proxy.csv")
print(df)