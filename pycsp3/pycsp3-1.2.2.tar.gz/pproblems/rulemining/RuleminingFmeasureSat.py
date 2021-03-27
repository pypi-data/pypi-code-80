
# Rule mining problem (partial classification): A solution is a matrix s[i][j] that represents a disjunction of rules. Each line "i" is a rule and represents a conjunction of terms. Hence, each position "j" is a term and is associated to the attribute of the position "j" of the table called attributes. Note also that we fix the number of term to the number of attributs. Several heuristics allow to measure the quality of solutions. In this model, our objective is to maximize the number of both True Positive and True Negative individuals. When the solver found a solution, we calculate the F-mesure of the solution (decimal between [0, 1]). The closer the f-measurement of the solution is to 1, the better the solution is. 

#command: python3 pproblems/rulemining/RuleminingIntensionOrder.py -dataparser=pproblems/rulemining/Rulemining_Parser.py pproblems/rulemining/instances/ecoli1d/ecoli1d.desc pproblems/rulemining/instances/ecoli1d/ecoli1d.individuals.1.training pproblems/rulemining/instances/ecoli1d/ecoli1d.individuals.1.test

from pycsp3 import *
from pycsp3.solvers.abscon import AbsConProcess
from itertools import chain, combinations
from shutil import copyfile

import uuid
import time
import random

attributes, prediction, individuals, nb_rules, nb_terms, solution_data, solution_type, id_file, borne_min, nsolutions = data
max_rules = int(nb_rules)
max_terms_per_rule = int(nb_terms)
max_terms = max_rules * max_terms_per_rule

borne_min = int(borne_min)
if borne_min == 0:
    borne_min = 1


#positive_individuals = [tuple(element[:-1]) for element in individuals if element[-1] == 0] 
#negative_individuals = [tuple(element[:-1]) for element in individuals if element[-1] == 1]


index_prediction = [index for index, value in enumerate(prediction.attribute.values) if value.strip() == prediction.value.strip()][0]
print("index_prediction:", index_prediction)
class_individuals = [1 if element[-1][1] == index_prediction else 0 for element in individuals]
individuals = [tuple(element[:-1]) for element in individuals]
individuals_indexes = []
individuals_value = []
for indi in individuals:
    new_indi = []
    new_value = []
    for t in indi:
        new_indi.append(t[0])
        new_value.append(t[1])
    individuals_indexes.append(new_indi)
    individuals_value.append(new_value)
    

nb_attributes = len(attributes)-1
nb_individuals = len(individuals) 

nb_positive_individuals = len([ele for ele in class_individuals if ele == 1])
nb_negative_individuals = len([ele for ele in class_individuals if ele == 0])

attributes_domains_len = [len(attribute.values) for attribute in attributes]
max_attributes_domains = max(attributes_domains_len) 

coefficient_objective = nb_negative_individuals//nb_positive_individuals if nb_positive_individuals < nb_negative_individuals else 1

print()
print("Modeling ...")
print("Number of attributes: ", nb_attributes)
print("Number of individuals: ", nb_individuals)
print("prediction:", prediction.value.strip())
print("Number of individuals for the prediction: ", nb_positive_individuals)
print("Number of individuals that do not the prediction: ", nb_negative_individuals)

print("coefficient_objective:", coefficient_objective)
print("Max rules : ", max_rules)
print("max_terms_per_rule : ", max_terms_per_rule)
print("max_terms: ", max_terms)
print("solution_data: ", solution_data)
print("solution_type: ", solution_type)
print("borne_min: ", borne_min)

def convert1Dto2D(data):
    new_data = []
    index = 0
    for r in range(max_rules):
        n = []
        for t in range(max_terms_per_rule):
            n.append(elements[index])
            index+=1 
        new_data.append(n)
    return new_data

if solution_data != "None" and solution_type == "Instantiation":
    f = open(solution_data, "r")
    tmp = f.read()
    f.close()
    solution_data = tmp
    solution_data = solution_data.replace("[", "").replace("]", "").strip()
    elements = solution_data.split(" ")
    s_attribute_data = convert1Dto2D(elements)
    elements = elements[max_rules*max_terms_per_rule:]
    s_value_data = convert1Dto2D(elements)
    elements = elements[max_rules*max_terms_per_rule:]
    s_operator_data = convert1Dto2D(elements)
        
