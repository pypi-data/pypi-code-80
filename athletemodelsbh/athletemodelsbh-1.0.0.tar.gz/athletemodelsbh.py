import os
import pickle
from athletelist_sbh import AthleteListSBh

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)

    (mins,secnd) = timestrin.split(splitter)
    return(mins + '.' + second)

def get_coach_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        temp = data.strip().split(',')
        return(AthleteListSBh(temp.pop(0),temp.pop(0),temp))
    except IOError as Err1:
        print('File IOError (get_coach_data):'+ Err1)

def put_to_store(filelist):
    all_athletes = {}
    for each_file in filelist:
        athlist = get_coach_data(each_file)
        all_athletes[athlist.Name] = athlist
    try:
        with open('athlete.pickle','wb') as athpck:
            pickle.dump(all_athletes,athpck)
    except IOError as Err2:
        print('File IO Error (Put_to _store):' + str(Err2))
    return(all_athletes)

def get_from_store():
    all_athletes = {}
    try:
        with open('athlete.pickle','rb') as athpck:
            all_athletes = pickle.load(athpck)
    except IOError as Err3:
        print('File IO Error (get_from_store):' + str(Err3))
    return(all_athletes)



