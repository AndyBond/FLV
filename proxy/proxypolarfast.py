import re
import polars as pl
from time import time

# Предкомпилируем регулярное выражение один раз
pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line):
    matches = pattern.findall(line)
    return [field if (field.startswith('<') and field.endswith('>')) else field.strip('"') for field in matches]

def process_file_to_polars(filename):
    rows = []
    max_len = 0

    # Одно проходное чтение + парсинг + определение максимальной длины
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.startswith("#"):
                parsed = parse_line(line.strip())
                rows.append(parsed)
                #max_len = max(max_len, len(parsed))

    # Если есть строки разной длины — заполним недостающие поля пустыми значениями
    #for i in range(len(rows)):
    #    if len(rows[i]) < max_len:
    #        rows[i].extend([''] * (max_len - len(rows[i])))

    #columns = [f'col_{i+1}' for i in range(max_len)]
    max_len = 18
    columns = [f'col_{i+1}' for i in range(max_len)]
    print("закончили обработку строк", max_len)
    df = pl.DataFrame(rows, schema=columns)
    return df

# Быстрый запуск
start = time()
df = process_file_to_polars("C:\\Projects\\FLV\\input\\proxy.log")
end = time() - start
print("Парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
print(df)
# Парсинг: 00:01:25.81 - 01:13