def print_list(name):
    for each_item in name:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print(each_item)
