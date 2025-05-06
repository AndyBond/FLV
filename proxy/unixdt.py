import polars
from datetime import datetime
ts = '1745960459.523'
print(datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S'))


