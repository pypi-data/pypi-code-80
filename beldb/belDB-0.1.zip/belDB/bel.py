import os.path
import ast


class Bel():
    
    def __init__(self):

        if not os.path.isfile('db.bel'):
            open("db.bel", "w").close()

        self.file = "db.bel"

    def get(self, key):
        file = open(self.file, "r")

        lines = file.readlines()
        output = ""
        for line in lines:
            line_key, line_value = line.split(":")


            if line_key == key:
                output = line_value
                break


        if output == "":
            return None

        else:
            try:
                as_list = ast.literal_eval(output)
                return as_list

            except ValueError:
                return output[:-1]
        
    def set(self, key, value):

        if not isinstance(key, str):
            raise Exception("The given key " + str(key) +" is " + type(key) + " and not str")
            return



        file = open(self.file, "a")


        file.write(key + ":" + str(value) + "\n")
        


    def reset(self):
        open(self.file, "w").write("")


    def get_keys(self):
        keys = []

        file = open(self.file, "r")

        lines = file.readlines()
        for line in lines:
            line_key, line_value = line.split(":")
            keys.append(line_key)

        return keys

    def get_values(self):
        values = []

        file = open(self.file, "r")

        lines = file.readlines()
        for line in lines:
            line_key, line_value = line.split(":")
            values.append(line_value)

        return values

    def get_all(self):
        items = []

        file = open(self.file, "r")

        lines = file.readlines()
        for line in lines:
            line_key, line_value = line.split(":")
            items.append([line_key, line_value])

        return items

    def search(self, value):
        file = open(self.file, "r")

        lines = file.readlines()
        output = ""
        for line in lines:
            line_key, line_value = line.split(":")
            line_value = line_value[:-1]

            if line_value == str(value):
                output = line_key
                break

        if output == "":

            return None

        else:
            return (output, value)

