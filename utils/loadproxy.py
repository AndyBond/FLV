import polars as pl
import re
from time import time
from datetime import datetime
from datetime import timedelta

LogFile = "C:\\Temp\\accesslogs\\aclog.M42.@20250429T000059.s"
df = pl.read_csv(LogFile, comment_prefix="#",has_header=False, separator=" ", encoding="utf8", eol_char='\n', truncate_ragged_lines=True)
with pl.Config(tbl_cols=-1):
    print(df)
