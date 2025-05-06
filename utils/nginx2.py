import polars as pl
import re
from datetime import datetime
import pyarrow as pa
from typing import List, Dict, Any

def parse_nginx_log(log_file_path: str) -> pl.DataFrame:
    # Чтение всего файла сразу, а не построчно
    with open(log_file_path, 'r') as file:
        log_lines = file.readlines()
    
    # Регулярное выражение для парсинга логов nginx
    pattern = r'(?P<ip>[\d.]+) - - \[(?P<datetime>[\w:/]+\s[+\-]\d{4})\] "(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    
    # Создаем списки для каждого столбца
    ips: List[str] = []
    datetimes: List[datetime] = []
    requests: List[str] = []
    statuses: List[int] = []
    bytes_vals: List[int] = []
    referers: List[str] = []
    user_agents: List[str] = []
    
    # Компилируем регулярное выражение один раз
    regex = re.compile(pattern)
    
    # Обрабатываем каждую строку
    for line in log_lines:
        match = regex.match(line.strip())
        if match:
            group = match.groupdict()
            ips.append(group['ip'])
            
            # Оптимизируем парсинг даты
            dt_str = group['datetime']
            dt_obj = datetime.strptime(dt_str, '%d/%b/%Y:%H:%M:%S %z')
            datetimes.append(dt_obj)
            
            requests.append(group['request'])
            statuses.append(int(group['status']))
            bytes_vals.append(int(group['bytes']))
            referers.append(group['referer'])
            user_agents.append(group['user_agent'])
    
    # Создаем DataFrame напрямую из собранных данных
    df = pl.DataFrame({
        'ip': ips,
        'datetime': datetimes,
        'request': requests,
        'status': statuses,
        'bytes': bytes_vals,
        'referer': referers,
        'user_agent': user_agents
    })
    
    return df

def parse_nginx_log_fast(log_file_path: str) -> pl.DataFrame:
    """Альтернативный метод с использованием сканирования Polars"""
    # Чтение файла целиком
    with open(log_file_path, 'r') as file:
        content = file.read()
    
    # Создаем DataFrame из одной колонки со строками логов
    raw_df = pl.DataFrame({'raw_log': content.strip().split('\n')})
    
    # Используем polars для извлечения данных с помощью регулярных выражений
    pattern = r'([\d.]+) - - \[([\w:/]+ [+\-]\d{4})\] "([^"]*)" (\d+) (\d+) "([^"]*)" "([^"]*)"'
    
    df = raw_df.with_columns([
        pl.col('raw_log').str.extract(pattern, 1).alias('ip'),
        pl.col('raw_log').str.extract(pattern, 2).alias('datetime_str'),
        pl.col('raw_log').str.extract(pattern, 3).alias('request'),
        pl.col('raw_log').str.extract(pattern, 4).cast(pl.Int32).alias('status'),
        pl.col('raw_log').str.extract(pattern, 5).cast(pl.Int64).alias('bytes'),
        pl.col('raw_log').str.extract(pattern, 6).alias('referer'),
        pl.col('raw_log').str.extract(pattern, 7).alias('user_agent')
    ]).drop('raw_log')
    
    # Преобразуем строку даты в формат datetime
    df = df.with_columns([
        pl.col('datetime_str').str.strptime(pl.Datetime, '%d/%b/%Y:%H:%M:%S %z').alias('datetime')
    ]).drop('datetime_str')
    
    return df

def main():
    #log_file_path = input("Введите путь к лог-файлу nginx: ")
    log_file_path = "C:\\Projects\\FLV\\input\\access3.log"
    try:
        # Используем быструю версию парсера
        df = parse_nginx_log_fast(log_file_path)
        print(f"Лог успешно загружен. Форма данных: {df.shape}")
        print(df.head())
        
        # Пример дополнительной оптимизации при сохранении
        # df.write_parquet("nginx_logs.parquet", compression="zstd", compression_level=3)
        
    except Exception as e:
        print(f"Произошла ошибка при обработке лог-файла: {e}")

if __name__ == "__main__":
    main()