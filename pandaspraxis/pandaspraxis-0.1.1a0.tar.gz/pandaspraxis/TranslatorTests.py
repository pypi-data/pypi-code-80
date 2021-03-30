####
## Helper functions (compare, canonicalize)
####

import pandas
import numpy
import sqlite3
import csv
import re
import json

from Translator import *

# Takes in a pandas object and "canonicalizes" it by 
# removing the index and turning a Series into a DataFrame

def canonicalize(pandas_object):
    if isinstance(pandas_object, pandas.core.series.Series):
        pandas_object = pandas_object.to_frame()
    elif not isinstance(pandas_object, pandas.core.frame.DataFrame):
        # probably a single string or number; put into a dataframe with wildcard column name
        pandas_object = pandas.DataFrame({'*': pandas_object}, columns=['*'], index=[0])
    
    if isinstance(pandas_object.index, pandas.core.indexes.numeric.Int64Index):
        if pandas_object.index.name is not None:
            # index is actually a column we want to keep, reset index to get it into columns
            pandas_object = pandas_object.reset_index()
        # either way, now reset the numbers to go from 0 to n
        pandas_object.index = pandas.RangeIndex(0, len(pandas_object.index))
    
    if not isinstance(pandas_object.index, pandas.core.indexes.range.RangeIndex):
        # neither range nor numeric index, take the column out
        pandas_object = pandas_object.reset_index()
        
    return pandas_object

# Compares two dataframes and outputs human-readable information about them

def compare(df1, df2, query, case_sense=True):
    # with case-sense False, compares lowercase column names;

        result = ""
        identical = True
        
        if not case_sense:
            df1 = df1.rename(columns={x:x.lower() if type(x) == str else x for x in df1.columns})
            df2 = df2.rename(columns={x:x.lower() if type(x) == str else x for x in df2.columns})
        
        # Check index
        if not df1.index.equals(df2.index):
            dftext = []
            for df in [df1, df2]:
                if type(df.index) == pandas.core.indexes.range.RangeIndex:
                    dftext.append(f"the range index ({df.index.start}, {df.index.stop})")
                else:
                    dftext.append(df.index)
            identical = False
            result += f"Indices were not identical. DF1 has\n{dftext[0]}\nand DF2 has\n{dftext[1]}.\n\n"
            df1 = df1.reset_index()
            df2 = df2.reset_index()
        
        # Check columns
        columns1 = set(df1.columns)
        columns2 = set(df2.columns)
        col_identical = True

        if columns1 == columns2:
            result += "Columns identical.\n\n"
        else:
            df1_extra = columns1.difference(columns2)
            df2_extra = columns2.difference(columns1)
            if len(df1_extra) == 1 and df2_extra == {'*'} or \
                len(df2_extra) == 1 and df1_extra == {'*'}:
                # treat * as wildcard character
                result += "Columns identical.\n\n"

            elif len(df1_extra) == 1 and len(df2_extra) == 1:
                # if same column, but different name, basically identical
                col1 = df1[df1_extra.pop()]
                col2 = df2[df2_extra.pop()]
                comparisons = col1 == col2
                if all(comparisons):
                    result += "Columns identical, but with different names.\n\n"
                else:
                    col_identical = False

            else:
                col_identical = False

            if not col_identical:
                identical = False
                if len(df1_extra) > 0:
                    result += f"DF1 has the extra column(s) {df1_extra}\n"
                if len(df2_extra) > 0:
                    result += f"DF2 has the extra column(s) {df2_extra}\n"
                result += "\n"

        # Check row length
        rows1 = df1.shape[0]
        rows2 = df2.shape[0]
        if rows1 == rows2:
            result += "Identical number of rows.\n\n"
        else:
            identical = False
            result += f"DF1 has {rows1} rows, and DF2 has {rows2} rows.\n\n"

        # Check row contents (for identical columns, not including the already-checked index)
        # Note that indexing into original dfs must be case-sensitive
        samecols = []
        for column1 in df1.columns:
            for column2 in df2.columns:
                if column1 != "index" and column1 == column2:
                    samecols.append((column1, column2))
                    continue
                    
        for columns in samecols:
            column1, column2 = columns
            comparisons = df1[column1] == df2[column2]
            if not all(comparisons):
                identical = False
                result += f"The DFs differ in column '{column1}', at positions:\n"
                for i, comparison in enumerate(comparisons):
                    if not comparison:
                        result += f"{i} ({df1[column1][i]} vs {df2[column2][i]})\n"
                        
        if identical: return "Identical."
        return result

