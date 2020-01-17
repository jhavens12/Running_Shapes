import get_data
import functions as f
import get_time
import credentials


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
    print(str(n)+": "+current_dict[key]['weekday_short_date'])

choice = int(input("Which run to graph?"))

polyline = current_dict[choice_dict[choice]]['map']['summary_polyline']

f.run_and_graph(choice_dict[choice],polyline)
