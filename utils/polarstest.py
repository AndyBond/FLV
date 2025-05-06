import polars as pl
from time import time
from datetime import datetime
from datetime import timedelta

def make_date(strdate, strtime):
    """
    Функция берет текстовые поля дата и время из лога и делает из них одно поле формата "дата", добавляя 3 часа
    """
    newdate = datetime.strptime(strdate + " " + strtime, '%Y-%m-%d %H:%M:%S')
    newdate = newdate + timedelta(hours=3)
    return(newdate)

print(pl.__version__)
names = ["date", "time", "s_sitename", "s_computername", "s_ip", "cs_method", "cs_uri_stem", "cs_uri_query", "s_port", "cs_username", "c_ip", "cs_version", "cs_User_Agent",
        "cs_Referer", "cs_host", "sc_status", "sc_substatus", "sc_win32_status", "sc_bytes", "cs_bytes", "time_taken", "X_Forwarded_For"]
start = time()
df2 = pl.read_csv("F:\\SampleLogs\\*.log", comment_prefix="#",has_header=False, separator=" ", encoding="utf8", new_columns=names).with_columns(fulldate = pl.concat_str(pl.col("date"), pl.col("time")).str.strptime(pl.Datetime, '%Y-%m-%d %H:%M:%S').dt.offset_by("3h"))
print(df2)
end = time() - start
print("Загрузка: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))

start1 = time()
df3 = pl.sql(
"""
SELECT * FROM df2 WHERE cs_username LIKE '%bond0226%'
"""
).collect()
print(df3)
end = time() - start1
print("Запрос: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
start2 = time()
df3.write_csv("out.csv", separator=",")
end = time() - start2
print("сохранение: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
