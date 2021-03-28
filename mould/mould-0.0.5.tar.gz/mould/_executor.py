# Wrapper function that calls the code builder with input content and input variables
import os
import io
from _utils import _build_python_code, _validate_input_syntax, _parse_the_variables


def it(input_template_content, input_variables):
    '''
    Description:
    This function gets the user input and renders the templated output with values applied for the variables, conditionals and loops processed

    Parameters:
    input_template_content (string or file) : This is the user input, which can be a string or a file.
    input_variables (dictionary) : This is the collection of variables and their values as a dictionary

    Returns:
    output_text (string) : Returns the rendered file as a string

    Usage Example:
                $ sample_input = "
                This is where it all starts!!!
                Hello {{ text }} This is a wonderful day. My name is {{ name }}.
                {% if a < b %}
                'b' is bigger
                The value of b is {{ b }}
                {% else %}
                'a' is bigger
                The value of a is {{ a }}
                {% endif %}
                "
                $ sample_variables = {
                "text" : "World !"
                "name" : "Python"
                "a" : 50
                "b" : 100
                }
                $ mould.it(sample_input,sample_variables)
                This is where it all starts!!!
                Hello World ! This is a wonderful day. My name is Python
                'b' is bigger
                The value of b is 100

    '''
    try:
        input_content = ""
        # Checks whether the input_variables is a dictionary and if it is otherwise, returns to user with the same message
        if type(input_variables) != dict:
            return "Error: input_variables should be of type 'dictionary'"

        if os.path.isfile(input_template_content) and len(open(input_template_content).read().strip()) != 0:
            input_content = open(input_template_content).read()
        elif len(input_template_content.strip()) != 0:
            input_content = input_template_content
        else:
            return "Error: 'input_template_content' cannot be empty"

        syntax_error = _validate_input_syntax(input_content)

        if syntax_error:
            return syntax_error

        built_code = _build_python_code(input_content, input_variables)
        # Running the generated code 'built-code' in a separate environment and returs the output back to user
        try:
            f = io.StringIO()
            env = {}
            exec(built_code, env)
            built_code_output = env['mould_function']
            built_code_output(f)
            return f.getvalue().strip()
        except NameError:
            return "NameError : Not all variables used, are present in 'input_variables' dictionary"
        except SyntaxError:
            return "SyntaxError: variables (or) 'if' (or) 'for' is not correctly syntaxed"
        except TypeError:
            return "TypeError: Please check whether the variables used in 'for' are of the allowed datatypes"
    except:
        return "An error occurred, please check the syntax!"
