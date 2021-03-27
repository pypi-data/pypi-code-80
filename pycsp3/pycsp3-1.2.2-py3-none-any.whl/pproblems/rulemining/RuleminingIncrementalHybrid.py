import os
import subprocess
from lxml import etree
import re
import sys
import signal
import time
import uuid
import random
total_wall_time2 = 0
total_wall_time = 0
total_wall_time_pycsp = 0
total_wall_time_solver = 0
nsolutions = 100
ncurrentsolutions = 0
solutions = []
max_objective = 0
random.seed()
base_time = time.time()

nb_attr = 0

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

class Instantiation:
    def __init__(self, pretty_solution, variables, values):
        self.pretty_solution = pretty_solution
        self.variables = variables
        self.values = values

    def __repr__(self):
        return self.variables, self.values

    def __str__(self):
        return str(self.pretty_solution)

data = dict()
data["attributes"] = []
data["prediction"] = None

class Attribute():
    pos = 0

    def __init__(self, name, order, values):
        self.name = name
        self.order = order
        self.values = values
        self.position = Attribute.pos
        Attribute.pos = Attribute.pos + 1

    def __repr__(self):
        return str(self.name) + ": " + ",".join(element for element in self.values)

class Prediction():
    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def __repr__(self):
        return str(self.attribute) + " - " + self.operator + " - " + self.value

def add_attribute(name, elements):
    global data
    order = True if elements.startswith("<") else False
    if order:
        elements = elements[1:]
    elements = [element.replace("{","").replace("}","").strip() for element in elements.split(",")]
    attribute = Attribute(name, order, elements)
    data["attributes"].append(attribute)
    
    
def add_prediction(name, operator, value):
    global data
    attribute = [attribute for attribute in data["attributes"] if attribute.name == name][0]
    data["prediction"] = Prediction(attribute, operator, value)
    


def read_description(description_file):
    global nb_attr
    prediction_started = False
    f = open(description_file, "r") 
    for line in f: 
        if not prediction_started and "@attribute" in line:
            add_attribute(line.split(" ")[1], line.split(" ")[2])
        elif not prediction_started and "@prediction" in line:
            prediction_started = True
            add_prediction(line.split(" ")[1], line.split(" ")[2], line.split(" ")[3])
    nb_attr = len(data["attributes"]) - 1 

