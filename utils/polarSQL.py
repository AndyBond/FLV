import tkinter as tk
from tkinter import ttk, filedialog
import polars

columns_data = [
'date', 
'time',  
's_sitename', 
's_computername',  
's_ip',  
'cs_method',  
'cs_uri_stem',  
'cs_uri_query',  
's_port', 
'cs_username', 
'c_ip', 
'cs_version', 
'cs_User_Agent', 
'cs_Referer', 
'cs_host', 
'sc_status',  
'sc_substatus',  
'sc_win32-status',  
'sc_bytes',  
'cs_bytes',  
'time_taken',  
'X_Forwarded_For'
]


file_path = "C:\\Projects\\IISLogAnalyzer\\input\\u_ex250208_x.log"
SQLString = "SELECT cs_username, count(sc_status) FROM LogData WHERE sc_status = 200 GROUP BY cs_username"
SQLString2 = "SELECT cs_username, count(sc_status) FROM LogData WHERE sc_status = 200 GROUP BY cs_username LIMIT 10"

LogData = polars.read_csv(file_path, comment_prefix="#",has_header=False, separator=" ", encoding="utf8", new_columns=columns_data)
print(LogData)

ctx = polars.SQLContext(LogData=LogData, eager=True)
result = ctx.execute(SQLString)
print(result)

#ctx = polars.SQLContext(LogData=LogData, eager=True)
result = ctx.execute(SQLString2)
print(result)

#ctx = polars.SQLContext(LogData=LogData, eager=True)
result = ctx.execute(SQLString)
print(result)