from datetime import datetime, timedelta
import copy

from src.timed_item import TimedItem


time_format = "%d %m %y %H %M"
SECONDS_IN_DAY = 60*60*24
SECONDS_IN_HOUR = 60*60

def list_to_timed_item(my_first_list):
    my_list = copy.deepcopy(my_first_list)
    my_list = read_all_times(my_list)

    return TimedItem(my_list)
    
def read_all_times(my_list):
    my_list[1] = read_delta_maybe_spaces(my_list[1])
    my_list[2] = read_delta_maybe_spaces(my_list[2])
    if my_list[3] != '':
        my_list[3] = read_time(my_list[3])
    if my_list[4] != '':
        my_list[4] = read_time(my_list[4])
    return my_list
    
def read_time(input_string):
    return datetime.strptime(input_string, time_format)
    
def write_time(input_time):
    return datetime.strftime(input_time, time_format)
    
def read_delta_maybe_spaces(input_string):
    input_string = input_string.strip()
    output = read_delta(input_string)
    return output
    
def read_delta(input_string):
    split_by_spaces = input_string.split(" ")
    if only_hours_minutes(split_by_spaces):
        output = read_delta_hours_minutes(input_string)
    elif only_days(split_by_spaces):
        output = timedelta(days=int(split_by_spaces[0]))
    else:
        output = timedelta(days=int(split_by_spaces[0]))
        output += read_delta_hours_minutes(split_by_spaces[1])
    return output

def only_hours_minutes(string_list):
    return len(string_list) == 1 and ":" in string_list[0]
    
def only_days(string_list):
    return len(string_list) == 1 and ":" not in string_list[0]

   
def read_delta_hours_minutes(input_string):
    split_by_colon = input_string.split(":")
    return timedelta(hours=int(split_by_colon[0]), minutes=int(split_by_colon[1]))
    
def write_delta(my_delta):
    all_seconds = my_delta.total_seconds()
    output, all_seconds = get_days(all_seconds)
    output, all_seconds = get_hours(output, all_seconds)
    output, all_seconds = get_minutes(output, all_seconds)
    return output
    
def get_days(all_seconds):
    if all_seconds > SECONDS_IN_DAY:
        output = str(int(all_seconds/SECONDS_IN_DAY))
        all_seconds = all_seconds % SECONDS_IN_DAY
    else:
        output = ''
    return output, all_seconds

def get_hours(output, all_seconds):
    if all_seconds > SECONDS_IN_HOUR:
        output += str(int(all_seconds/SECONDS_IN_HOUR)) + ":"
        all_seconds = all_seconds % SECONDS_IN_HOUR
    else:
        output += "00:"
    return output, all_seconds

def get_minutes(output, all_seconds):
    if all_seconds > 60:
        output += str(int(all_seconds/60))
    else:
        output += "00"
    return output, all_seconds
        