class Rulemining():

    def __init__(self, instance_desc, instance_training, instance_test, nb_rules=1, nb_terms=1, data_solution=None, type_solution=None):
        self.instance_desc = instance_desc
        self.instance_training = instance_training
        self.instance_test = instance_test
        self.nb_rules = nb_rules
        self.nb_terms = nb_terms
        self.data_solution = data_solution
        self.type_solution = type_solution
        self.nb_individuals = 0
        self.f_measure = 0
        self.time_pycsp3 = 0
        self.time_solver = 0
        self.result = None
        self.solver_log = None
        read_description(self.instance_desc)
        

    def get_objective(self, base_objective, log_file):
        objective = base_objective
        o = open(log_file, "r")
        r = o.readlines()
        for l in r:
            if l.startswith("o "):
                tmp  = int(l.split(" ")[1])
                if tmp > objective:
                    objective = tmp
        o.close()
        return objective

    def construct_id_file(self):
        id_file = "%.20f" % time.time()
        id_file = id_file.replace(".", "")
        id_file += "_" + str(random.randint(0, 100000))
        return id_file

    def start(self, limit_objective=True, sat=False):
        global max_objective
        global total_wall_time2
        global base_time
        global ncurrentsolutions
        id_file = self.construct_id_file()
        
        if ncurrentsolutions < nsolutions - 10:
            nsol = 10
        else:
            nsol = nsolutions - ncurrentsolutions
        if sat is True:
            cmd = "python3 pproblems/rulemining/RuleminingFmeasureSat.py -dataparser=pproblems/rulemining/RuleminingParserSat.py"
        else:
            cmd = "python3 pproblems/rulemining/RuleminingFmeasure.py -dataparser=pproblems/rulemining/RuleminingParser.py"
        cmd += " " + self.instance_desc
        cmd += " " + self.instance_training
        cmd += " " + self.instance_test
        cmd += " " + str(self.nb_rules)
        cmd += " " + str(self.nb_terms)
        cmd += " " + str(self.data_solution) + ""
        cmd += " " + str(self.type_solution) 
        cmd += " " + str(id_file)
        cmd += " " + str(max_objective)
        if sat is True:
            cmd += " " + str(nsol)
        print(cmd)
        
        #launch process
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
        
        #get the good log file
        uuid_mac = str(hex(uuid.getnode()))
        pid = str(os.getpgid(p.pid))
        
        end_file_name = str(uuid_mac)+"_"+str(pid)+"_"+str(id_file)+".log"
        print("ends file name:", end_file_name)
        
        log_files = []
        while log_files == []:
            filenames = [f for _, _, filenames in os.walk("pycsp3/solvers/") for f in filenames]
            log_files = [filename for filename in filenames if filename.endswith(end_file_name)]
            print("Wait that the solver runs :) ...")
            total_wall_time2 = time.time() - base_time
            if total_wall_time2 > limit_time:
                os.killpg(os.getpgid(p.pid), signal.SIGINT)
                print("kill due to time limit exceeded")            
                return
            time.sleep(1)
        print("nfiles found:", len(log_files))
        log_file = "pycsp3/solvers/"+log_files[0]

        print("Log file found: ", log_file)
        self.solver_log = log_file
        handler = signal.getsignal(signal.SIGINT)   
        def new_handler(frame, signum):
            os.killpg(os.getpgid(p.pid), signal.SIGINT)
        signal.signal(signal.SIGINT, new_handler)
        
        solving = False
        solving_lines = []
        modeling_lines = []
        outs = None
        objective = 0
        tmp_objective = 0
        no_change = 0
        
        
        before_objective = max_objective
        print("previous objective:", before_objective)
        while p.poll() is None:
            time.sleep(1)
            tmp_objective = objective
            objective = self.get_objective(objective,log_file)
            if sat is not True:
                print("objective:", objective)
            if objective != 0 and objective > max_objective:
                max_objective = objective
            if objective != 0 and objective != tmp_objective:
                no_change = 0
            if objective != 0 and objective == tmp_objective:
                no_change += 1
            if no_change == 30 and limit_objective and objective >= max_objective:
                print("kill due to no change of the objective:", objective)            
                os.killpg(os.getpgid(p.pid), signal.SIGINT)
                break
            #print(total_wall_time2)
            total_wall_time2 = time.time() - base_time
            if total_wall_time2 > limit_time:
                os.killpg(os.getpgid(p.pid), signal.SIGINT)
                print("kill due to time limit exceeded - objective:", objective)            
                break
            
        p.wait()
        outs, errs = p.communicate()
        #print(outs)
        #print(errs)
        p.terminate()
        signal.signal(signal.SIGINT, handler)  # Reset the right SIGINT
        
        objective = self.get_objective(objective,log_file)
        print("final objective:", objective)
        outs = outs.decode("utf-8").split("\n")
        for line in outs:
           if "Solving by AbsCon in progress" in line:
               solving = True
           if "Solved by AbsCon in" in line:
               solving = False
           if solving is False:    
               modeling_lines.append(line)
           else:
               solving_lines.append(line)
           #sys.stdout.write(line)
        
        self.result = "\n".join(modeling_lines)
        

    def get_information_from_result(self, pattern, *, position=-1):
        stdout = self.result
        if stdout.find(pattern) != -1:
            index = stdout.find(pattern)
            line = stdout[index:]
            line = line.split("\n")[0]
            line = line.split(" ")[position].strip()
            return escape_ansi(line) 
        return None
        
    def get_pretty_solution(self):
        stdout = self.result
        if stdout.find("Rule number") != -1:
            index = stdout.find("Rule number")
            line = stdout[index:]
            return escape_ansi(line) 
        return None

    def solutions(self, nb_rules, nb_terms):
        global ncurrentsolutions
        o = open(self.solver_log, "r")
        r = o.readlines()
        sols = []
        for l in r:
            if l.startswith(" <instantiation id="):
                ncurrentsolutions+=1
                data = l.split("<values>")[1]
                data = data.split("</values>")[0]
                data = data.strip()
                tmp_values = data.split()  # a list with all values given as strings (possibly '*')
                values = []
                # new code for * in the values of the solution 
                for value in tmp_values:
                    if "x" not in value:
                        values.append(value)
                    else:
                        val, n_val = value.split("x")
                        values.extend([val]*int(n_val))
                
                values = values[:3*(nb_terms*nb_rules)]
                #print("data:", values)
                str_sol = ""
                #s_attribute[][] s_value[][] s_operator[][]
                pos_attribute = 0
                pos_value = nb_terms*nb_rules
                pos_operator = (2*(nb_terms*nb_rules))
                #print(pos_attribute, pos_value, pos_operator)
                for i in range(nb_rules):
                    str_sol += "r"+str(i)+" "
                    for n in range(nb_terms):
                        str_sol += "attr:"+values[pos_attribute]+" value:"+values[pos_value]+" operator:"+values[pos_operator] + ";"
                        pos_attribute+=1
                        pos_value+=1
                        pos_operator+=1
                #print(data)
                sols.append(str_sol)
        create_file_solutions(sols)
        o.close()

    def solution(self, sat=False):
        global base_time   
        stdout = self.result
        try:
            total_wall_time2 = time.time() - base_time
            if sat is False and total_wall_time2 < limit_time:
                self.nb_individuals = int(self.get_information_from_result("Number of individuals:"))
                self.f_measure = float(self.get_information_from_result("fmeasure:"))
            self.time_pycsp3 = float(self.get_information_from_result("* Generating the file", position=-2))
            self.time_solver = float(self.get_information_from_result("* Solved by AbsCon in", position=-2))
        except:
            print("PROBLEM_____________________________________________________")
            print(stdout)
            return "problem"
        
        print(self.get_pretty_solution())
        if stdout.find("<unsatisfiable") != -1 or stdout.find("s UNSATISFIABLE") != -1:
            return Instantiation("unsatisfiable", None, None)
        if stdout.find("<instantiation") == -1 or stdout.find("</instantiation>") == -1:
            print("  Actually, the instance was not solved")
            return None
        left, right = stdout.rfind("<instantiation"), stdout.rfind("</instantiation>")
        s = stdout[left:right + len("</instantiation>")].replace("\nv", "")
        root = etree.fromstring(s, etree.XMLParser(remove_blank_text=True))
        variables = []
        for token in root[0].text.split():
            variables.append(token)
        tmp_values = root[1].text.split()  # a list with all values given as strings (possibly '*')
        values = []
        # new code for * in the values of the solution 
        for value in tmp_values:
            if "x" not in value:
                values.append(value)
            else:
                val, n_val = value.split("x")
                values.extend([val]*int(n_val))
        
        pretty_solution = etree.tostring(root, pretty_print=True, xml_declaration=False).decode("UTF-8").strip()
       
        return Instantiation(pretty_solution, variables, values)

    def increase_dimension_solution(self, solution, new_nb_rules, new_nb_terms):
        nb_variables_s = self.nb_rules * self.nb_terms
        
        old_solution = solution.values
        new_solution = []
        #print(old_solution)
        # for the variable s
        solution_s_attribute, old_solution = old_solution[:nb_variables_s], old_solution[nb_variables_s:]
        
        
        #print("solution_s_attribute:", solution_s_attribute)

        new_variable_s = self.increase_dimension_s(solution_s_attribute, new_nb_rules, new_nb_terms)
        new_solution.extend(new_variable_s)

        # for the variable s_values
        solution_s_value, old_solution = old_solution[:nb_variables_s], old_solution[nb_variables_s:]
        #print("solution_s_value:", solution_s_value)
        new_variable_s_value = self.increase_dimension_s(solution_s_value, new_nb_rules, new_nb_terms)
        new_solution.extend(new_variable_s_value)
        
        # for the variable s_operator
        solution_s_operator, old_solution = old_solution[:nb_variables_s], old_solution[nb_variables_s:]
        #print("solution_s_operator:", solution_s_operator)
        
        new_variable_s_operator = self.increase_dimension_s(solution_s_operator, new_nb_rules, new_nb_terms)
        new_solution.extend(new_variable_s_operator)
        
        # for the variable satisfies_term
        nb_variables_satisfies_term = self.nb_individuals * self.nb_rules * self.nb_terms
        
        solution_satisfies_term, old_solution = old_solution[:nb_variables_satisfies_term], old_solution[nb_variables_satisfies_term:]
        #print("solution_satisfies_term:", solution_satisfies_term)
        new_variable_satisfies_term = self.increase_dimension_satisfies_term(solution_satisfies_term, new_nb_rules, new_nb_terms)
        
        #print("NEXT")
        new_solution.extend(new_variable_satisfies_term)
        
        # for the variable satisfies_rule
        nb_variables_satisfies_rule = self.nb_individuals * new_nb_rules
        new_solution.extend(["*"]*nb_variables_satisfies_rule)

        # for the variable satisfies_ruleset
        new_solution.extend(["*"]*self.nb_individuals)

        # for TP and FP
        new_solution.extend(["*"]*2)
        return new_solution

    def increase_dimension_s(self, partial_solution, new_nb_rules, new_nb_terms):
        index = 0
        new_solution_s = []
        new_size = new_nb_rules * new_nb_terms
        for id_rule in range(self.nb_rules):
            for id_term in range(self.nb_terms):
                new_solution_s.append(partial_solution[index])
                index += 1
            id_term = self.nb_terms
            while id_term != new_nb_terms:
                new_solution_s.append("*")
                id_term += 1
        id_rule = self.nb_rules
        while id_rule != new_nb_rules:
            for id_term in range(new_nb_terms):
                new_solution_s.append("*")
            id_rule += 1
        return new_solution_s

    def increase_dimension_satisfies_term(self, partial_solution, new_nb_rules, new_nb_terms):
        new_solution_s = []
        nb_elements_individual = self.nb_rules*self.nb_terms
        start = 0
        end = nb_elements_individual
        for _ in range(self.nb_individuals):
            new_solution_s.extend(self.increase_dimension_s(partial_solution[start:end], new_nb_rules, new_nb_terms))
            start += nb_elements_individual
            end += nb_elements_individual
        return new_solution_s


