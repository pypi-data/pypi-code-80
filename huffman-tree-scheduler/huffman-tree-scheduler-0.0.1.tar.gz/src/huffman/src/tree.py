import copy

class Tree():

    def __init__(self, my_dict):
        self.nodes = []
        for item in my_dict.keys():
            my_node = Node(item, my_dict[item])
            self.nodes.append(my_node)
            
    def __eq__(self, other):
        return self.nodes == other.nodes
        
    def __str__(self):
        my_string = "Tree with nodes: "
        for node in self.nodes:
            my_string += str(node) + "\n"
        return my_string
        
    def create_trivial_output(nodes):
        item = LabelledItem((nodes[0].item_list[0][0], "o"))
        output = [item]
        return output
    
    def create_nontrivial_output(nodes):
        output = []
        for item in nodes[0].item_list:
            output.append(LabelledItem(item))
        return output

    def create_output(nodes):
        if len(nodes[0].item_list) == 1:
            output = Tree.create_trivial_output(nodes)
        else:
            output = Tree.create_nontrivial_output(nodes)
        return output

    def do_huffman(self):
        output_string = """"""
        
        while len(self.nodes) > 1:
            self.combine_nodes()
        
        output = []
        if len(self.nodes) == 1:
            output = Tree.create_output(self.nodes)
        return output
        
    def remove_two_lowest_nodes(self, lowest_node, next_lowest_node):
        self.nodes.remove(lowest_node)
        self.nodes.remove(next_lowest_node)
        
    def combine_nodes(self):
        lowest_node, next_lowest_node = self.find_two_lowest_nodes()
        self.remove_two_lowest_nodes(lowest_node, next_lowest_node)
        combined_node = Tree.squish_nodes_together(lowest_node, next_lowest_node)
        self.nodes.append(combined_node)
        
    def find_lowest_node(self):
        min_weight = min([node.weight for node in self.nodes])
        for node in self.nodes:
            if node.weight == min_weight:
                lowest_node = node
        return lowest_node
        
    def find_next_lowest_node(self, lowest_node):
        next_min_weight = min([node.weight for node in self.nodes if node != lowest_node])
        for node in self.nodes:
            if node.weight == next_min_weight and node != lowest_node:
                next_lowest_node = node
        return next_lowest_node
        
    def find_two_lowest_nodes(self):
        lowest_node = self.find_lowest_node()
        next_lowest_node = self.find_next_lowest_node(lowest_node)
        return lowest_node, next_lowest_node   
        
    def squish_nodes_together(lowest_node, next_lowest_node):
        new_node = copy.deepcopy(lowest_node)
        for item in new_node.item_list:
            item[1] = "o" + item[1]
        for item in next_lowest_node.item_list:
            item[1] = "l" + item[1]
        new_node.item_list += next_lowest_node.item_list
        new_node.weight += next_lowest_node.weight
        return new_node

class Node():
    def __init__(self, item, weight):
        self.item_list = [[item, ""]]
        self.weight = weight
        
    def __eq__(self, other):
        return self.item_list == other.item_list and self.weight == other.weight
        
    def __str__(self):
        return f"Node with items {self.item_list} and weight {self.weight}"
      
      
class LabelledItem():

    def __init__(self, item):
         self.label = item[1]
         self.name = item[0]
         
    def __str__(self):
        return f"Item with label {self.label} and name {self.name}"
        
    def __eq__(self, other):
        return self.label == other.label and self.name == other.name
  