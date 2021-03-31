"""
This contains a number of useful functions used by other modules.
"""
import os
import platform
from lark.tree import Tree
from sca2d.scadclasses import Variable

def is_empty_arg(tree):
    """
    Checks if an argument is empty. This is needed becuse
    lark returns and empty arg tree when `foo()` is encountered.
    This function is trivial but makes code clearer.
    """
    return len(tree.children) == 0

def is_termination(tree_or_token):
    """
    Checks if the tree or token is a termination character. i.e ";".
    This is useful when deciding how to pass a module call scope as
    the module may be called with a scope following or terminated. It is
    Used for all module and control scopes as terminating them isntantly
    with a semicolon is always valid .scad even if it does not make sense
    to do so.
    """
    if isinstance(tree_or_token, Tree):
        return False
    return tree_or_token.type == 'TERMINATION'

def get_constituents_of_expr(expr):
    """
    Returns a list of the variables used and functions called in the input
    expression. Two lists are returned. For variables the list is of
    sca2d.scadclasses.Variable objects but for the function calls they are
    lark.tree.Tree as they will require further processing in the calling scope.
    """
    excluded_trees = ['let_expr','echo_func', 'list_comp_expr', 'assert_func_expr']
    if expr.data == 'function_call':
        return [], [expr], []
    if expr.data in ['let_expr', 'list_comp_expr', 'assert_func_expr']:
        return [], [], [expr]
    var_tokens = get_all_matching_tokens(expr, 'VARIABLE', exclude_trees=excluded_trees)
    func_trees = get_all_matching_subtrees(expr , 'function_call', exclude_trees=excluded_trees)
    lc_trees = get_all_matching_subtrees(expr , 'list_comp_expr', include_nested=False, exclude_trees=excluded_trees)
    let_expr_trees = get_all_matching_subtrees(expr , 'let_expr', include_nested=False, exclude_trees=excluded_trees)
    assert_exprs = get_all_matching_subtrees(expr , 'assert_func_expr', include_nested=False, exclude_trees=excluded_trees)
    complex_expressions = lc_trees + let_expr_trees + assert_exprs
    variables = [Variable(token) for token in var_tokens]
    return variables, func_trees, complex_expressions

def parse_assignment(assign_tree):
    """
    Spits and asignment (could be a kwarg or a control assignment)
    into the assinged variable and the expression.
    """
    assigned_var = Variable(assign_tree.children[0])
    expr = assign_tree.children[1]
    used_vars, used_functions, complex_expressions = get_constituents_of_expr(expr)
    return assigned_var, used_vars, used_functions, complex_expressions

def get_all_matching_subtrees(tree, tree_name, include_nested=True, exclude_trees=None):
    """
    Returns a list of all matching subtrees in the order they appear in the
    code. Trees match if Tree.data (i.e. the rule name in the .lark definion)
    matches the input "tree_name". If include nested then nested trees of the
    same type will be found.
    """
    if exclude_trees is not None:
        if tree.data in exclude_trees:
            return []

    subtrees = []
    for child in tree.children:
        if isinstance(child, Tree):
            if child.data == tree_name:
                subtrees.append(child)
                if not include_nested:
                    # Don't try to match subtrees if include_nested is false
                    continue
            subtrees += get_all_matching_subtrees(child,
                                                  tree_name,
                                                  include_nested=include_nested,
                                                  exclude_trees=exclude_trees)
    return subtrees

def get_all_matching_tokens(tree, token, exclude_trees=None):
    """
    Returns a list of all matching tokens in the order they appear in the
    code. Tokens match if Token. Type matches the input.
    Any tokens inside excluded tree types are not returned.
    """
    if exclude_trees is not None:
        if tree.data in exclude_trees:
            return []

    tokens = []
    for child in tree.children:
        if isinstance(child, Tree):
            tokens += get_all_matching_tokens(child, token, exclude_trees=exclude_trees)
        else:
            if child.type == token:
                tokens.append(child)
    return tokens

def get_all_tokens(tree):
    """
    Returns all tokens in a given lark Tree. Note that the tokens are the terminus or leaf
    of each branch of the tree, but not all trees terminate in tokens.
    """
    tokens = []
    for child in tree.children:
        if isinstance(child, Tree):
            tokens += get_all_tokens(child)
        else:
            tokens.append(child)
    return tokens

def library_path():
    """
    Returns the openscad librarypath
    """
    if platform.system() == 'Windows':
        return [r"C:\My Documents\OpenSCAD\libraries"]
    if platform.system() == 'Darwin':
        return ["/Documents/OpenSCAD/libraries"]
    return ["~/.local/share/OpenSCAD/libraries", "/usr/share/openscad/libraries"]

def locate_file(use_inc_statement):
    """
    This function locates the used/included files.
    """
    required_file = use_inc_statement.filename
    calling_file = use_inc_statement.calling_file
    if os.path.isabs(required_file):
        return required_file
    call_dir = os.path.dirname(calling_file)
    local_file =  os.path.normpath(os.path.join(call_dir, required_file))
    if os.path.exists(local_file):
        return local_file
    for lib_dir in library_path():
        library_file =  os.path.normpath(os.path.join(lib_dir, required_file))
        if os.path.exists(library_file):
            return library_file
    # If it cannot be found just return the original file.
    return required_file
