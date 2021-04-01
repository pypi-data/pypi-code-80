####
## Lark imports and re-defining Lark transformers
####

from functools import wraps
import random
from inspect import getmembers, getmro

import lark
from lark import Lark
from lark import utils
from lark import Tree
from lark.exceptions import VisitError, GrammarError
from lark import Token

import json

class Discard(Exception):
    """When raising the Discard exception in a transformer callback,
    that node is discarded and won't appear in the parent.
    """
    pass

# Transformers

class _Decoratable:
    "Provides support for decorating methods with @v_args"

    @classmethod
    def _apply_decorator(cls, decorator, **kwargs):
        mro = getmro(cls)
        assert mro[0] is cls
        libmembers = {name for _cls in mro[1:] for name, _ in getmembers(_cls)}
        for name, value in getmembers(cls):

            # Make sure the function isn't inherited (unless it's overwritten)
            if name.startswith('_') or (name in libmembers and name not in cls.__dict__):
                continue
            if not callable(value):
                continue

            # Skip if v_args already applied (at the function level)
            if hasattr(cls.__dict__[name], 'vargs_applied') or hasattr(value, 'vargs_applied'):
                continue

            static = isinstance(cls.__dict__[name], (staticmethod, classmethod))
            setattr(cls, name, decorator(value, static=static, **kwargs))
        return cls

    def __class_getitem__(cls, _):
        return cls

    
class TreeTransformer(_Decoratable):
    """Identical to the Lark Transformer class, but passes trees into visitor functions rather than the tree's children.
    """
    __visit_tokens__ = True   # For backwards compatibility

    def __init__(self,  visit_tokens=True):
        self.__visit_tokens__ = visit_tokens

    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = new_children if new_children is not None else tree.children
        tree.children = new_children 
        # change: added above line since passing in tree directly means updating its children separately
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree.data, children, tree.meta)
        else:
            try:
                wrapper = getattr(f, 'visit_wrapper', None)
                if wrapper is not None:
                    return f.visit_wrapper(f, tree.data, tree, tree.meta) #change: children -> tree
                else:
                    return f(tree) #change: children -> tree
            except (GrammarError, Discard):
                raise
            except Exception as e:
                raise VisitError(tree.data, tree, e)

    def _call_userfunc_token(self, token):
        try:
            f = getattr(self, token.type)
        except AttributeError:
            return self.__default_token__(token)
        else:
            try:
                return f(token)
            except (GrammarError, Discard):
                raise
            except Exception as e:
                raise VisitError(token.type, token, e)


    def _transform_children(self, children):
        for c in children:
            try:
                if isinstance(c, Tree):
                    yield self._transform_tree(c)
                elif self.__visit_tokens__ and isinstance(c, Token):
                    yield self._call_userfunc_token(c)
                else:
                    yield c
            except Discard:
                pass

    def _transform_tree(self, tree):
        children = list(self._transform_children(tree.children))
        return self._call_userfunc(tree, children)

    def transform(self, tree):
        return self._transform_tree(tree)

    def __mul__(self, other):
        return TransformerChain(self, other)

    def __default__(self, data, children, meta):
        """Default operation on tree (for override)
        Function that is called on if a function with a corresponding name has not been found.
        Defaults to reconstruct the Tree.
        """
        return Tree(data, children, meta)

    def __default_token__(self, token):
        """Default operation on token (for override)
        Function that is called on if a function with a corresponding name has not been found.
        Defaults to just return the argument.
        """
        return token

####
## Grammar for SQL parsing
####

# adding i after a string indicates case-insensitivity
sql_parser = Lark(r"""
select: "select"i (fields | functionfields) "from"i table join? where? groupby? ";"?
join: ("inner"i)? "join"i table "on"i tablefield "=" tablefield
where: "where"i field operator constraint
groupby: "group by"i fields
functionfields: ((function "(" field ")") | field) ("," ((function "(" field ")") | field))*
fields: field ("," field)*

constraint: ESCAPED_STRING | ESCAPED_STRING_SING | INT | DECIMAL
table: VAR ("as"i VAR)?
field: VAR ("as"i VAR)? | tablefield | allfields
function: VAR 
allfields: "*"
operator: "=" -> eq
| ">" -> gt
| "<" -> lt
| "<=" -> leq
| ">=" -> geq
| "!=" -> neq

tablefield: table "." field

// copied directly from lark but with single-quote option added
ESCAPED_STRING : "\"" _STRING_ESC_INNER "\""
ESCAPED_STRING_SING: "'" _STRING_ESC_INNER "'"

%import common.WS
%import common.CNAME -> VAR
%import common.INT
%import common.DECIMAL
%import common._STRING_ESC_INNER
%ignore WS
""", start='select', propagate_positions=True)

