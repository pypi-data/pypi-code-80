import os
os.chdir('C:\Backup\Python\File')

class AthleteListSBh(list):
    def __init__(self, a_Name, a_Dob, a_Times=[]):
        list.__init__([])
        self.Name  = a_Name
        self.Dob   = a_Dob
        self.extend(a_Times)
    def top3(self):
        return(sorted(set([sanitize(t) for t in self]))[0:3])

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return(time_string)

    (mins,second) = time_string.split(splitter)
    return(mins + '.' + second)

def get_coach_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        temp = data.strip().split(',')
        return(AthleteListSBh(temp.pop(0),temp.pop(0),temp))
    except IOError as Err1:
        print('File IOError occurred:' + str(Err1))

james = get_coach_data('james.txt')
julie = get_coach_data('julie.txt')
mikey = get_coach_data('mikey.txt')
sarah = get_coach_data('sarah.txt')

veera = AthleteListSBh('veera','2019-01-09')
veera.append('1.31')
veera.extend(['1:01','1-03','3.45'])

print(james.Name, "'s fastest timings are:" + str(james.top3()))
print(julie.Name, "'s fastest timings are:" + str(julie.top3()))
print(mikey.Name, "'s fastest timings are:" + str(mikey.top3()))
print(sarah.Name, "'s fastest timings are:" + str(sarah.top3()))
print(veera.Name, "'s fastest timings are:" + str(veera.top3()))
