import get_data
import functions as f
import get_time
import credentials
import pprint

color_dict = {"Strava Orange":"#fc4c02", "Nice Blue":"#64a7da"}

master_dict = get_data.my_filtered_activities()

def current_period(n,master_dict):
    dict_1 = master_dict.copy()
    first10 = {k: master_dict[k] for k in list(master_dict)[:n]}
    return first10

current_dict = current_period(10,master_dict)

choice_dict = {}
for n,key in enumerate(sorted(current_dict.keys())):
    n=n+1
    choice_dict[n] = key
    print(str(n)+": "+current_dict[key]['type']+" - "+current_dict[key]['weekday_short_date'])

print("-------------------")
choice = int(input("Which run to graph?"))
print()

color_choice_dict = {}
for n,color in enumerate(color_dict.keys()):
    n=n+1
    color_choice_dict[n] = key
    print(str(n)+": "+color)

print("-------------------")
color_choice = int(input("Which color?"))
print()

polyline = current_dict[choice_dict[choice]]['map']['summary_polyline']

f.run_and_graph(color_dict[color_choice_dict[color_choice]),choice_dict[choice],polyline)
#This works but the image doesn't gen correctly on IOS
#f.gen_text(choice_dict[choice],current_dict[choice_dict[choice]]) #title then dictionary
