import re
import polars as pl
from time import time

log_file_path = "C:\\Projects\\FLV\\input\\proxy_s.log"
pattern2 = r'([\d.]+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) (<[^>]*>) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+) ("[^"]*"|\S+)'

start = time()
delim = chr(1) # фейковый разделитель
raw_df = pl.read_csv(log_file_path,  comment_prefix="#",has_header=False, separator=delim, encoding="utf8")
print(raw_df)
end = time() - start
print("заполнили lazy: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
start2 = time()
#    pl.col('column_1').str.extract(pattern2, 1).add('0'*9).str.replace(r'\.(\d{3}).*', '${1}').cast(pl.Int64).alias('datetime'),
#    pl.col('column_1').str.extract(pattern2, 1).str.replace(r'\.', '').cast(pl.Int64).cast(pl.Datetime("ms")).alias('datetime'),
df = raw_df.with_columns([
    pl.col('column_1').str.extract(pattern2, 1).cast(pl.Float64).alias("c1"),
    pl.col('column_1').str.extract(pattern2, 2).alias("c2"),
    pl.col('column_1').str.extract(pattern2, 3).alias("c3"),
    pl.col('column_1').str.extract(pattern2, 4).alias("c4"),
    pl.col('column_1').str.extract(pattern2, 5).alias("c5"),
    pl.col('column_1').str.extract(pattern2, 6).alias("c6"),
    pl.col('column_1').str.extract(pattern2, 7).alias("c7"),
    pl.col('column_1').str.extract(pattern2, 8).alias("c8"),
    pl.col('column_1').str.extract(pattern2, 9).alias("c9"),
    pl.col('column_1').str.extract(pattern2, 10).alias("c10"),
    pl.col('column_1').str.extract(pattern2, 11).alias("c11"),
    pl.col('column_1').str.extract(pattern2, 12).alias("c12"),
    pl.col('column_1').str.extract(pattern2, 13).alias("c13"),
    pl.col('column_1').str.extract(pattern2, 14).alias("c14"),
    pl.col('column_1').str.extract(pattern2, 15).alias("c15"),
    pl.col('column_1').str.extract(pattern2, 16).alias("c16"),
    pl.col('column_1').str.extract(pattern2, 17).alias("c17"),
    pl.col('column_1').str.extract(pattern2, 18).alias("c18")
]).with_columns(pl.from_epoch("c1", time_unit="s").dt.offset_by("3h"))
#]).with_columns(pl.from_epoch("c1", time_unit="ms"))
#]).drop('column_1')
print(df)
end = time() - start2
print("заполнение дф: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))
end = time() - start
print("всего: {:02.0f}:{:02.0f}:{:02.2f}".format(end // 3600, end % 3600 // 60, end % 60))