EQ = 1 # =
LT = 2 # <
GT = 3 # >



# s(r)(t) represents a disjunction of rules. Each line r is a rule and represents a conjunction of t terms. 
s_attribute = VarArray(size=[max_rules, max_terms_per_rule], dom=range(nb_attributes))

# s_value(r)(t) is the value of the term t of the rule r
s_value = VarArray(size=[max_rules, max_terms_per_rule], dom=range(max_attributes_domains))

# s_operator(r)(t) 0: not used - EQ:1: == - LT:2: > - GT:3: <  
s_operator = VarArray(size=[max_rules, max_terms_per_rule], dom={-1, EQ, LT, GT})

# p(i,r,t) == 1 if the individual i satisfies the term t of the rule r 
satisfies_term = VarArray(size=[nb_individuals, max_rules, max_terms_per_rule], dom={0, 1})

# satisfies_rule(i,r) == 1 if the individual i validates the rule r 
satisfies_rule = VarArray(size=[nb_individuals, max_rules], dom={0,1})

# satisfies_ruleset(i) == 1 if the individual i satisfies any rule
satisfies_ruleset = VarArray(size=nb_individuals, dom={0,1})

# True positive (solution says positive and the individual is positive)
tp = Var(dom=range(1, nb_positive_individuals))

tp_100 = Var(dom=range(100, nb_positive_individuals*100))

sensitivity_f = Var(dom=range(1,100))

# False positive (solution says positive but the individual is negative)
fp = Var(dom=range(nb_negative_individuals))

confidence_1 = Var(dom=range(1, nb_individuals))

confidence_f = Var(dom=range(1, 100))

fmeasure_1 = Var(dom=range(1, 200))
fmeasure_2 = Var(dom=range(1, 10000))
fmeasure_3 = Var(dom=range(1, 20000))

fmea = Var(dom=range(borne_min, 100))

def score_positive_table():
    return [(0,1),(1,0)]

def score_negative_table():
    return [(0,0),(1,1)]

# (satisfies_term[i][r][t], s_attribute[r][t], s_operator[r][t], s_value[r][t])
def create_table_satisfies_term(t, id_individual, id_rule, id_term):
    table = []
    max_values = len(range(max_attributes_domains))
    for id_attribute,attribute in enumerate(attributes):
        if id_attribute in individuals_indexes[id_individual]:
            index_value = individuals_indexes[id_individual].index(id_attribute)
            value = individuals_value[id_individual][index_value]
        else:
            value = 0  
        nb_possible_values = len(attribute.values)
        assert 0 <= value < nb_possible_values, "Bad value of a attribute for an individual"
        
        # For EQ
        for i in range(0, nb_possible_values):
            if i == value:
                table.append((1, id_attribute, EQ, i))
            else:
                table.append((0, id_attribute, EQ, i))
        if nb_possible_values > 3:
            # For LT
            if value == 0: #case <0 not possible
                #pass
                table.append((0, id_attribute, LT, ANY))
            else:
                # if value == 2: (1, 0, 2, <2(<=1))(0,0,2,>=2)
                table.append((1, id_attribute, LT, lt(value)))
                # and to avoid value between [nb_possible_values, max_values]
                for i in range(value, nb_possible_values):
                    table.append((0, id_attribute, LT, i))
            
            # For GT
            if value == nb_possible_values -1: #case > nb_possible_values -1 not possible 
                table.append((0, id_attribute, GT, ANY))
            else:
                table.append((0, id_attribute, GT, le(value)))
                for i in range(value + 1, nb_possible_values):
                    table.append((1, id_attribute, GT, i))
        
    table.append((1, ANY, -1, ANY))
    
    return table

# (satisfies_term[i][r][t], s_attribute[r][t], s_operator[r][t], s_value[r][t])
def create_table_satisfies_term_complete(t, id_individual, id_rule, id_term):
    table = []
    max_values = len(range(max_attributes_domains))
    for id_attribute,attribute in enumerate(attributes):
        if id_attribute in individuals_indexes[id_individual]:
            index_value = individuals_indexes[id_individual].index(id_attribute)
            value = individuals_value[id_individual][index_value]
        else:
            value = 0  
        table.append((1, id_attribute, EQ, value))
        table.append((0, id_attribute, EQ, ne(value)))
        table.append((1, id_attribute, LT, lt(value)))
        table.append((0, id_attribute, LT, ge(value)))
        table.append((1, id_attribute, GT, gt(value)))
        table.append((0, id_attribute, GT, le(value)))
    table.append((1, ANY, -1, ANY))
    return table
        
