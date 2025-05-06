
from datetime import datetime
from datetime import timedelta

edate = "16.02.2025 0:00:00"
etime = "01.01.2000 23:59:52"

d1 = datetime.strptime(edate, '%d.%m.%Y %H:%M:%S')
t1 = datetime.strptime(etime, '%d.%m.%Y %H:%M:%S')
newdate = d1
newdate = newdate.replace(hour=t1.hour, minute=t1.minute, second=t1.second)
print(newdate)
newdate = newdate + timedelta(hours=3)
print(newdate)