# _STRING_INNER: /.*?/
# _STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/

# ESCAPED_STRING : "\"" _STRING_ESC_INNER "\""

####
## Tree transform helper functions
####

# transfer the metadata about original text position from one tree to another
def transfer_meta(metaless, metaful):
    metaless.meta.column = metaful.column if metaful.column is not None else -1
    metaless.meta.end_column = metaful.end_column if metaful.end_column is not None else -1

# transfer the metadata about original text position from a tree to a token
# (slightly different syntax)
def transfer_meta_tok(metaless, metaful):
    if hasattr(metaful.meta, 'column'):
        metaless.column = metaful.column
        metaless.end_column = metaful.end_column
    else:
        metaless.column = -1
        metaless.end_column = -1

# create a token with the specified name and text, which has `metaful`'s metadata
def create_and_transfer(token_name, token_text, metaful):
    result = Token(token_name, token_text)
    transfer_meta_tok(result, metaful)

    # if the tree stores an or option, preserve what that option was
    if hasattr(metaful, 'or_text'):
        result.pos_in_stream = True
        result.end_pos = metaful.or_text
    else:
        result.pos_in_stream = False

    return result

# check if any of the direct children are part of an or node, and if so,
# set the tree to storing their position
# requires: only one or option in direct children (should always be the case
# if the tree is not of type `or_node`, which does not call this)
def check_or_pos(tree):
    for child in tree.children:
        if hasattr(child, 'pos_in_stream') and child.pos_in_stream == True:
            tree.or_text = child.end_pos
        elif hasattr(child, 'or_text'):
            tree.or_text = child.or_text

# Rearrange a Tree's nodes. Takes in a Tree's type and children and a list of integers,
# e.g. [1, 0, 2], and returns a new Tree such that the ith node in the original Tree is at 
# list.index(i) in the new Tree. Requires that list.sort() = range(len(list)) = len(Tree.children).
def rearrange_nodes(tree_type, children, new_indices):
    if not(sorted(new_indices) == list(range(len(new_indices))) \
         and len(new_indices) == len(children)):
        raise ValueError("The input list of new indices is not formatted correctly.")
        
    return Tree(tree_type, [children[i] for i in new_indices])

# Swap two nodes of a Tree. Requires that the two nodes given are both < len(Tree.children).
def swap_nodes(tree_type, children, node1, node2):
    if max((node1, node2)) >= len(children):
        raise ValueError("The given nodes are not in the Tree (it is too small).")
    
    new_indices = list(range(len(children)))
    new_indices[node1], new_indices[node2] = new_indices[node2], new_indices[node1]
    return rearrange_nodes(tree_type, children, new_indices)

# Returns True if a Tree contains a node of a given type and False otherwise.
# recurse = False only looks at top-level children; recurse = True looks at all levels
def contains(tree_type, children, recurse=False):
    for child in children:
        if isinstance(child, lark.tree.Tree):
            if child.data == tree_type:
                return True
            if recurse and contains(tree_type, child.children, recurse=True):
                return True
        elif isinstance(child, lark.lexer.Token):
            if child.type == tree_type:
                return True
    return False

# Returns the sub-tree within children which has the given type.
# Requires that contains(branch_type, children, recurse=True) is True. O
# If recurse is True, only returns the first such sub-tree using depth-first search.
def get_branch(branch_type, children, recurse=False):
    if not contains(branch_type, children, recurse=True):
        raise ValueError("The tree nodes given do not contain this branch type.")
    
    for child in children:
        if isinstance(child, lark.tree.Tree):
            if child.data == branch_type:
                return child
            if recurse and contains(branch_type, child.children, recurse=True):
                return get_branch(branch_type, child.children)


# Same requirements as get_branch. Returns a list of all sub-trees with the given type,
# excluding those already contained within sub-trees of that type.
def get_all_branch(branch_type, children, result=None):
    if not contains(branch_type, children, recurse=True):
        if result is None:
            # throw an error on the first call to alert the user
            raise ValueError("The tree nodes given do not contain this branch type.")
        else:
            return result
    
    if result is None: result = []
    for child in children:
        if isinstance(child, lark.tree.Tree):
            if child.data == branch_type:
                result.append(child)
            elif contains(branch_type, children, recurse=True):
                result = get_all_branch(branch_type, child.children, result)
    return result

    