satisfy(
    [AllDifferent(s_attribute[r]) for r in range(max_rules)],
    
    [Count(s_operator[r], value=-1) < max_terms_per_rule for r in range(max_rules)],
    
    #To avoid that an attribute is both < and the value 0
    [imply(((s_operator[r][t] == GT)|(s_operator[r][t] == LT)) & (s_attribute[r][t] == id_attribute), s_value[r][t] != 0)
        for r in range(max_rules) 
        for t in range(max_terms_per_rule)
        for id_attribute, attribute in enumerate(attributes)
    ],

    # To avoid that an attribute is > to its max_values
    [imply(((s_operator[r][t] == GT)|(s_operator[r][t] == LT)) & (s_attribute[r][t] == id_attribute), s_value[r][t] != len(attribute.values)-1)
        for r in range(max_rules) 
        for t in range(max_terms_per_rule)
        for id_attribute, attribute in enumerate(attributes)
    ],

    #For domain between s_attribute[r][t] and s_value[r][t]
    [imply(s_attribute[r][t] == id_attribute, s_value[r][t] < len(attribute.values))
        for r in range(max_rules) 
        for t in range(max_terms_per_rule)
        for id_attribute, attribute in enumerate(attributes)
    ],

    # Link the solution and satisfies_term(i,r,t)
    [(satisfies_term[i][r][t], s_attribute[r][t], s_operator[r][t], s_value[r][t]) in create_table_satisfies_term(individuals, i, r, t) 
        for i in range(nb_individuals) 
        for r in range(max_rules) 
        for t in range(max_terms_per_rule)],

    # Conjunction of rule for all individuals
    [conjunction(satisfies_term[i][r]) == satisfies_rule[i][r] for i in range(nb_individuals) for r in range(max_rules)],

    # An individual validates the solution if the disjunction of rules is true with the current solution
    [disjunction(satisfies_rule[i]) == satisfies_ruleset[i] for i in range(nb_individuals)],

    # TP
    Count([satisfies_ruleset[i] for i in range(nb_individuals) if class_individuals[i] == 1], value=1) == tp,

    # FP
    Count([satisfies_ruleset[i] for i in range(nb_individuals) if class_individuals[i] == 0], value=1) == fp,

    tp_100 == tp * 100,
    sensitivity_f == tp_100 // nb_positive_individuals,
    confidence_1 == (tp + fp), 
    confidence_f == tp_100 // confidence_1,
    fmeasure_1 == sensitivity_f + confidence_f,
    fmeasure_2 == sensitivity_f * confidence_f,
    fmeasure_3 == 2 * fmeasure_2, fmea == fmeasure_3 // fmeasure_1, fmea == borne_min
)

if solution_type == "Instantiation":
    satisfy(
        # Instantiation attributes
        [s_attribute[r][t] == s_attribute_data[r][t] for r in range(max_rules) for t in range(max_terms_per_rule) if s_attribute_data[r][t] != "*"],

        # Instantiation values
        [s_value[r][t] == s_value_data[r][t] for r in range(max_rules) for t in range(max_terms_per_rule) if s_value_data[r][t] != "*"],

        # Instantiation operators
        [s_operator[r][t] == s_operator_data[r][t] for r in range(max_rules) for t in range(max_terms_per_rule) if s_operator_data[r][t] != "*"],
            
    )

def construct_filename(begin="model", end=".xml"):
    id_file = "%.20f" % time.time()
    id_file = id_file.replace(".", "")
    id_file += "_" + str(random.randint(0, 100000))
    uuid_mac = str(hex(uuid.getnode()))
    pid = os.getpid()
    return begin+str(uuid_mac)+"_"+str(pid)+"_"+str(id_file)+end
    
name = construct_filename("model_sat_"+str(max_rules)+"_"+str(max_terms_per_rule)+"_"+nsolutions+"_")
print("name of the xml file:", name)
instance = compile(name)

