import datetime

from src.schedule_parser import list_to_timed_item, time_format, read_delta_maybe_spaces 
from src.schedule_exceptions import BadChangeTypeException, NoSuchItemNameException


class FilePersistence:
    def __init__(self, input_filename, output_filename):
        self.output_filename = output_filename
        with open(input_filename, 'r') as f:
            all_lines = f.readlines()
        self.all_lists = FilePersistence.fill_in_all_lists(all_lines)
        
    def fill_in_all_lists(all_lines):
        output = []
        for line in all_lines:
            my_list = line.split(",")[:-1]
            if not FilePersistence.is_trivial(my_list):
                output.append(my_list)
        return output
    
    def is_trivial(my_list):
        return my_list[0] == ""
        
    def list_timed_items(self):
        output = []
        for my_list in self.all_lists:
            timed_item = list_to_timed_item(my_list)
            output.append(timed_item)
        return output
        
    def number(date_input):
        return date_input.total_seconds()/60
            
    def snooze_default(self, idx, input_time):
        my_item = self.all_lists[idx]
        my_item[4] = datetime.datetime.strftime(input_time + datetime.timedelta(hours=1), time_format)
        self.all_lists[idx] = my_item
        
    def snooze_amount(self, idx, input_time):
        my_item = self.all_lists[idx]
        my_item[4] = datetime.datetime.strftime(input_time + read_delta_maybe_spaces(my_item[5]), time_format)
        
    def persist_done(self, splitsies, input_time):
        self.write_all_lists()
        
    def persist_snooze(self, splitsies, input_time):
        self.write_all_lists()
        
    def persist_overwhelm(self, splitsies, item_overwhelm):
        self.write_all_lists()
        
    def time_to_string(date):
        return datetime.datetime.strftime(date, time_format)
        
    def write_all_lists(self):
        with open(self.output_filename, 'w') as f:
            for my_list in self.all_lists:
                f.write(",".join(my_list))
                f.write("\n")
                
    def get_input_time():
        return datetime.datetime.now()
        
    def get_user_input(my_input=None):
        while my_input not in ["1", "2"]:
            my_input = input("Enter 1 to mark as done, enter 2 to snooze\n")
        return FilePersistence.parse_user_input(my_input)
        
    def parse_user_input(my_input):
        my_input_dict = {'1': "DONE", '2': "SNOOZE"}
        return my_input_dict[my_input]
        
    def get_item_overwhelm(my_input=None):
        while my_input not in [str(n) for n in list(range(1, 6))]:
            my_input = input("Rate how overwhelming this item is from 1-5\n")
        return my_input