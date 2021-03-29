from src.timed_schedule_config import TimedScheduleConfig
from src.huffman_tree import Huffman

class Scheduler:
    
    def __init__(self, timed_config):
        self.config = timed_config
                
    
    def pick_item(self, input_time=0):
        self.config.create_weighted_items(input_time)
        all_the_items = list(self.config.weights.keys())
        if len(all_the_items) == 0:
            return "Nothing to do!  Wait a few minutes before trying again.", False
        if len(all_the_items) == 1:
            return all_the_items[0], True
        else:
            return self.pick_from_longer_list(input_time)
            
            
    def pick_from_longer_list(self, input_time):
        self.create_weighted_items(input_time)
        self.do_huffman()
        return self.schedule.pick_item(), True
        
    def create_weighted_items(self, input_time):
        self.config.create_weighted_items(input_time)
        
    def do_huffman(self):
        self.schedule = Huffman(self.config.weights)
        self.schedule.do_huffman()