# Same requirements as get_branch. 
# Returns children with the first instance of the given branch deleted.           
def remove_branch(branch_type, children):            
    if not contains(branch_type, children, recurse=True):
        raise ValueError("The tree nodes given do not contain this branch type.")
        
    for i, child in enumerate(children):
        if isinstance(child, lark.tree.Tree):
            if child.data == branch_type:
                return children[0:i] + children[i+1:]
            if contains(branch_type, child.children, recurse=True):
                return children[0:i] + [Tree(child.data, remove_branch(branch_type, child.children))] + children[i+1:]

# Same requirements as get_branch. 
# Returns children with all instances of the given branch deleted.    
def remove_all_branch(branch_type, children, recurse=False):
    if not contains(branch_type, children, recurse=True):
        if not recurse:
            # throw an error on the first call to alert the user
            raise ValueError("The tree nodes given do not contain this branch type.")
        # on recursive calls, if not contains, we're done, so return children
        return children

    for i, child in enumerate(children):
        if isinstance(child, lark.tree.Tree):
            if child.data == branch_type:
                return remove_all_branch(branch_type, children[0:i], True) + \
                        remove_all_branch(branch_type, children[i+1:], True)
            if contains(branch_type, child.children, recurse=True):
                new_tree = Tree(child.data, remove_all_branch(branch_type, child.children))
                
                new_tree.meta.column = child.column
                new_tree.meta.end_column = child.end_column
    
                return remove_all_branch(branch_type, children[0:i], True) + \
                        [new_tree] + \
                        remove_all_branch(branch_type, children[i+1:], True)

functions = {'sum': 'sum', 'avg': 'mean', 'count': 'count', 'min': 'min', 'max':'max'}

# helper functions to create a particular type of string_wrap tree
def quotation_wrap(child):
    result = Tree('string_wrap', [child])
    result.wrap_char = ['\'', '\'']
    return result

def bracket_wrap(child):
    result = Tree('string_wrap', [child])
    result.wrap_char = ['[', ']']
    return result

def paren_wrap(child):
    result = Tree('string_wrap', [child])
    result.wrap_char = ['(', ')']
    return result

# helper function for a command: takes in a function tree,
# returns the tree equivalent of df = df[function]
def make_command(function_tree, table_name='df'):
    result = Tree('assign', [table_name, Tree('command', [table_name, function_tree])])
    #transfer_meta(result, function_tree)
    return result


####
## SQL-to-Pandas tree transformer
####