#if solution_type != "Instantiation":
#    copy = "Rulemining_"+str(max_rules)+"_"+str(max_terms_per_rule)+".xml"
#    copyfile(instance, copy)
abscon = AbsConProcess()
abscon.command = "java -Xmx50000M -jar ace/build/libs/ACE-20-12.jar"
abscon.id_file = id_file
verbose = ""
#max_time = " -positive=str2 -valh=Rand"
#max_time = " -aie=3 -vie=100000000 -positive=str2 -valh=Rand -npc"
max_time = " -positive=str2 -npc -jsonLimit=0 -xas -s="+nsolutions

warm = "-warm="+str(solution_data) if solution_data != "None" and solution_type == "Warm" else ""

dict_options={"args": warm + max_time}
print(dict_options)
result, solution = abscon.solve(instance, verbose, dict_options=dict_options)

def check_solution_order():
    tp, fp, fn, tn = 0, 0, 0, 0
    for index_individual, individual in enumerate(individuals):
        index_attributes = 0
        index_values = max_rules * max_terms_per_rule
        index_orders = (max_rules * max_terms_per_rule)*2
        or_for_rules = False
        for rule in range(max_rules):
            and_for_terms = []
            for term in range(max_terms_per_rule):
                attribute = solution.values[index_attributes] # Attribute
                value = solution.values[index_values + index_attributes]
                order = solution.values[index_orders + index_attributes]
                if int(order) != -1:
                    if int(attribute) in individuals_indexes[index_individual]:
                        position = individuals_indexes[index_individual].index(int(attribute))
                        value_individual = individuals_value[index_individual][position]
                    else:
                        value_individual = 0
                        
                    if int(order) == EQ:
                            and_for_terms.append(int(value) == int(value_individual))
                    elif int(order) == LT:
                            and_for_terms.append(int(value) < int(value_individual))
                    elif int(order) == GT:
                        and_for_terms.append(int(value) > int(value_individual))
                    else:
                        print("error: " + order + " not possible")
                        exit(0)

                index_attributes = index_attributes + 1
            #print(individual)
            if all(and_for_terms):
                or_for_rules = True
                break
        
        if or_for_rules:
            if class_individuals[index_individual]:
                #print("TP: ", individual)
                tp+=1
            else:
                #print("FP: ", individual)
                fp+=1
        else:
            if class_individuals[index_individual]:
                #print("FN: ", individual)
                fn+=1
            else:
                #print("TN: ", individual)
                tn+=1
    return tp, tn, fp, fn 
    

def print_solution_order():
    solution_str = ""
    index_attributes = 0
    index_values = max_rules * max_terms_per_rule
    index_orders = (max_rules * max_terms_per_rule)*2
    for rule in range(max_rules):
        solution_str += "Rule number " + str(rule) + ":\n"
        for term in range(max_terms_per_rule):
            attribute = solution.values[index_attributes] # Attribute
            attr = attributes[int(attribute)] 
            value = solution.values[index_values + index_attributes]
            if int(value) >= len(attr.values):
                print("The value of a term is not possible:", attr.values, int(value))
                return None
            sol = attr.values[int(value)]
            order = solution.values[index_orders + index_attributes]
            if int(order) != -1:
                if int(order) == EQ:
                    str_order = "="
                elif int(order) == LT:
                    str_order = ">"
                elif int(order) == GT:
                    str_order = "<"
                else:
                    print("error: " + order + " not possible")
                    exit(0)
                solution_str += " " + attr.name + " " + str_order + " " + str(sol)    
            index_attributes = index_attributes + 1
        solution_str += "\n"
    return solution_str
    
def sensitivity(tp, tn, fp, fn):
    if tp + fn == 0:
        return 0 
    return tp / (tp + fn)

def confidence(tp, tn, fp, fn):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)

def fmeasure(s, c):
    if c + s == 0:
        return 0
    return (2 * c * s) / (c + s)

print("Result:", result)

if result != "UNSAT" and result != "UNKNOWN":

    tp, tn, fp, fn = check_solution_order()
    print(solution)

    print("tp:", tp)
    print("tn:", tn)
    print("fp:", fp)
    print("fn:", fn)

    s = sensitivity(tp, tn, fp, fn)
    print("sensitivity:", s)
    
    c = confidence(tp, tn, fp, fn)
    print("confidence:", c)
    
    f = fmeasure(s, c)
    print("fmeasure:", f)

    print("sensitivity:", s)
    print("confidence:", c)
    print("fmeasure:", f)

    print(print_solution_order())
