def print_list(name,level=0):
    for each_item in name:
        if isinstance(each_item,list):
            print_list(each_item,level+1)
        else:
            print(each_item)