####
## Short static tests
####
grades = pandas.read_csv('grades.csv', \
                         names=["student_id", "class", "grade"], \
                         dtype={'student_id': 'Int64', 'class': str, 'grade': numpy.float64})

student_info = pandas.read_csv('student_info.csv', \
                         names=["student_id", "name", "kerb"], \
                         dtype={'student_id': 'Int64', 'name': str, 'kerb': str})


connection = sqlite3.connect('grades.db')
cursor = connection.cursor()

tests = [
    {'name': 'simple_select',
     'sql': 'SELECT * FROM grades',
     'pandas': ('df = grades', 'df')},
    
    {'name': 'select_two',
     'sql': "SELECT student_id, class FROM grades",
     'pandas': ('df = grades', "df = df[['student_id','class']]", 'df')},
    
    {'name': 'simple_groupby',
     'sql': "SELECT student_id, class FROM grades GROUP BY student_id",
     'pandas': ('df = grades', "df = df.groupby('student_id').head(n=grades.shape[0])",
                "df = df[['student_id','class']]", 'df')},
    
    {'name': 'simple_where',
     'sql': 'SELECT * FROM grades WHERE student_id = 1',
     'pandas': ('df = grades', "df = df[df['student_id']==1]", 'df')},
    
    {'name': 'where_select_two',
     'sql': 'SELECT student_id, class FROM grades WHERE student_id = 1',
     'pandas': ('df = grades', "df = df[df['student_id']==1]", 
                "df = df[['student_id','class']]", 'df')},
    
    {'name': 'where_string',
     'sql': 'SELECT student_id, grade FROM grades WHERE class = \"6.031\"',
     'pandas': ('df = grades', 'df = df[df[\'class\']=="6.031"]', 
                "df = df[['student_id','grade']]", 'df')},

    {'name': 'count_all',
     'sql': 'SELECT COUNT(*) FROM grades',
     'pandas': ('df = grades', 'df = df.iloc[0]', 'df = df.count()', 'df')},
    
    {'name': 'simple_join',
     'sql': 'SELECT student_id, grade, kerb FROM grades JOIN student_info ON grades.student_id = student_info.student_id',
     'pandas': ('df = grades', 'df2 = student_info', "df = df.merge(df2, left_on='student_id',right_on='student_id')", 
                "df = df[['student_id','grade','kerb']]", 'df')},

    {'name': 'join_with_table_as',
     'sql': 'SELECT T1.student_id, T2.kerb FROM grades AS T1 JOIN student_info AS T2 ON T1.student_id = T2.student_id',
     'pandas': ('t1 = grades', 't2 = student_info', "t1 = t1.merge(t2, left_on='student_id',right_on='student_id')", 
                "t1 = t1[['student_id','kerb']]", 't1')}, #TODO: change this part?
]

probabilistic_tests = [
    {'name': 'select_one',
     'sql': 'SELECT student_id FROM grades',
      'pandas': [(('df = grades', 'df = df[\'student_id\']', 'df'), 0.7), 
                 (('df = grades', 'df = df[[\'student_id\']]', 'df'), 0.3)]},
    
    {'name': 'groupby_average',
     'sql': "SELECT AVG(grade), student_id FROM grades GROUP BY student_id",
     'pandas': [(('df = grades', 'df = df.groupby(\'student_id\').mean().reset_index()', 
                  'df = df[[\'grade\',\'student_id\']]','df'), 0.8),
                (('df = grades', 'df = df.groupby(\'student_id\').agg(\'mean\').reset_index()', 
                  'df = df[[\'grade\',\'student_id\']]','df'), 0.2)]},
    
    {'name': 'simple_function_max',
     'sql': 'SELECT MAX(grade) FROM grades',
     'pandas': [(('df = grades', 'df = df.max()', 'df = df[\'grade\']', 'df'), 0.8*0.7),
                (('df = grades', 'df = df.agg(\'max\')', 'df = df[\'grade\']', 'df'), 0.8*0.3),
                (('df = grades', 'df = df.max()', 'df = df[[\'grade\']]', 'df'), 0.2*0.7),
                (('df = grades', 'df = df.agg(\'max\')', 'df = df[[\'grade\']]', 'df'), 0.2*0.3)]},
    
    {'name': 'simple_as',
     'sql': 'SELECT student_id AS student_identity FROM grades',
     'pandas': [(('df = grades', 'df = df[\'student_id\']',
                  'df = df.rename(columns={\'student_id\':\'student_identity\',})',
                  'df'), 0.7),
                (('df = grades', 'df = df[[\'student_id\']]',
                  'df = df.rename(columns={\'student_id\':\'student_identity\',})',
                  'df'), 0.3),]},
]