class SqlToPandasTransformer(TreeTransformer):
    def select(self, select):
        # children are functionfields|fields|all, table, join?, where?, groupby?
        # rearrange into table, table2+join?, where?, groupby?, fields, as? (from fields)

        children = select.children
        final_order = ('table', 'table2', 'join', 'where', 'groupby', 'function', 'fields', 'as')
        final_nodes = {tree_name: None for tree_name in final_order}
        
        ## Make table child (directly from original)
        table = get_branch('table', children)
        table_name = 'df'
        if len(table.children) > 1:
            # table already has a name (table AS name)
            table_name = table.children[1].lower()

        final_nodes['table'] = Tree('assign', [table_name, table])
        transfer_meta(final_nodes['table'], table)

        ## Make as child (by removing any 'as' children from their fields 
        ## and grouping them together)
        if contains('as-node', children, recurse=True):
            as_children = get_all_branch('as-node', children)
            children = remove_all_branch('as-node', children)

            as_enhanced = []
            for child in as_children:
                # pairs (old_name, new_name) gets set to (old_name : new_name ,)
                as_enhanced.append(child.children[0])
                as_enhanced.append(':')
                as_enhanced.append(child.children[1])
                as_enhanced.append(',')
            as_tree = Tree('string_wrap', as_enhanced)
            as_tree.wrap_char = ['.rename(columns={', '})']

            # just transfer the meta for the first as command (for now)
            final_as_tree = make_command(as_tree, table_name)
            final_as_tree.meta.column = as_children[0].meta.column
            final_as_tree.meta.end_column = as_children[0].meta.end_column
            final_nodes['as'] = final_as_tree
        
        ## Pull out function (for use in groupby later)
        fields_children = children[0].children
        
        if contains('functionfields', children, recurse=False) and \
            contains('function', children, recurse=True):
                function = get_branch('function', children, recurse=True)
                function_name = functions[function.children[0].value.lower()]
                
                funct_opt1 = Tree('string_wrap', [function_name])
                funct_opt2 = Tree('string_wrap', [quotation_wrap(function_name)])
                
                if function_name != 'count':
                    if contains('groupby', children, recurse=False):
                        # function will come after grouping, at which point the
                        # index will be out of whack
                        funct_opt1.wrap_char = ['.', '().reset_index()']
                        funct_opt2.wrap_char = ['.agg(', ').reset_index()']
                    else:
                        funct_opt1.wrap_char = ['.', '()']
                        funct_opt2.wrap_char = ['.agg(', ')']
                else: 
                    # SQL count assumes all fields have the same number and only counts one;
                    # Pandas counts each one separately, so just count the first Pandas field
                    funct_opt1.wrap_char = ['.iloc[0].', '()']
                    funct_opt2.wrap_char = ['.iloc[0].agg(', ')']

                funct_or_tree = Tree('or_node', [make_command(Tree('or_opt', [funct_opt1]), table_name), make_command(Tree('or_opt', [funct_opt2]), table_name)])
                funct_or_tree.probabilities = [80, 20]
                funct_or_tree.info = ".agg() is typically used to aggregate multiple functions, but it can also take just one input."
                funct_or_tree.concept = {'funct-call': ['normal', 'aggregate']}

                final_nodes['function'] = funct_or_tree
                transfer_meta(final_nodes['function'], function)
                
                # remove function from fields
                fields_children = [child for child in children[0].children if child != function]
        
        ## Make field child
        if contains('functionfields', children, recurse=False) or \
            contains('fields', children, recurse=False):
            if len(fields_children) == 1 and fields_children[0] == Tree('allfields', []):
                final_nodes['fields'] = None # don't select out any fields
                
            else:
                # we only want to store the fields, so if any children are tablefields, let's clear the table
                simple_children = []
                for child in fields_children: # should be either 'field' or 'tablefield' Tree
                    if child.data == 'field':
                        simple_children.append(child)
                    else:
                        # tablefield is table.field, we want to change it to field_table (pandas' column syntax)
                        #TODO AAAAAA no we don't -- well, only sometimes - make this an or node
                        field = child.children[1]
                        # field's child is a quotation-wrap whose child is the actual text
                        field_name = field.children[0].children[0]
                        field.children[0].children[0] = Token('VAR', field_name)
                        simple_children.append(field)

                fields_tree = bracket_wrap(bracket_wrap(Tree('fields', simple_children)))

                if len(simple_children) == 1:
                    # can use [] instead of [[]] with one-field requests
                    fields_tree2 = bracket_wrap(Tree('fields', simple_children))
                    fields_tree = Tree('or_node', [make_command(Tree('or_opt', [fields_tree]), table_name), make_command(Tree('or_opt', [fields_tree2]), table_name)])
                    fields_tree.probabilities = [30, 70]
                    fields_tree.info = "With a single field, we can use a list (like we do with multiple fields) or just put the field."
                    fields_tree.concept = {'indexing': ['normal', 'single-bracket']}

                    final_nodes['fields'] = fields_tree
                else:
                    final_nodes['fields'] = make_command(fields_tree, table_name)

                transfer_meta(final_nodes['fields'], children[0])
        
        ## Make groupby child
        if contains('groupby', children, recurse=False):
            group_field = children[-1]
            if contains('tablefield', children[-1].children, recurse=True):
                # we always merge before grouping, so the table isn't relevant anymore - just take the field
                tablefield = get_branch('tablefield', children[-1].children, recurse=True)
                group_field = tablefield.children[1]
            
            # add pandas groupby syntax around the field
            groupby_tree = Tree('string_wrap', [group_field])
            if final_nodes['function'] is None:
                groupby_tree.wrap_char = ['.groupby(', ').first().reset_index()']
                groupby_tree = make_command(groupby_tree, table_name)
                #TODO: this is very bad
            else:
                groupby_tree.wrap_char = ['.groupby(', ')']
                # incorporate the function into the command
                groupby_opt1 = Tree('groupby', [groupby_tree, Tree('or_opt', [funct_opt1])])
                groupby_opt2 = Tree('groupby', [groupby_tree, Tree('or_opt', [funct_opt2])])

                groupby_tree = Tree('or_node', [make_command(groupby_opt1, table_name), make_command(groupby_opt2, table_name)])
                groupby_tree.info = ".agg() is typically used to aggregate multiple functions, but it can also take just one input."
                groupby_tree.concept = {'funct-call': ['normal', 'aggregate']}
                groupby_tree.probabilities = [80, 20]

                final_nodes['function'] = None
                
            final_nodes['groupby'] = groupby_tree
            transfer_meta(final_nodes['groupby'], get_branch('groupby', children))
            
        ## Make join child
        if contains('join', children, recurse=False):
            join = get_branch('join', children)
            
            # join's children are table to be joined on, list of two columns to join
            table2 = join.children[0]
            table_name2 = 'df2'
            if len(table2.children) > 1:
                # table already has a name (table AS name)
                table_name2 = table2.children[1].lower()

            final_nodes['table2'] = Tree('assign', [table_name2, table2])
            transfer_meta(final_nodes['table2'], table2)
            
            #TODO: left and right might be swapped, have to figure out which is which using
            # table names (which is children[0])
            left = join.children[1].children[1]
            right = join.children[2].children[1]
            left_tree = Tree('string_wrap', [left])
            left_tree.wrap_char = [', left_on=', ',']
            right_tree = Tree('string_wrap', [right])
            right_tree.wrap_char = ['right_on=', '']
            suffixes = ', suffixes=(\'_' + table_name + '\',\'_' + table_name2 + '\'))'

            merge_tree = Tree('string_wrap', [table_name2, left_tree, right_tree])
            merge_tree.wrap_char = ['.merge(', suffixes]

            pd_join = make_command(merge_tree, table_name)
            final_nodes['join'] = pd_join
            transfer_meta(final_nodes['join'], join)
        
        ## Make where child
        if contains('where', children, recurse=False):
            # where's children are field, operator, constraint;
            # we want a syntax like [table['field' operator constraint]]
            
            where = get_branch('where', children)
            
            field = where.children[0]
            if field.data == 'tablefield': # we have a specific table to refer to
                # tablefield is [table, field]
                wheretable = field.children[0]
                field = bracket_wrap(field.children[1])
            else:
                # assume table is our main one
                wheretable = table_name
                field = bracket_wrap(where.children[0])
                
            where.children = [wheretable, field, where.children[1], where.children[2]]
            where_tree = bracket_wrap(where)
            final_nodes['where'] = make_command(where_tree, table_name)
            transfer_meta(final_nodes['where'], where)
        
        ## Construct final tree (starting with the last step, the evaluation)
        final_tree = Tree('evaluate', [table_name])
        for node in final_order[::-1]:
            # go in reverse order, skpping the last one (that we already used)
            if final_nodes[node] is not None:
                final_tree = Tree('sequence', [final_nodes[node], final_tree])
                
        return final_tree

    def fields(self, fields):
        fields2 = Tree('fields', fields.children)
        transfer_meta(fields2, fields)
        return fields2
    
    def field(self, field):
        if isinstance(field.children[0], lark.tree.Tree) and \
            field.children[0].data == 'tablefield':
            # original command was for a table.field (0th and 1st child of tablefield respectively)
            return Tree('tablefield', [field.children[0].children[0], field.children[0].children[1]])
        elif len(field.children) == 1:
            # no renaming occurring
            if field.children[0] == Tree('allfields', []):
                return Tree('allfields', [])
            
            new_field = Tree('field', [quotation_wrap(field.children[0])]) 
            transfer_meta(new_field, field)
            return new_field
        else:
            old_name = quotation_wrap(field.children[0])
            new_name = quotation_wrap(field.children[1])
            
            as_tree = Tree('as-node', [old_name, new_name])
            transfer_meta(as_tree, field.children[1])
            new_field = Tree('field', [old_name, as_tree])
            transfer_meta(new_field, field)
            return new_field


