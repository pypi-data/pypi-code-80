import csv
import datetime

from src.schedule_exceptions import BadChangeTypeException, TimeIntervalNotSpecifiedException

MAX_WEIGHT = 1000
HIGHEST_OVERWHELM = 5

DONE = "DONE"
SNOOZE = "SNOOZE"

class TimedScheduleConfig():

    def __init__(self, persistence, overwhelm=0):
        self.persistence = persistence
        TimedScheduleConfig.fix_lines(persistence)
        self.overwhelm = overwhelm
        
    def create_weighted_items(self, input_time=datetime.datetime.now()):
        weights = {}
        for item in self.list_timed_items():
            weight = self.get_weight(item, input_time)
            if weight != 0:
                weights[item.name] = self.get_weight(item, input_time)
        self.weights = weights
        
    def list_timed_items(self):
        return self.persistence.list_timed_items()
        
    def fix_lines(persistence):
        for idx, my_list in enumerate(persistence.all_lists):
            while len(my_list) < 8:
                my_list.append("")
            persistence.all_lists[idx] = my_list
            if my_list[1] == "" or my_list[2] == "":
                raise TimeIntervalNotSpecifiedException
     
    def get_weight(self, item, input_time):
        if not item.done:
            output =  MAX_WEIGHT
        else:
            output = self.get_weight_maybe_due(item, input_time)
        if item.snooze:
            if input_time < item.snooze:
                output = 0
        if not type(item.overwhelm) == str:
            if HIGHEST_OVERWHELM - self.overwhelm + 1 < item.overwhelm:
                output = 0
        return output
        
    def get_weight_maybe_due(self, item, input_time):
        due_time = item.done + item.wait_interval_start
        if input_time < due_time:
            output = 0
        else:
            slope = self.get_slope(item)
            output = slope * type(self.persistence).number((input_time - due_time))
        return output
        
    def get_slope(self, item):
        return MAX_WEIGHT/type(self.persistence).number((item.wait_interval_end - item.wait_interval_start))
        
    def find_in_list_timed_items(self, item_name):
        for idx, item in enumerate(self.list_timed_items()):
            if item.name == item_name:
                output_item = item
                output_idx = idx
        return output_idx, output_item
                
    def done(self, item_name, input_time):
        idx, item = self.find_in_list_timed_items(item_name)
        TimedScheduleConfig.set_done(idx, item, self.persistence, input_time)
        
    def set_done(idx, item, persistence, input_time):
        persistence.all_lists[idx][3] = type(persistence).time_to_string(input_time)
        persistence.persist_done(idx, input_time)
        
    def snooze(self, item_name, input_time):
        idx, item = self.find_in_list_timed_items(item_name)
        TimedScheduleConfig.set_snooze(idx, item, self.persistence, input_time)
        
    def set_snooze(idx, item, persistence, input_time):
        if item.snooze_amount and TimedScheduleConfig.not_is_string_and_space(item.snooze_amount) and item.snooze_amount != "":
            persistence.snooze_amount(idx, input_time)
        else:
            persistence.snooze_default(idx, input_time)
        persistence.persist_snooze(idx, input_time)
        
    def set_item_overwhelm(self, item_name, item_overwhelm):
        idx, item = self.find_in_list_timed_items(item_name)
        TimedScheduleConfig.set_overwhelm(idx, item, item_overwhelm, self.persistence)
        
    def set_overwhelm(idx, item, item_overwhelm, persistence):
        persistence.all_lists[idx][6] = item_overwhelm
        persistence.persist_overwhelm(idx, item_overwhelm)
    
    def not_is_string_and_space(stringie):
        output = True
        if type(stringie) == str and stringie.isspace():
            output = False
        return output
        
    def get_feedback(self, item_name, change_type=None, input_time=None, item_overwhelm=None):
        if not change_type:
            change_type = type(self.persistence).get_user_input()
        if not input_time:
            input_time = type(self.persistence).get_input_time()
        if not item_overwhelm:
            item_overwhelm = type(self.persistence).get_item_overwhelm()
        self.set_item_overwhelm(item_name, item_overwhelm)
        if change_type == DONE:
            self.done(item_name, input_time)
        elif change_type == SNOOZE:
            self.snooze(item_name, input_time)
        else:
            raise BadChangeTypeException
        