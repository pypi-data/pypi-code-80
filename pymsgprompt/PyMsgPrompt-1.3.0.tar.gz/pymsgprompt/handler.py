import sys

def default_on_error(question, choices, default, error):
    '''
    A default callback after failed validation of the answer
    This funtion retuns a boolean value, True or False, in case it returns True,
    the question will be re asked!
    '''
    sys.stderr.write('%s\n'%error)
    return False

def default_on_success(question, actual_answer, original_answer):
    '''
    A default callback after successful validation of the answer
    This function can return either the actual answer or the original answer,
    given by the user.
    '''
    sys.stdout.write('%s\n'%actual_answer)
    return actual_answer