#instance_description = "pproblems/rulemining/instances/ecoli1d/ecoli1d.1.desc"
#instance_training = "pproblems/rulemining/instances/ecoli1d/ecoli1d.individuals.1.training"
#instance_test = "pproblems/rulemining/instances/ecoli1d/ecoli1d.individuals.1.test"
instance_description = sys.argv[1]
instance_training = sys.argv[2]
instance_test = sys.argv[3]
limit_time = int(sys.argv[4])

warm_start_file = "warm_start.txt"
instantiation_file = "instantiation.txt"
solutions_file = "solutions.txt"

def delete_file_solutions():
    global solutions_file
    if os.path.exists(solutions_file):
        os.remove(solutions_file)
    

def create_file_solutions(sols):
    global solutions_file
    f = open(solutions_file, "a")
    for s in sols:
        f.write(s+"\n")
    f.close()  

def create_file_warm_start(solution_new_dimension):
    global warm_start_file
    if os.path.exists(warm_start_file):
        os.remove(warm_start_file)
    f = open(warm_start_file, "a")
    f.write(" ".join(solution_new_dimension))
    f.close()    

def create_file_instantiation(solution_new_dimension):
    global instantiation_file
    if os.path.exists(instantiation_file):
        os.remove(instantiation_file)
    f = open(instantiation_file, "a")
    f.write(" ".join(solution_new_dimension))
    f.close()

