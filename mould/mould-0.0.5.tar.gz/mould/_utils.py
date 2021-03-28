from _constants import *

# Checks for syntax errors and returns the error text if there are any.


def _validate_input_syntax(input_content):
    # TODO - Implement better logic to capture all syntax issues

    if not input_content.count(IF_BLOCK_START) == input_content.count(IF_BLOCK_END) and input_content.count(FOR_BLOCK_START) == input_content.count(FOR_BLOCK_END):
        return "SyntaxError: please check 'if' or 'for' blocks"
    for every_line in input_content.split(LINE_BREAK):
        if not every_line.count(VAR_OPEN_MARKER) == every_line.count(VAR_CLOSE_MARKER):
            return "SyntaxError: please check '{{' and '}}'"
        if not every_line.count(IF_FOR_OPEN_MARKER) == every_line.count(IF_FOR_CLOSE_MARKER):
            return "SyntaxError: please check '{%' and '%}'"
    return ""


# Parses the lines present in input content where-ever a variable or variable expression is present

def _parse_the_variables(input_line):
    '''
    Description:
    This function parses the given line with variables and returns the variables and strings in comma separated format to put them directly to a print statement

    Parameters:
    input_line (string) : This string is supposed to have variables or variable expressions with or without other plain texts

    Returns: The plain text and variables / variable expressions are returned as a comma separated string which can be directly put into a print statement

    Example:

            $ _parse_the_variables("Hello  {{ world }}")
            "Hello",world
    '''

    output = []

    while len(input_line) != 0:
        if VAR_OPEN_MARKER in input_line:
            input_line = input_line.split(VAR_OPEN_MARKER, 1)
            if input_line[0] != "":
                output.append(STR_BLOCK_START + QUOTES +
                              input_line[0] + QUOTES + STR_BLOCK_END)

            input_line = input_line[1].strip().split(VAR_CLOSE_MARKER, 1)
            output.append(STR_BLOCK_START + input_line[0] + STR_BLOCK_END)

            if input_line[1] != "":
                input_line = input_line[1]
        else:
            if input_line[-1] != "":
                output.append(STR_BLOCK_START + QUOTES +
                              input_line + QUOTES + STR_BLOCK_END)
            break

    return "+".join(output)


def _build_python_code(input_content, variables):
    '''
    Description:
    This function builds executable python code with appropriate indentation so that the code can be run as such to render the user's input text.
    It processes plain lines, lines with if,else,elif,for blocks and lines with variables and variable expressions

    Parameters:
    input_content (string) : This is the user input, which is assumed to have multiple lines
    variables (dictionary) : This contains the list of variables and their values as key-value pairs

    Returns: Executable python code as a string

    Example:
            $sample_input = "
             This is where it all starts!!!
             Hello {{ text }} This is a wonderful day. My name is {{ name }}.
             "
            $sample_variables = {
                "text" : "World !"
                "name" : "Python"
                }
            $_build_python_code(sample_input, sample_variables)
            text = "World !"
            name = "Python"
            print("Hello",text,"This is a wonderful day. My name is",name)
    '''

    output_string = "def mould_function(f):" + LINE_BREAK
    indent = 4

    for key, value in variables.items():
        if type(value) != str:
            output_string += (indent*SPACE) + key + \
                ASSIGNMENT_SIGN + str(value) + LINE_BREAK
        else:
            output_string += (indent*SPACE) + key + ASSIGNMENT_SIGN + \
                QUOTES + str(value) + QUOTES + LINE_BREAK

    for every_line in input_content.split(LINE_BREAK):
        line = every_line.strip()

        # Checks for if,else,elif and for blocks and adds the relevant python code block to the output code

        if line.startswith(IF_FOR_OPEN_MARKER) and line.endswith(IF_FOR_CLOSE_MARKER) and not IF_BLOCK_END in line.split() and not FOR_BLOCK_END in line.split():
            line_split = line.split()
            if line_split[1] in ["else", "elif"]:
                indent -= 4
                output_string += (indent*SPACE) + \
                    SPACE.join(line_split[1:-1]) + SCOPING_COLON + LINE_BREAK
                indent += 4
            elif line_split[1] in ["if", "for"]:
                output_string += (indent*SPACE) + \
                    SPACE.join(line_split[1:-1]) + SCOPING_COLON + LINE_BREAK
                indent += 4

        # Checks for endif block to close the indentation generated for if block previously in the output code

        elif line.startswith(IF_FOR_OPEN_MARKER) and line.endswith(IF_FOR_CLOSE_MARKER) and (IF_BLOCK_END in line.split() or FOR_BLOCK_END in line.split()):
            indent -= 4

        # Adds the variable declaration statements and variable expression statements in output python code

        elif VAR_OPEN_MARKER in line:
            output_string += (indent * SPACE) + PRINT_BLOCK_START + \
                _parse_the_variables(line) + PRINT_BLOCK_END + LINE_BREAK

        # Checks for plain lines to be printed as such and add them to the output code

        elif VAR_OPEN_MARKER not in line and IF_FOR_OPEN_MARKER not in line:
            output_string += (indent*SPACE)+PRINT_BLOCK_START + QUOTES + \
                line + QUOTES + PRINT_BLOCK_END + LINE_BREAK

    return output_string