# to_run is a regex controlling which test names are run
# verbose will print intermediate trees as well as final result
# det_prob controls running deterministic and probabilistic tests, respectively --
#     probabilistic tests run 100s of times, so turn them off when using print statements
def run_tests(to_run, verbose, det_prob):
    count = [0, 0]
    to_run = re.compile(to_run)
    
    for i, test in enumerate(tests):
        if not det_prob[0]: break
        if to_run.search(test['name']) is None: continue
        name = test['name']
        count[1] += 1
        if verbose: print('Testing', test['sql'])
        try:
            pandas_actual = tuple(translate_test(test['sql'], verbose))
        except Exception as e:
            print(f"Failed test {i}: error thrown while translating. Error message:\n{e})\n")
            continue

        if pandas_actual == test['pandas']:
            print(f"Passed test {name}.\n")
            count[0] += 1
            continue

        else: # commands are not text-equal, check if they are result-equal
            print(f"Test {name} returned an unexpected command: expected\n{test['pandas']}, got\n{pandas_actual}")
            for command in pandas_actual[:-1]:
                print(command)
                exec(command)
            pandas_actual_result = canonicalize(eval(pandas_actual[-1])) # pandas_actual puts result in variable `df`
            for command in test['pandas'][:-1]:
                exec(command)
            pandas_expected_result = canonicalize(eval(test['pandas'][-1]))

            try:
                match = True
                for column in pandas_expected_result.columns:
                    for j in range(len(pandas_expected_result[column])):
                        if pandas_expected_result[column][j] != pandas_actual_result[column][j]:
                            print(f"Failed test {i}: items were not equal. Expected result " \
                            f"was\n{pandas_expected_result}\n and got\n{pandas_actual_result}\n" \
                            f"from command {pandas_actual}")
                            match = False
                            break
                    if not match:
                        break
                if match:
                    count[0] += 1
                    print(f"Passed test {name}: different command, but items were equal.\n")

            except:
                print(f"Failed test {name}: with exception thrown. Expected result " \
                            f"was\n{pandas_expected_result}\n and got\n{pandas_actual_result}\n" \
                            f"from command {pandas_actual}")

    print(f"Passed {count[0]} of {count[1]} deterministic tests.\n\n")

    count = [0,0]
    runs = 100 # try each probabilistic test `runs` times
    error_margin = 0.15 # should be between 0 and 1; allow each test to be up to and including
                    # error_margin away from the given probability distribution

    def run_n_times(command, expected, counter):
        fail = False
        for i in range(runs):
            pandas_actual = tuple(translate_test(command, verbose=verbose))
            try:
                counter[pandas_actual] += 1
            except:
                print(f"Failed test {name}: incorrect pandas command returned. Expected result was one of " \
                            f"\n{test['pandas']}\n and got\n{pandas_actual}\n")
                fail = True
                break

        if not fail:
            for pandas_option in expected:
                if abs(counter[pandas_option[0]]/runs - pandas_option[1]) > error_margin:
                    print(f"Failed test {name}: probabilities did not match expected distribution. " \
                         f"Expected distrbution was\n{test['pandas']} and got\n{counter}\n")
                    fail = True
                    break

        return fail

    for i, test in enumerate(probabilistic_tests):
        if not det_prob[1]: break
        if to_run.search(test['name']) is None: continue
        name = test['name']
        count[1] += 1
        if verbose: print('Testing', test['sql'], 'probabilistically')

        for i in range(3):
            # Try the probabilistic test a few times if it fails the first time.
            fail = run_n_times(test['sql'], test['pandas'], 
                                          {pandas_option[0]: 0 for pandas_option in test['pandas']})
            if not fail:
                break

        if not fail:
            print(f"Passed probabilistic test {name}.\n")
            count[0] += 1
            continue

    print(f"Passed {count[0]} of {count[1]} probabilistic tests.")

####
## Data tests
####

try:
    if connections is not None:
        pass
except:
    # initialize connections and db_tables
    connections = {}
    db_tables = {}

