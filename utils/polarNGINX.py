import polars as pl
import re
from time import time
from datetime import datetime
from datetime import timedelta
"""
Здесь парсится лог битрикса. Для конкретного применения - смотреть формат конкретных логов. Может быть очень разный.
Также, разным бывает поле даты. Например:
[10/Feb/2025:09:55:56 +0300]
Или вот - первое тире это просто тире, второе может быть на месте числа - времени ответа апстрима
[10/Feb/2025:09:55:56 +0300 - 0.060]
[10/Feb/2025:09:55:59 +0300 - -]
Если импортировать лог как CSV, в первом случае дата разделится на два поля, во втором и третьем - на три. Нужно это учитывать
Тестов загрузки в sqlite нет, там медленнее на два порядка, отброшено. polars подд
"""


def import_NGINX_Log(LogFile):
    # Просто импортирует лог как файл CSV с пробелами в качестве разделителей. Поле даты разрывается на 2 части
    names = ["ip", "x", "username", "datetime", "timeshift", "status", "request", "bytes", "referer", "user_agent", "forwarder_for"]
    # Это читерский формат даты. Так поларс захватывает CSV с пробелом в поле даты.
    # вторую часть даты выбрасываем и прибавляем 3 часа "+ timedelta(hours=3)" (московское время), если нужно (!!! нужно смотреть, в каком формате время в журнале, это может бьть уже UTC+3 )  
    DateFormat = "[%d/%b/%Y:%H:%M:%S"
    df = pl.read_csv(LogFile, comment_prefix="#",has_header=False, separator=" ", encoding="utf8", new_columns=names).with_columns(fulldate=pl.col("datetime").str.strptime(pl.Datetime, DateFormat)).drop('datetime').drop('timeshift').drop('x')
    #Закоментирована строка, в которой оставлены ненужные поля и остатки попиленной даты
    #df = pl.read_csv(LogFile, comment_prefix="#",has_header=False, separator=" ", encoding="utf8", new_columns=names).with_columns(fulldate=pl.col("datetime").str.strptime(pl.Datetime, DateFormat))
    return df

def parse_nginx_log(log_file_path):
    # Построчно считываем лог, парсим регекспом, загоняем в список и из него уже в датафрейм полара
    # Регулярное выражение для парсинга логов nginx
    # Пример строки лога:
    # 192.168.1.1 - - [21/Oct/2023:13:55:36 +0200] "GET /path/file.html HTTP/1.1" 200 2326 "http://referer.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    #pattern = r'(?P<ip>[\d.]+) - - \[(?P<datetime>[\w:/]+\s[+\-]\d{4})\] "(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    #pattern = r'(?P<ip>[\d.]+) - - \[(?P<datetime>[\w:/]+\s[+\-]\d{4})\] "(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    # строка изменена. В конкретном логе битрикса другой порядок полей и нужно экранировать "/"
    pattern = r'(?P<ip>[\d.]+) - - \[(?P<datetime>[\w:\/]+\s[+\-]\d{4})\] (?P<status>\d+) "(?P<request>[^"]*)" (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)" "(?P<forwarder_for>[^"]*)"'
    # Чтение файла и извлечение данных с помощью регулярного выражения
    data = {
        'ip': [],
        'datetime': [],
        'status': [],
        'request': [],
        'bytes': [],
        'referer': [],
        'user_agent': [],
        'forwarder_for':[]
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
                data['status'].append(int(group['status']))
                data['request'].append(group['request'])
                data['bytes'].append(int(group['bytes']))
                data['referer'].append(group['referer'])
                data['user_agent'].append(group['user_agent'])
                data['forwarder_for'].append(group['forwarder_for'])

    
    # Создание Polars DataFrame
    df = pl.DataFrame({
        'ip': data['ip'],
        'datetime': data['datetime'],
        'status': data['status'],
        'request': data['request'],
        'bytes': data['bytes'],
        'referer': data['referer'],
        'user_agent': data['user_agent'],
        'forwarder_for': data['forwarder_for'],
    })
    
    return df


def parse_nginx_log_fast(log_file_path: str) -> pl.DataFrame:
    # Альтернативный метод с использованием сканирования Polars
    # Читаем файл построчно в датафрейм полара, затем проходим по этому датафрейму парсим скомпилированным регексом и заполняем новый датафрейм. старый удаляем
    # Чтение файла целиком
    with open(log_file_path, 'r') as file:
        content = file.read()
    
    # Создаем DataFrame из одной колонки со строками логов
    raw_df = pl.DataFrame({'raw_log': content.strip().split('\n')})
    # Используем polars для извлечения данных с помощью регулярных выражений
    pattern = r'([\d.]+) - - \[([\w:\/]+ [+\-]\d{4})\] (\d+) "([^"]*)" (\d+) "([^"]*)" "([^"]*)" "([^"]*)"'
    
    df = raw_df.with_columns([
        pl.col('raw_log').str.extract(pattern, 1).alias('ip'),
        pl.col('raw_log').str.extract(pattern, 2).alias('datetime_str'),
        pl.col('raw_log').str.extract(pattern, 3).cast(pl.Int32).alias('status'),
        pl.col('raw_log').str.extract(pattern, 4).alias('request'),
        pl.col('raw_log').str.extract(pattern, 5).cast(pl.Int64).alias('bytes'),
        pl.col('raw_log').str.extract(pattern, 6).alias('referer'),
        pl.col('raw_log').str.extract(pattern, 7).alias('user_agent'),
        pl.col('raw_log').str.extract(pattern, 8).alias('forwarder_for')
    ]).drop('raw_log')
    # Преобразуем строку даты в формат datetime
    df = df.with_columns([
        pl.col('datetime_str').str.strptime(pl.Datetime, '%d/%b/%Y:%H:%M:%S %z').alias('datetime')
    ]).drop('datetime_str')
    
    return df

def main():
    # если какая-то ветка try вылетит по исключению, переменные останутся инициализированными
    end1 = 0
    end2 = 0
    end3 = 0
    log_file_path = "C:\\Projects\\FLV\\input\\access3.log"
    print(pl.__version__)

    try:
        start = time()
        df = import_NGINX_Log(log_file_path)
        end3 = time() - start
        print(f"Лог успешно загружен. Форма данных: {df.shape}")
        with pl.Config(tbl_cols=-1):
            print(df)
    except Exception as e:
        print(f"Произошла ошибка при обработке лог-файла: {e}")

    try:
        start = time()
        df = parse_nginx_log_fast(log_file_path)
        end1 = time() - start
        print(f"Быстрый парсинг успешно загружен. Форма данных: {df.shape}")
        with pl.Config(tbl_cols=-1):
            print(df)
    except Exception as e:
        print(f"Произошла ошибка при обработке быстрого парсинга: {e}")
    
    try:
        start = time()
        df = parse_nginx_log(log_file_path)
        end2 = time() - start
        print(f"Парсинг успешно загружен. Форма данных: {df.shape}")
        with pl.Config(tbl_cols=-1):
            print(df)
    except Exception as e:
        print(f"Произошла ошибка при обработке парсинга: {e}")

    print("Быстрый парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end1 // 3600, end1 % 3600 // 60, end1 % 60))
    print("Обычный парсинг: {:02.0f}:{:02.0f}:{:02.2f}".format(end2 // 3600, end2 % 3600 // 60, end2 % 60))
    print("Импорт: {:02.0f}:{:02.0f}:{:02.2f}".format(end3 // 3600, end3 % 3600 // 60, end3 % 60))

if __name__ == "__main__":
    main()