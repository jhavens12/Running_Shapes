#v2.0
import time
import datetime
import calendar
from datetime import date
from dateutil.relativedelta import relativedelta, MO, SU
##

def now():
    return datetime.datetime.now()

def forever():
    return datetime.datetime(year=1900, month=1, day=1)

def FOM(x):
    #first of month
    #start of day
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month - x, 1)

def LOM(x):
    #last of month
    #end of day
    now = datetime.datetime.now()
    past = datetime.datetime(now.year, now.month - (x-1), 1) - (datetime.timedelta(days=1))
    return datetime.datetime(past.year, past.month, past.day, hour=23, minute=59, second=59)

def FOY():
    #first of year
    #start of day
    now = datetime.datetime.now()
    return datetime.datetime(now.year, 1, 1)

def PFOY():
    #first of last year
    #start of day
    now = datetime.datetime.now()
    return datetime.datetime((now.year-1), 1, 1)

def LM(x):
    #last monday
    #start of day
    now = datetime.datetime.now()
    date = datetime.datetime(now.year, now.month, now.day)
    return date - datetime.timedelta(weeks=x, days=now.weekday())

def LS(x):
    #last sunday
    #end of day
    now = datetime.datetime.now()
    date = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)
    return date - datetime.timedelta(weeks=x, days=now.weekday()+1,)

def LS_S(x):
    #last sunday
    #start of day
    now = datetime.datetime.now()
    date = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    return date - datetime.timedelta(weeks=x, days=now.weekday()+1,)

def running_week(x):
    #running week start
    #down to hour
    now = datetime.datetime.now()
    return now - datetime.timedelta(weeks=x, days=+7)

def running_thirty(x):
    #30 days ago start
    #down to hour
    now = datetime.datetime.now()
    return now - datetime.timedelta(weeks=(4*x), days=+30)

def day(x):
    #x days ago
    #down to hour
    now = datetime.datetime.now()
    return now - datetime.timedelta(days=x)

def weekday(x):
    return calendar.day_name[x.weekday()]

def what_month(x): #takes 1-12 as input, not datetime
    return calendar.month_name[x]

def difference_days(time1,time2):
    if time1 > time2:
        newer_time = time1
        older_time = time2
    if time2 > time1:
        older_time = time1
        newer_time = time2
    delta = newer_time - older_time
    return delta.days

def difference_minutes(time1,time2):
    if time1 > time2:
        newer_time = time1
        older_time = time2
    if time2 > time1:
        older_time = time1
        newer_time = time2
    delta = newer_time - older_time
    return delta

def convert_weekday_full(i):
    return str(calendar.day_name[i.weekday()])+" "+str(calendar.month_name[i.month])+" "+str(i.day)

def convert_month_name(i):
    return str(calendar.month_name[i.month])

def convert_year_name(i):
    return str(i.year)
