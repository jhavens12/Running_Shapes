#v4 - created for Pythonista github
import time
import datetime
from datetime import date
import get_time
import pprint
import calendar


#
def activity_count(dictionary):
    #counts amount of keys in dictionary
    amount = len(dictionary.keys())
    amount_str = str(amount)
    return amount_str
#

#New:

def full_running_totals(dictionary1,days,unit):
    #creadted for use with master_dict
    #newest and working
    #limit days after this calculation for range
    #Creates running totals for each day - not just activity day
    calculation_range_time = []
    final_list = []
    dictionary = dictionary1.copy()
    x = days
    #time functions
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day, hour=0, minute=0, second=0)
    end_of_today = datetime.datetime(now.year, now.month, now.day, hour=23, minute=59, second=59)

    difference = start_of_today - get_time.forever() #fix start peroid

    calculation_range = list(range(0,(difference.days +1))) #creates list from past date(given) to current date
    calculation_range_rev = list(reversed(calculation_range))
    calculation_range_time = [end_of_today - datetime.timedelta(days=x) for x in range(0,(difference.days +1))]

    for i,f in zip(calculation_range_time,calculation_range): #for every calculation day ex 1,2,3,4,5 back
        dictionary_1 = dictionary.copy() #create a new dictionary
        oldest_time = end_of_today - (datetime.timedelta(days=(x+f)))
        for key in list(dictionary_1):
            if key > i:
                del dictionary_1[key] #delete keys newer than calculation day
        for key in list(dictionary_1):
            if key < oldest_time: #delete keys older than oldest time
                 del dictionary_1[key]
        value_list = []
        for key in dictionary_1:
            value_list.append(float(dictionary_1[key][unit])) #adds variables to list
        list_sum = sum(value_list)
        final_list.append(list_sum)
    new_date_list = []
    for i in calculation_range: #create list of days going backwards from today
        new_day = get_time.day(i)
        new_date_list.append(new_day)
    new_dict = dict(zip(new_date_list, final_list))
    return new_dict

def monthly_daily_totals(dictionary,time_input,unit_input):
    #for use with masterdict (get_data.my_filtered_activities())
    #01.29.18
    #takes in number for how many months ago. Ex 0 is current, 1 is last month
    x_list = []
    y_list = []

    #filters out only dates needed
    for key in list(dictionary):
        if key < get_time.FOM(time_input): #if older than first of month
            del dictionary[key]
    for key in list(dictionary):
       if key > get_time.LOM(time_input): #if newer than first of month
           del dictionary[key]

    calculation_day_count = (get_time.LOM(time_input) - get_time.FOM(time_input)).days #how many days in the month
    calculation_day_range = list(range(1,calculation_day_count+2)) #range of 1 to the days in the month - calculation days

    mile_count = 0
    mile_count_list = [] #list of miles
    day_count_list = [] #list of days miles occurred
    for day in calculation_day_range:  #ex 1-31
        for activity in dictionary:
            if activity.day == day: #if the day of the activity matches the day in the list
                mile_count = mile_count + float(dictionary[activity][unit_input])
                mile_count_list.append(mile_count) #add mile count
                day_count_list.append(activity.day) #add day that count occurs

    return dict(zip(day_count_list,mile_count_list))

# also new

def monthly_stats(dictionary):
    #used to return dictionary of stats for each month - key is just a string
    #currently only distance_miles is being used
    #can certainly be expanded upon in the future
    count_dict = {}
    for date in dictionary:
        count_dict[str(date.year)+"-"+str(date.month)] = [] #create dict of lists
        #count_dict[datetime.datetime(date.year,date.month,1)] = [] #use datetime as key

    for date in dictionary:
        count_dict[str(date.year)+"-"+str(date.month)].append(float(dictionary[date]['distance_miles'])) #creates list of distance_miles
        #count_dict[datetime.datetime(date.year,date.month,1)].append(dictionary[date]['distance_miles']) #use datetime as key

    final_dict = {}
    for month in count_dict:
        final_dict[month] = {}
        final_dict[month]['run_count'] = len(count_dict[month])
        final_dict[month]['miles_ran'] = sum(count_dict[month])
        month_name = month.split('-')
        final_dict[month]['year'] = str(month_name[0])
        final_dict[month]['month'] = str(month_name[1])
        final_dict[month]['date_human'] = str(calendar.month_name[int(month_name[1])]+" "+month_name[0])

    return final_dict

def weekly_stats(dictionary):
    #Monday is first day of week
    #This is done poorly and needs to be rewritten
    count_dict = {} #create keys (weeks)
    weekly_runs = {} #dictionary to hold the actual runs
    for date in dictionary:
        week_number = date.isocalendar()[1]
        count_dict[str(date.year)+"-"+str(week_number)] = [] #create list
        weekly_runs[str(date.year)+"-"+str(week_number)] = {} #create dict
    for date in dictionary:
        week_number = date.isocalendar()[1]
        count_dict[str(date.year)+"-"+str(week_number)].append(float(dictionary[date]['distance_miles'])) #list of distances for each week
        weekly_runs[str(date.year)+"-"+str(week_number)][date] = dictionary[date]

    final_dict = {}
    for week in count_dict:

        final_dict[week] = {}
        final_dict[week]['run_dict'] = weekly_runs[week] #add the actual runs to the final dictionary
        final_dict[week]['run_count'] = len(count_dict[week])
        final_dict[week]['miles_ran'] = sum(count_dict[week])
        week_name = week.split('-')
        final_dict[week]['year'] = str(week_name[0])
        final_dict[week]['week'] = str(week_name[1])
        week_datetime = datetime.datetime.strptime(week + '-1', "%Y-%W-%w")
        final_dict[week]['date_human'] = str(week_datetime.year)+"-"+str(week_datetime.month)+"-"+str(week_datetime.day)

    return final_dict

#### MOved from running_graphs

def yearly_totals(dictionary,years_ago):
    #0 = this year
    #1 = last year
    #returns days of year as keys (1-365)
    now = datetime.datetime.now()
    start_of_year = datetime.datetime((now.year - years_ago), 1, 1)
    end_of_year = datetime.datetime((now.year - years_ago), 12, 31)

    for key in list(dictionary):
        if key < start_of_year: #if older than first of month
            del dictionary[key]
    for key in list(dictionary):
       if key > end_of_year: #if newer than first of month
           del dictionary[key]

    calculation_day_count = (end_of_year - start_of_year).days #how many days in the month
    calculation_day_range = list(range(1,calculation_day_count+2)) #range of 1 to the days in the month - calculation days

    mile_count = 0
    mile_count_list = [] #list of miles
    day_count_list = [] #list of days miles occurred
    for day in calculation_day_range:  #ex 1-31
        for activity in dictionary:
            if activity.timetuple().tm_yday == day: #if the day of the activity matches the day in the list
                mile_count = mile_count + float(dictionary[activity]['distance_miles'])
                mile_count_list.append(mile_count) #add mile count
                day_count_list.append(activity.timetuple().tm_yday) #add day that count occurs

    return dict(zip(day_count_list,mile_count_list))