####
## Pandas unparser
####

class PandasUnparser(TreeTransformer):
    def sequence(self, tree):
        # left child is a command, 
        # right child is either a command or another sequence
        result = []
        result.append(tree.children[0])
        if type(tree.children[1]) == list: 
            # since we go leaf-up, this means right child is a smaller already-unparsed sequence list that we'll absorb here
            result.extend(tree.children[1])
        else:
            result.append(tree.children[1])
        return result
    
    def assign(self, tree):
        # left child is dataframe to set equal to an expression
        # right child is the expression, which could also be multiple options
        check_or_pos(tree)
        return create_and_transfer('assign', tree.children[0] + ' = ' + tree.children[1], tree)

    def evaluate(self, tree):
        # child is the name of a dataframe to be evaluted
        check_or_pos(tree)
        return create_and_transfer('evaluate', tree.children[0], tree)
    
    def command(self, tree):
        # left child is dataframe on which to evaluate an expression,
        # right child is expression to call on it
        check_or_pos(tree)
        return create_and_transfer('command', ''.join(tree.children), tree)
    
    def fields(self, tree):
        # children are variable names
        check_or_pos(tree)
        return create_and_transfer('fields', ','.join(tree.children), tree)
    
    def table(self, tree):
        # child is a dataframe's name
        check_or_pos(tree)
        return create_and_transfer('table', tree.children[0].lower(), tree)
    
    def where(self, tree):
        # children are table, field, eq, constraint (e.g. grades[grade] > 80)
        eqs = {'eq': '==', 'gt': '>', 'lt': '<', 'leq': '<=', 'geq': '>=', 'neq': '!='}
        tree.children[2] = eqs[tree.children[2].data]
        check_or_pos(tree)
        return create_and_transfer('where', ''.join(tree.children), tree)
    
    def allfields(self, none):
        # no children - started with a '*', so keep whole dataframe/don't select any fields
        return create_and_transfer('allfields', '', none)
    
    def field(self, tree):
        # child is the name of one field
        check_or_pos(tree)
        return create_and_transfer('field', tree.children[0].lower(), tree)
    
    def constraint(self, tree):
        # child is a constraint for a where statement (currently only supports numbers)
        check_or_pos(tree)
        return create_and_transfer('constraint', tree.children[0].value, tree)

    def groupby(self, tree):
        # children are the parts of a groupby command
        if isinstance(tree, str) or isinstance(tree, lark.lexer.Token): #TODO this is bad
            return tree
        check_or_pos(tree)
        return create_and_transfer('groupby', ''.join(tree.children), tree)
    
    def as_node(self, tree):
        # children are the parts of a rename command
        check_or_pos(tree)
        return create_and_transfer('as_node', ''.join(tree.children), tree)
    
    def function(self, tree):
        check_or_pos(tree)
        return create_and_transfer('function', ''.join(tree.children), tree)
    
    def or_opt(self, tree):
        # child is a token that is an or option; we want to keep track of it
        # so we know what to highlight later

        if type(tree.children[0]) == str:
            result = Token('or_opt', tree.children[0])
        else: # already is Token
            result = tree.children[0]

        result.pos_in_stream = True
        result.end_pos = tree.children[0]
        return result

    def or_node(self, tree):
        # tree's children as a list of `assign`s which can each work as a translation;
        # tree also keeps track of information about the concept and info behind each choice
        # move this information into a json/dict format for UI formatting

        for child in tree.children:
            # right now, every command that's part of an or node stores the specific subpart that represents the 'or'
            # in end_pos, and has pos_in_stream set to True.
            # we want to record the start and end indices of that subpart so we can highlight it later
            if hasattr(child, 'pos_in_stream') and child.pos_in_stream == True:
                child.pos_in_stream = child.index(child.end_pos)
                child.end_pos = child.pos_in_stream + len(child.end_pos)
            else: # not part of an or node, no highlighting
                child.pos_in_stream = -1
                child.end_pos = -1

        main_concept = next(iter(tree.concept)) # tree.concept is a one-key dict
        options = {tree.concept[main_concept][i]: (tree.children[i], tree.children[i].pos_in_stream, tree.children[i].end_pos) \
            for i in range(len(tree.children))}
        choices = {'options': options, 'tooltip': tree.info, 'concept': main_concept, \
            'meta': (tree.column if tree.column is not None else -1, # meta stores the part of the SQL command this links to
                    tree.end_column if tree.end_column is not None else -1)}
        return choices
    
    def string_wrap(self, tree):
        # child is a string that should be wrapped in some particular other string
        check_or_pos(tree)
        return tree.wrap_char[0] + ''.join(tree.children) + tree.wrap_char[1]
    
    def tablefield(self, tree):
        # children are table name and field name
        check_or_pos(tree)
        return tree.children[0] + '.' + tree.children[1]