# to_run is a regex controlling which sql commands are run
# dataset options: 'all_data.json' (19k), 'no_join_data.json' (12k), '100_no_join.json', '1000_no_join.json'
def run_training(to_run, dataset, verbose=False):
    count = {'total': 0, 'sql error': 0, 'pandas translate error': 0, 'pandas execute error': 0,
         'comparison error': 0, 'different result': 0, 'success': 0}
    queries = json.load(open(dataset))
    to_run = re.compile(to_run)
    
    for query in queries:
        if to_run.search(query[0]) is None: continue
        count['total'] += 1
        if count['total'] % 1000 == 0: print(f"Done {count['total']} of {len(queries)}")
        db = query[1]
        if db in connections:
            connection = connections[db]
            tables = db_tables[db]
        else:
            # set up connection to the SQL database
            # spider, cosql, and sparc all have same datasets, so just load spider's
            connection = sqlite3.connect(f'../../../Datasets/spider/database/{db}/{db}.sqlite')
            connection.text_factory = lambda x: x.decode('utf-8', 'ignore') # ignore unicode errors
            connections[db] = connection

            # load the tables from the database as pandas dataframes
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            sql_tables = cursor.fetchall()
            tables = {}
            for sql_table in sql_tables:
                table_name = sql_table[0].lower()
                table = pandas.read_sql_query("SELECT * from %s" % table_name, connection)
                table.columns = list(map(lambda x: x.lower(), table.columns))
                tables[table_name] = table
            db_tables[db] = tables

        try:
            sql_result = pandas.read_sql_query(query[0], connection)
        except Exception as e:
            #print(e)
            count['sql error'] += 1
            continue


        try:
            pandas_command = translate_test(query[0], verbose)

            try:
                # execute all the commands except the last one, which is the final variable to be evaluated
                exec('\n'.join(pandas_command[:-1]), globals(), tables)
                pandas_result = canonicalize(tables[pandas_command[-1]])

            except Exception as e3:
                count['pandas execute error'] += 1
                # print(query, '\n')
                # print(pandas_command, '\n')
                # print(e3, '\n\n')
                continue

            try:
                #TODO how best to compare between them?
                # check if they are identical (post-canonicalization)
                comparison = compare(sql_result, pandas_result, query[0], case_sense=False)
                if sql_result.equals(pandas_result) or comparison == "Identical.":
                    count['success'] += 1

                else:
                    count['different result'] += 1
                    # if count['total'] < 200:
                    #     print(f"Comparison for\n{query[0]}\nvs.\n{pandas_command}\non database {query[1]}")
                    #     print(comparison)
                    #     print("SQL:\n", sql_result, "\n\n")
                    #     print("Pandas:\n", pandas_result, "\n\n")

            except Exception as e1:
                count['comparison error'] += 1
                # if count['total'] < 2000:
                #     print(query)
                #     print(pandas_command)
                #     print(e1)
                #     print(sql_result)
                #     print(pandas_result)
                #     print('\n\n')
                continue
                

        except Exception as e2:
            count['pandas translate error'] += 1
            #trans_error.append(query)
            # print(query)
            # if count['total'] < 20:
            #         print(query)
            #         print(e2)

    print(f"Ran {count['total']} commands:")
    print(f"{count['success']} succeeded.")
    print(f"{count['different result']} ran correctly, but produced a different result.")
    print(f"{count['sql error']} threw an error while running the SQL command.")
    print(f"{count['pandas translate error']} threw an error while translating the Pandas command.")
    print(f"{count['pandas execute error']} threw an error while executing the Pandas command.")
    print(f"{count['comparison error']} threw an error while comparing the two result DataFrames.")

####
## Actually run tests
####

# Short and static
#run_tests('count', verbose=False, det_prob=[True, False])

# Data-based
#run_training('.*', '../../training_data/random_200.json', verbose=False)
# t1 = db_tables['ship_1']['captain']
# t2 = db_tables['ship_1']['ship']
# t1 = t1.merge(t2, left_on='ship_id',right_on='ship_id', suffixes=("_a","_b"))
# print(t1, "\n")
# t1 = t1[t2['name']=="HM Cutter Avenger"]
# print(t1)

# Other
#teststr = "SELECT T1.kerb FROM student_info AS T1 JOIN grades AS T2 ON T1.student_id = T2.student_id"
teststr = "SELECT COUNT(student_id) FROM grades GROUP BY class "
print(translate_real(teststr))