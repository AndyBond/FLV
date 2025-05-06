import re
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from tqdm import tqdm
import polars as pl


#    processes обычно быстрее на CPU-нагруженных задачах (например, разбор с регулярками).
#    threads может быть быстрее на I/O-нагруженных задачах.

# Предкомпилированное регулярное выражение
pattern = re.compile(r'<[^>]*>|"[^"]*"|\S+')

def parse_line(line: str) -> list[str]:
    return [
        field if field.startswith('<') and field.endswith('>') else field.strip('"')
        for field in pattern.findall(line)
    ]

def load_lines(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.lstrip().startswith('#')]

def parallel_parse(lines: list[str], executor_cls, max_workers: int) -> list[list[str]]:
    parsed_rows = []
    with executor_cls(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_line, line) for line in lines]
        for future in tqdm(as_completed(futures), total=len(futures), desc=executor_cls.__name__):
            parsed_rows.append(future.result())
    return parsed_rows

def run_benchmark(filename: str, max_workers: int = 8):
    lines = load_lines(filename)
    print(f'Загружено строк: {len(lines)}')

    results = []

    for mode, executor_cls in [("threads", ThreadPoolExecutor), ("processes", ProcessPoolExecutor)]:
        start = time.time()
        parsed_rows = parallel_parse(lines, executor_cls, max_workers)
        elapsed = time.time() - start

        #max_len = max(len(row) for row in parsed_rows)
        #normalized = [row + [''] * (max_len - len(row)) for row in parsed_rows]
        #df = pl.DataFrame(parsed_rows, schema=[f'col_{i+1}' for i in range(max_len)])
        df = pl.DataFrame(parsed_rows)
        print("загрузили df")
        results.append((mode, elapsed, df.shape))
        print("заполнили results")

    print("\nСравнение производительности:")
    print(f"{'Режим':<10} | {'Время (сек)':<12} | {'Размер DataFrame'}")
    print("-" * 40)
    for mode, time_sec, shape in results:
        print(f"{mode:<10} | {time_sec:<12.3f} | {shape}")

# Запуск
if __name__ == '__main__':
    run_benchmark("C:\\Projects\\FLV\\input\\proxy_s.log", max_workers=8)


    """
Чтобы сконвертировать первую колонку с UNIX timestamp в datetime прямо во время импорта в polars, ты можешь просто применить преобразование pl.col("col_1").cast(pl.Datetime("us")) сразу после создания DataFrame.

Вот как внести это изменение в функцию run_benchmark, в момент, где создаётся DataFrame:
df = pl.DataFrame(normalized, schema=[f'col_{i+1}' for i in range(max_len)])
поменять на:
columns = [f'col_{i+1}' for i in range(max_len)]
df = pl.DataFrame(normalized, schema=columns)

# Преобразуем первую колонку (UNIX timestamp) в datetime
df = df.with_columns(
    pl.col("col_1").cast(pl.Float64).cast(pl.Datetime("us"))
)

Объяснение:

    col_1 сначала приводим к Float64, потому что UNIX timestamp в секундах может быть дробным (1745874053.097).
    Затем cast(..., pl.Datetime("us")) конвертирует в datetime с микросекундной точностью.

------
Вот финальная вставка, которая преобразует col_1 в datetime и переименовывает её в timestamp:
заменить:
columns = [f'col_{i+1}' for i in range(max_len)]
df = pl.DataFrame(normalized, schema=columns)

# Преобразуем первую колонку (UNIX timestamp) в datetime
df = df.with_columns(
    pl.col("col_1").cast(pl.Float64).cast(pl.Datetime("us"))
)
на:
columns = [f'col_{i+1}' for i in range(max_len)]
df = pl.DataFrame(normalized, schema=columns)

# Преобразуем и переименовываем первую колонку в datetime
df = df.with_columns(
    pl.col("col_1").cast(pl.Float64).cast(pl.Datetime("us")).alias("timestamp")
).drop("col_1")

Теперь колонка col_1:

    будет преобразована в datetime,
    переименована в timestamp,
    удалена в исходной форме, чтобы не дублировалась.



    """
    