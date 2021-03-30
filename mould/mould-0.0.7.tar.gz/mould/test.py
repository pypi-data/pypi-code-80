import mould
# from mould._utils import _build_python_code
variables = {"text": "World !", "marker": "Macbook Pro",
             "name": "Python", "n": 1, "x": 6, "y": 6, "d": {"a": 1, "b": 2}, "l": [1, 2, 3, 4, 5], "t": ("q", "w", "e", "r", "t", "y")}

# input_data = '''{% if x == y %}
# This is from a nested IF
# {{ n+44 }}
# This is "just" a line
# {% else %}
# This is line {{ n }}
# {% endif %}
# ending block'''

print(mould.it("/Users/raam/Desktop/PyWorkspace/test", variables))
# print(mould.it(input_data, variables))
# input = open("/Users/raam/Desktop/PyWorkspace/test").read()

# op = _build_python_code(input, variables)
# op = _build_python_code(input_data, variables)

# print(op)
