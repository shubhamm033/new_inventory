import time
from datetime import datetime
from pytz import timezone

jwt_secret="qwertyuiiiimm"

TIME_ZONE =  'Asia/Kolkata'

def itime():
    india  = timezone(TIME_ZONE)
    now = datetime.now(india)
    tt = datetime.timetuple(now)
    n_time = time.mktime(tt)
    return n_time

def nicetime(ep,pattern=None):
    if not pattern:
        pattern = "%d/%m/%Y"
        # pattern = "%H:%M %d/%m/%Y"
        # pattern="%Y-%m-%d"
    return time.strftime(pattern,time.localtime(ep))

def dateToepoch(tm):
    
    return int(time.mktime(time.strptime(tm,"%d/%m/%Y")))
    