def run(*, nb_rules, nb_terms, solution_file=None, solution_type=None, limit_objective=True, sat=False):
    
    global total_wall_time, total_wall_time_solver, total_wall_time_pycsp 
    rulemining = Rulemining(instance_description, instance_training, instance_test, 
                        nb_rules, nb_terms, solution_file, solution_type)
    rulemining.start(limit_objective, sat=sat)
    
    solution = rulemining.solution(sat=sat)
    print("solution:\n", solution)
    print("fmeasure:", rulemining.f_measure)
    print()
    print("For ", nb_rules, " rules and ", nb_terms, " terms")
    print("pycsp3 time:", rulemining.time_pycsp3, " seconds")
    print("solver time:", rulemining.time_solver, " seconds")
    print("pycsp3 + solver time:", "{:.2f}".format(rulemining.time_solver + rulemining.time_pycsp3), " seconds")
    total_wall_time = total_wall_time + rulemining.time_solver + rulemining.time_pycsp3
    total_wall_time_solver = total_wall_time_solver + rulemining.time_solver
    total_wall_time_pycsp = total_wall_time_pycsp + rulemining.time_pycsp3 
    print("total time pycsp3:", "{:.2f}".format(total_wall_time_pycsp), " seconds")
    print("total time solver:", "{:.2f}".format(total_wall_time_solver), " seconds")
    print("total time:", "{:.2f}".format(total_wall_time), " seconds")
    return rulemining

def create_warm(solution, nb_rules, nb_terms):
    global warm_start_file
    if solution is not None and solution != "problem":
        print("Warm loaded ...")   
        warm_start_file = construct_filename("warm_start_"+str(nb_rules)+"_"+str(nb_terms)+"_",".txt")
        create_file_warm_start(solution.values)
        return True
    return False

def time_exceeded():
    global base_time
    global limit_time
    if time.time() - base_time > limit_time:
        return True
    return False

def construct_filename(begin="model", end=".xml"):
    id_file = "%.20f" % time.time()
    id_file = id_file.replace(".", "")
    id_file += "_" + str(random.randint(0, 100000))
    uuid_mac = str(hex(uuid.getnode()))
    pid = os.getpid()
    return begin+str(uuid_mac)+"_"+str(pid)+"_"+str(id_file)+end
    