# .sample_user works in notebook, sample_user (no dot prefix) works in testing - why? TODO
from .sample_user import *

def make_choice(options, main_concept, function):
    # given a tree with a list of options for the same command,
    # either choose the user's most or least known version (depending on `function`)
    # when user knowledge is not 1.0 for the item chosen,
    # modifies user to increase knowledge by 0.1 for item chosen

    #main_concept = next(iter(concept))
    if main_concept not in user:
        raise KeyError("This concept is not known to the user.")

    knowledge = user[main_concept]
    choice = function(knowledge, key=lambda key: knowledge[key])
    if choice not in options:
        raise KeyError("There is a mismatch between user and tree listing of this concept.")

    if user[main_concept][choice] < 1:
        user[main_concept][choice] += 0.1

    return (choice, options[choice])
    

####
## Actual translator
####

def translate(sql_command, verbose = False):
    sql_tree = sql_parser.parse(sql_command)
    if verbose: print("SQL command tree:", sql_tree.children,'\n')
    pandas_tree = SqlToPandasTransformer().transform(sql_tree)
    if verbose: print("Pandas command tree:", pandas_tree.children, '\n')
    pandas_command = PandasUnparser().transform(pandas_tree)
    if verbose: print("Final command:", pandas_command, '\n\n')
    return pandas_command

