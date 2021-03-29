from src.schedule_exceptions import TimeIntervalNotSpecifiedException

class TimedItem():
    def __init__(self, list_item):
        self.name = list_item[0]
        self.wait_interval_start = list_item[1]
        self.wait_interval_end = list_item[2]
        self.done = list_item[3]
        self.snooze = list_item[4]
        if list_item[6] != "":
            self.overwhelm = int(list_item[6])
        else:
            self.overwhelm = list_item[6]
        self.snooze_amount = list_item[5]
        
       
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __str__(self):
        return f"{self.name}, {self.wait_interval_start}, {self.wait_interval_end}, {self.done}, {self.snooze}"
            
    def set_done(self, input_time):
        self.done = input_time
        
    def set_snooze(self, input_time, snooze_amount):
        self.snooze = input_time + snooze_amount