def instantiation_strategy(total_nb_rules=2, total_nb_terms=2, *, warm_start=False):
    global max_objective
    global limit_time
    global nb_attr

    global warm_start_file
    global instantiation_file
    global solutions_file

    #first case
    nb_rules = 1
    nb_terms = 1
    good_nb_rules = nb_rules
    good_nb_terms = nb_terms
    add_term = True #true if add a term, false if add a rule
    limit_time = limit_time / 2
    
    print("_________________________________________")
    print("FIRST PHASE INSTANTIATION until nb_rules:", total_nb_rules, " - nb_terms:", total_nb_terms)
    print("FIRST PHASE INSTANTIATION until the limit time:", limit_time)
    print("_________________________________________")
    print("_________________________________________")
    print("FIRST PROBLEM nb_rules:", nb_rules, " - nb_terms:", nb_terms)
    print("_________________________________________")
        
    rulemining = run(nb_rules=nb_rules, nb_terms=nb_terms)
    solution = rulemining.solution()
    create_warm(solution, nb_rules, nb_terms)
    print("nb_attr:", nb_attr)
    if total_nb_terms > nb_attr:
        total_nb_terms = nb_attr
        
    if not time_exceeded():
        
        nb_terms = nb_terms + 1 if add_term else nb_terms
        nb_rules = nb_rules + 1 if not add_term else nb_rules
        add_term = False if add_term is True else True
        prev_nb_terms = nb_terms
        prev_nb_rules = nb_rules
        
        while nb_terms <= total_nb_terms and nb_rules <= total_nb_rules:
            
            print("_________________________________________")
            print("INSTANTIATION nb_rules:", nb_rules, " - nb_terms:", nb_terms)
            print("_________________________________________")
            
            solution_new_dimension = rulemining.increase_dimension_solution(solution, nb_rules, nb_terms)
            instantiation_file = construct_filename("instantiation_"+str(nb_rules)+"_"+str(nb_terms)+"_",".txt")
            
            create_file_instantiation(solution_new_dimension)
            rulemining = run(   nb_rules=nb_rules,
                                nb_terms=nb_terms, 
                                solution_file=instantiation_file, 
                                solution_type="Instantiation")
            solution = rulemining.solution()

            
            if create_warm(solution, nb_rules, nb_terms):
                good_nb_rules = nb_rules
                good_nb_terms = nb_terms

            if solution == "problem":
                print("Stop first phase due to: problem in the solution ...")
                break
            if time_exceeded():
                print("Stop first phase due to: time exceeded ...")
                break
            
            prev_nb_terms = nb_terms
            prev_nb_rules = nb_rules    
            
            if nb_terms == total_nb_terms:
                add_term = False 
            nb_terms = nb_terms + 1 if add_term else nb_terms
            nb_rules = nb_rules + 1 if not add_term else nb_rules
        
            if nb_terms == total_nb_terms:
                add_term = False
            else:
                add_term = False if add_term is True else True

            
        nb_terms = good_nb_terms
        nb_rules = good_nb_rules

    if not time_exceeded():
        print("_________________________________________")
        print("SECOND PHASE WARM on nb_rules:", nb_rules, " - nb_terms:", nb_terms)
        print("SECOND PHASE WARM until the limit time:", limit_time)
        print("_________________________________________")
        rulemining = run(   nb_rules=nb_rules, 
                            nb_terms=nb_terms, 
                            solution_file=warm_start_file, 
                            solution_type="Warm",
                            limit_objective=False)
        solution = rulemining.solution()
        create_warm(solution, nb_rules, nb_terms)
    else:
        print("Stop second phase due to: time exceeded ...")
                
        #    nb_terms -= 1

    limit_time = limit_time * 2
    
    solutions_file = construct_filename("solutions_"+str(nb_rules)+"_"+str(nb_terms)+"_",".txt")
    
    print("_________________________________________")
    print("THIRD PHASE SAT on nb_rules:", nb_rules, " - nb_terms:", nb_terms)
    print("THIRD PHASE SAT until the limit time:", limit_time)
    print("_________________________________________")
    while ncurrentsolutions != nsolutions:
        print("pass objective: ", max_objective)
        rulemining = run(   nb_rules=nb_rules, 
                            nb_terms=nb_terms, 
                            solution_file=warm_start_file, 
                            solution_type="Warm", 
                            limit_objective=False, 
                            sat=True)
        
        if rulemining.solver_log is not None:
            solution = rulemining.solutions(nb_rules, nb_terms)
        print("solutions: ", ncurrentsolutions)
        max_objective-=1
        

        if time_exceeded():
            print("Stop third phase due to: time exceeded ...")
            break
        
instantiation_strategy(warm_start=True)
print("solutions_file:", solutions_file)