def translate_simple(string):
    return string.upper()

def translate_test(sql_command, verbose = False):
    pandas_command = translate(sql_command, verbose)

    # filter out or nodes, only want to test first choice
    # (probabilistically we will test all options over time)
    new_command = []
    for item in pandas_command:
        if isinstance(item, lark.lexer.Token):
            new_command.append(item)
        elif isinstance(item, dict):
            #TODO how best to run originally probabilistic tests?
            #TODO this literally does not work
            choice = random.choice(item['options'])
            new_command.append(choice)
    return tuple(str(i) for i in new_command)

from lark import UnexpectedCharacters
def translate_real(sql_command):
    try:
        pandas_command = translate(sql_command, verbose=False)
    except UnexpectedCharacters as e:
        error_msg = str(e).split("'")
        error_pos = error_msg[2].split('\n')[0].split(' ')
 
        raise KeyError("Sorry! Either you have entered a non-SQL keyword or " + \
            "this translator does not currently support a SQL keyword you entered. " + \
            f"The issue starts at character {error_msg[1]}, position {error_pos[-1]}. " + \
            "Please feel free to try again.")
        return


    # unpack any recursive or nodes - we want to keep only the top-level ones
    # unpacked_command = []
    # for item in pandas_command:
    #     if isinstance(item, lark.lexer.Token):
    #         unpacked_command.append(item)
    #     elif isinstance(item, dict):
    #         # check each item in the dict to see if any of them need unpacking
    #         options = item['options'] # options is a concept_name : translation_string dict
    #         new_options = {k:unpack(options[k]) for k in options}
    #         new_item = {'options': new_options, 'tooltip': item['tooltip'], \
    #             'concept': item['concept'], 'meta': item['meta']}
    #         unpacked_command.append(new_item)

    # switch into json format
    expanded_command = []
    or_function = min # start by showing what user knows least

    for item in pandas_command:
        json_item = {}
        if isinstance(item, lark.lexer.Token):
            json_item['first_choice'] = item

        elif isinstance(item, dict):
            # or node: access user info to decide what to display
            chosen_concept, chosen_command = make_choice(item['options'], item['concept'], or_function)
            chosen_command, or_start, or_end = chosen_command

            chosen_command.pos_in_stream = or_start
            chosen_command.end_pos = or_end
            chosen_command.column = item['meta'][0]
            chosen_command.end_column = item['meta'][1]

            json_item['first_choice'] = chosen_command
            or_function = max # having pushed user's knowledge once, stick to most-known concepts afterwards

            json_item['other_options'] = []
            for alt in item['options']:
                if alt == chosen_concept:
                    continue 
                opt, start, end = item['options'][alt]
                opt.pos_in_stream = start
                opt.end_pos = end
                json_item['other_options'].append(opt)

            #json_item['other_options'] = [item['options'][i] for i in item['options'] if i != chosen_concept]
            json_item['tooltip'] = item['tooltip']
        expanded_command.append(json_item)
    
    return expanded_command

def unpack(item):
    if isinstance(item, lark.lexer.Token):
        return item
    pass