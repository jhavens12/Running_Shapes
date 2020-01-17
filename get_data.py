#v3 06/08/18 - SUPPORT FOR PAGINATION
import requests
import time
import datetime
from datetime import date
import get_time
import collections
import json
import calendar
import credentials
import pprint
import renew


def my_filtered_activities(): #combines my_activities and filter functions
    #import from api key file
    try:
        with open('./api_key.txt') as f:
            api_key = f.read().splitlines()[0] #only grab first line, remove /n from string
            print(api_key)
    except Exception:
        print("No key found in file")
        api_key = "nokey"

    if "nokey" not in api_key:
        #pulling key from file
        print("Getting Data...")
        url = 'https://www.strava.com/api/v3/athlete/activities'
        header = {'Authorization': 'Bearer '+api_key}
        param = {'per_page':200, 'page':1}
        print("Page: 1")
        dataset = requests.get(url, headers=header, params=param).json()
        count = len(dataset)
        if count == 2: #if there is an error
            #this runs if there is a key found in the text file, but it is expired
            print("Old key is bad")
            api_key = renew.main()
            print("Getting Data with new key...")
            url = 'https://www.strava.com/api/v3/athlete/activities'
            header = {'Authorization': 'Bearer '+api_key}
            param = {'per_page':200, 'page':1}
            print("Page: 1")
            dataset = requests.get(url, headers=header, params=param).json()
            count = len(dataset)

    else:

        #this runs if there is no key at all and one needs to be created
        api_key = renew.main()
        print("Getting Data with new key...")
        url = 'https://www.strava.com/api/v3/athlete/activities'
        header = {'Authorization': 'Bearer '+api_key}
        param = {'per_page':200, 'page':1}
        print("Page: 1")
        dataset = requests.get(url, headers=header, params=param).json()
        count = len(dataset)
        print("COUNT:"+str(count))

    if count == 200: #if 200 results come back
        loop_count = 1 #we've already done one loop
        while count == 200: #while it keeps returning 200 results
            loop_count = loop_count + 1 #increase loop_count or page number
            print("Page: "+str(loop_count))
            param = {'per_page':200, 'page':loop_count} #reset params
            sub_dataset = requests.get(url, headers=header, params=param).json() #pull new data with sub_dataset name
            dataset = dataset + sub_dataset #combine (Json files, not dictionaries thank jesus)
            count = len(sub_dataset) #count results to see if we need to loop again
    print(str(len(dataset))+" Total Activities")
    wanted_events_dict = {event_timestamp(i): clean_event(i) for i in dataset if wanted_event(i)}
    print(str(len(wanted_events_dict))+" Wanted Activities")
    return {event_timestamp(i): clean_event(i) for i in dataset if wanted_event(i)} #return as normal

def my_activities():
    url = 'https://www.strava.com/api/v3/athlete/activities'
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    my_dataset = requests.get(url, headers=header, params=param).json()
    return my_dataset

def activities():
    url = 'https://www.strava.com/api/v3/activities/following'
    header = {'Authorization': 'Bearer '+credentials.api_key}
    param = {'per_page':200, 'page':1}
    dataset = requests.get(url, headers=header, params=param).json()
    return dataset

def wanted_event(i):
    return i['type'] == 'Run' and i['distance'] != 0.0

def event_timestamp(i):
    return convert_timestamp(i['start_date_local'])

def convert_weekday(i):
    return str(calendar.day_name[i.weekday()])+" "+str(i.day)

def convert_weekday_full(i):
    return str(calendar.day_name[i.weekday()])+" "+str(calendar.month_name[i.month])+" "+str(i.day)

def convert_weekday_short(i):
    return str(calendar.day_abbr[i.weekday()])+" "+str(calendar.month_abbr[i.month])+" "+str(i.day)

def clean_event(i):
    if not i['has_heartrate']:
        i['average_heartrate'] = i['max_heartrate'] = 0
    i['elapsed'] = convert_seconds_to_minutes(i['elapsed_time'])
    i['pace_dec'] = convert_pace(i['distance'],i['moving_time'])
    i['pace'] = convert_dec_time(convert_pace(i['distance'],i['moving_time']))
    i['distance_miles'] = convert_meters_to_miles(i['distance'])
    i['total_elevation_feet'] = convert_elevation(i['total_elevation_gain'])
    i['start_date_datetime'] = event_timestamp(i)
    i['weekday_date'] = convert_weekday(i['start_date_datetime'])
    i['weekday_full_date'] = convert_weekday_full(i['start_date_datetime'])
    i['weekday_short_date'] = convert_weekday_short(i['start_date_datetime'])
    if "Treadmill" not in i['name']:
        i['treadmill_flagged'] = "no"
    if "Treadmill" in i['name']:
        i['treadmill_flagged'] = "yes"

    return i

# def filter(dataset):
#     return {event_timestamp(i): clean_event(i) for i in dataset if wanted_event(i)}

def convert_seconds_to_minutes(i):
    return datetime.timedelta(seconds=i)

def convert_timestamp(i):
    return datetime.datetime.strptime(i, "%Y-%m-%dT%H:%M:%SZ")

def convert_pace(distance,elapsed):
    minutes = elapsed/60
    miles = distance * 0.00062137
    pace = minutes/miles
    return pace

def convert_dec_time(dec):
    #converts decimal time to readable time format
    Minutes = dec
    Seconds = 60 * (Minutes % 1)
    result = ("%d:%02d" % (Minutes, Seconds))
    return result

def convert_meters_to_miles(meters):
    return ("{0:.2f}".format(int(meters) * 0.000621371))

def convert_elevation(i):
    return float(("{0:.2f}".format(i*3.28)))
