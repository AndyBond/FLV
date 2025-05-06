import re
import polars as pl

pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line):
    matches = pattern.findall(line)
    return [field if field.startswith('<') and field.endswith('>') else field.strip('"') for field in matches]

def process_file_in_chunks(filename, batch_size=100_000):
    rows = []
    max_len = 0
    part = 0

    with open(filename, 'r', encoding='utf-8') as file:
        for lineno, line in enumerate(file, 1):
            parsed = parse_line(line.strip())
            rows.append(parsed)
            max_len = max(max_len, len(parsed))

            if lineno % batch_size == 0:
                df = normalize_and_create_df(rows, max_len)
                df.write_parquet(f'output_part_{part}.parquet')
                print(f'Сохранена часть {part}, строк: {len(df)}')
                part += 1
                rows = []

        # Обработка оставшихся строк
        if rows:
            df = normalize_and_create_df(rows, max_len)
            df.write_parquet(f'output_part_{part}.parquet')
            print(f'Сохранена последняя часть {part}, строк: {len(df)}')

def normalize_and_create_df(rows, max_len):
    # Выравниваем строки по длине
    for i in range(len(rows)):
        if len(rows[i]) < max_len:
            rows[i].extend([''] * (max_len - len(rows[i])))
    columns = [f'col_{i+1}' for i in range(max_len)]
    return pl.DataFrame(rows, schema=columns)

# Запуск
process_file_in_chunks('your_file.csv', batch_size=100_000)