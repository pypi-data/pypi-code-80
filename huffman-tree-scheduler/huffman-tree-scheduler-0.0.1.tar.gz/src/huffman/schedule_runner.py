import sys
import datetime

from src.scheduler import Scheduler
from src.timed_schedule_config import TimedScheduleConfig
from src.file_persistence import FilePersistence

config_file = sys.argv[1]
persistence_file = sys.argv[2]
        
my_persistence = FilePersistence(config_file, persistence_file)

my_input = ""
while my_input not in [str(n) for n in range(1, 6)]:
    my_input = input("How overwhelmed are you from 1-5?\n")
        
timed_config = TimedScheduleConfig(my_persistence, int(my_input))

my_schedule = Scheduler(timed_config)

my_item, do_feedback = my_schedule.pick_item(datetime.datetime.now())

print(my_item)

if do_feedback:
    timed_config.get_feedback(my_item)




