import re
import polars as pl
import glob
import os

pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line):
    matches = pattern.findall(line)
    return [field if field.startswith('<') and field.endswith('>') else field.strip('"') for field in matches]

def process_file_in_chunks(filename, batch_size=100_000, output_prefix='output_part'):
    rows = []
    max_len = 0
    part = 0
    part_files = []

    with open(filename, 'r', encoding='utf-8') as file:
        for lineno, line in enumerate(file, 1):
            parsed = parse_line(line.strip())
            rows.append(parsed)
            max_len = max(max_len, len(parsed))

            if lineno % batch_size == 0:
                out_file = f'{output_prefix}_{part}.parquet'
                df = normalize_and_create_df(rows, max_len)
                df.write_parquet(out_file)
                part_files.append(out_file)
                print(f'Сохранена часть {part}, строк: {len(df)}')
                part += 1
                rows = []

        # Остаток
        if rows:
            out_file = f'{output_prefix}_{part}.parquet'
            df = normalize_and_create_df(rows, max_len)
            df.write_parquet(out_file)
            part_files.append(out_file)
            print(f'Сохранена последняя часть {part}, строк: {len(df)}')

    # Объединение всех частей
    final_df = pl.concat([pl.read_parquet(f) for f in part_files])
    final_df.write_parquet('combined_output.parquet')
    print(f'Финальный файл сохранён: combined_output.parquet')

    # (Необязательно) удалить промежуточные файлы
    for f in part_files:
        os.remove(f)

def normalize_and_create_df(rows, max_len):
    for i in range(len(rows)):
        if len(rows[i]) < max_len:
            rows[i].extend([''] * (max_len - len(rows[i])))
    columns = [f'col_{i+1}' for i in range(max_len)]
    return pl.DataFrame(rows, schema=columns)

# Запуск
process_file_in_chunks('your_file.csv', batch_size=100_000)