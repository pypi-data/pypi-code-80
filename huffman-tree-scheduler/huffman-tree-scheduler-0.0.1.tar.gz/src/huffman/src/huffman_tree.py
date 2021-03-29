import csv
import copy
import sys
import random
import math
import timeit

from src.schedule_exceptions import HangsOnSearchingLoopException 
from src.tree import Tree

class Huffman():
    def __init__(self, my_input):
        self.input_tree = Tree(my_input)
        self.output_tree = copy.deepcopy(self.input_tree)
        
    def do_huffman(self):
        output = self.output_tree.do_huffman()
        self.labelled_items = output
        
    def pick_item(self):
        random_number = random.randint(0, sys.maxsize)
        return self.get_tree_element(random_number)
        
    def initialize(the_number):
        if the_number == 0:
            output_string = "o"
        else:
            output_string = ""
        return output_string
        
    def lowest_binary_digit(the_number):
        if the_number % 2 == 1:
            output = "l"
        else:
            output = "o"
        return output
        
    def remove_lowest_binary_digit(the_number):
        return math.floor(the_number/2)
        
    def convert_next_binary_digit(output_string, remaining_to_be_converted):
        output_string = Huffman.lowest_binary_digit(remaining_to_be_converted) + output_string
        remaining_to_be_converted = Huffman.remove_lowest_binary_digit(remaining_to_be_converted)
        return output_string, remaining_to_be_converted

    def get_desired(the_number):
        remaining_to_be_converted = the_number
        output_string = Huffman.initialize(remaining_to_be_converted)
        while remaining_to_be_converted >= 1:
            output_string, remaining_to_be_converted = Huffman.convert_next_binary_digit(output_string, remaining_to_be_converted)
        return output_string
        
    def compare_low_bits(desired_end, encoding_begin, encoding_end):
        return (encoding_end == desired_end) and ("l" not in encoding_begin)
        
    def compare_strings(encoding, desired):
            n = min(len(encoding), len(desired))
            desired_end = desired[-n:]
            encoding_begin = encoding[:-n]
            encoding_end = encoding[-n:]
            matched = Huffman.compare_low_bits(desired_end, encoding_begin, encoding_end)
            return matched       

    def check_item(item, desired):
        encoding = item.label
        haveFoundNext = Huffman.compare_strings(encoding, desired)
        return haveFoundNext
        
    def do_searching_loop(labelled_items, desired):
        idx = 0
        output = None
        while idx < len(labelled_items) and not output:
            item = labelled_items[idx]
            haveFoundNext = Huffman.check_item(item, desired)
            if haveFoundNext:
                output = item.name
            idx = idx + 1
        return output

    def find_in_labelled_items(labelled_items, my_number):
        desired = Huffman.get_desired(my_number)
        output = Huffman.do_searching_loop(labelled_items, desired)
        return output 

    def run_loop(labelled_items, my_number, my_time_tracker):
        total_time = my_time_tracker.total_time()
        output = None
        while not output and total_time < my_time_tracker.time_limit:
            output = Huffman.find_in_labelled_items(labelled_items, my_number)
            my_number = my_number + 1 
            total_time = my_time_tracker.total_time()
        return output, total_time
                   
    def get_tree_element(self, my_number, my_time_tracker=None):
        if not my_time_tracker:
            my_time_tracker = TimeTracker()
        output, total_time = Huffman.run_loop(self.labelled_items, my_number, my_time_tracker)
        if total_time >= my_time_tracker.time_limit:
            raise HangsOnSearchingLoopException
        return output

        
class TimeTracker():

    def default_timer():
        while True:
            yield timeit.default_timer()

    def __init__(self, timer=None, time_limit=.5):
        if not timer:
            self.timer = TimeTracker.default_timer
        else:
            self.timer = timer
        self.time_limit = time_limit
        self.time_generator = self.timer()
        self.initial_time = next(self.time_generator)
        
    def total_time(self):
        next_guy = next(self.time_generator)
        total_time = next_guy - self.initial_time
        return total_time
    