import polars as pl
import re
from datetime import datetime

def parse_nginx_log(log_file_path):
    # Регулярное выражение для парсинга логов nginx
    # Пример строки лога:
    # 192.168.1.1 - - [21/Oct/2023:13:55:36 +0200] "GET /path/file.html HTTP/1.1" 200 2326 "http://referer.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    pattern = r'(?P<ip>[\d.]+) - - \[(?P<datetime>[\w:/]+\s[+\-]\d{4})\] "(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    
    # Чтение файла и извлечение данных с помощью регулярного выражения
    data = {
        'ip': [],
        'datetime': [],
        'request': [],
        'status': [],
        'bytes': [],
        'referer': [],
        'user_agent': []
    }
    
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                group = match.groupdict()
                data['ip'].append(group['ip'])
                
                # Преобразование даты и времени
                # Формат в логах: 21/Oct/2023:13:55:36 +0200
                dt_str = group['datetime']
                dt_obj = datetime.strptime(dt_str, '%d/%b/%Y:%H:%M:%S %z')
                data['datetime'].append(dt_obj)
                
                data['request'].append(group['request'])
                data['status'].append(int(group['status']))
                data['bytes'].append(int(group['bytes']))
                data['referer'].append(group['referer'])
                data['user_agent'].append(group['user_agent'])
    
    # Создание Polars DataFrame
    df = pl.DataFrame({
        'ip': data['ip'],
        'datetime': data['datetime'],
        'request': data['request'],
        'status': data['status'],
        'bytes': data['bytes'],
        'referer': data['referer'],
        'user_agent': data['user_agent']
    })
    
    return df

def main():
    log_file_path = input("Введите путь к лог-файлу nginx: ")
    try:
        df = parse_nginx_log(log_file_path)
        print(f"Лог успешно загружен. Форма данных: {df.shape}")
        print(df.head())
        
        # Можно сохранить в другой формат, если нужно
        # df.write_parquet("nginx_logs.parquet")
        
    except Exception as e:
        print(f"Произошла ошибка при обработке лог-файла: {e}")

if __name__ == "__main__":
    main()