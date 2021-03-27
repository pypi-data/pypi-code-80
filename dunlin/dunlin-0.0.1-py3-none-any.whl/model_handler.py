import configparser as cp
import numpy        as np
import pandas       as pd
from   pathlib      import Path

###############################################################################
#Non-Standard Imports
###############################################################################
try:
    import dunlin._utils_model.model_coder as coder
    import dunlin._utils_model.utils_ini   as uti
    import dunlin._utils_model.utils_model as utm
except Exception as e:
    if Path.cwd() == Path(__file__).parent:
        import _utils_model.model_coder as coder
        import _utils_model.utils_ini   as uti
        import _utils_model.utils_model as utm
    else:
        raise e

###############################################################################
#Globals
###############################################################################
display_settings = {'verbose' : False}

###############################################################################
#.ini Constructors
###############################################################################
def read_ini(filename, **kwargs):
    with open(filename, 'r') as file:
        return read_inicode(file.read(), **kwargs)
            
def read_inicode(inicode, **kwargs):
    '''
    Parses a string of code in .ini format. Note that Only the semicolon (';') 
    can be used to mark comments. Lines with the hash ('#') symbol will be read 
    and used as Python comments.

    Parameters
    ----------
    inicode : str
        A string of code in .ini format. Only the semicolon (';') can be used to 
        mark comments. Lines with the hash ('#') symbol will be read and used as 
        Python comments.

    Returns
    -------
    model_data : dict
        A dictionary of the data from the code.
    '''
    model_data = {}
    ini_args   = {'comment_prefixes':(';',), 'interpolation':cp.ExtendedInterpolation()}
    ini_args   = {**ini_args, **kwargs}
    config     = cp.ConfigParser(**ini_args)
    config.optionxform = str 
    config.read_string(inicode)
    
    for name in config.sections():
        if name[0] == '_' or name == kwargs.get('default_section', 'DEFAULT'):
            continue
        model_data[name] = parse_model(name, config)
    return model_data

def parse_model(name, config):
    '''
    Parses data indexed under name from a configparser exvect.
    
    :meta private:
    '''
    data = uti.parse_section(name, config)
    
    data['model'] = Model(**data['model'])
    model         = data['model']
    model_dict    = model.as_dict()
    
    # if 'exvs' in data:
    #     exvs              = data['exvs']
    #     exvs, exv_code    = coder.exvs2func(model_dict, exvs) 
    #     data['exvs']      = exvs
    #     data['exvs_code'] = exv_code
    #     model.exvs        = exvs
    #     model.exv_code    = exv_code 
    
    # if 'modify' in data:
    #     modify              = data['modify']
    #     model_func          = model.func
    #     modify, mod_code    = coder.modify2func(model_dict, modify, model_func)
    #     data['modify']      = modify
    #     data['modify_code'] = mod_code
    #     model.modify        = modify
        
    return data

###############################################################################
#Model Class
###############################################################################
class Model():
    ###############################################################################
    #Constructors
    ###############################################################################
    def __init__(self, name, states, params, inputs, equations=None, meta=None, tspan=None, int_args=None, exv_eqns=None, modify_eqns=None, solver_args=None, use_numba=True):

        if type(name) != str:
            raise TypeError('name argument must be a str.')
        if meta is not None and type(meta) != dict:
            raise TypeError('meta argument must be a dict.')
        
        #Get names of states, params and inputs
        state_names, init_vals  = utm.read_init(states)
        param_names, param_vals = utm.read_params(params)
        input_names, input_vals = utm.read_inputs(inputs)
        tspan_                  = utm.read_tspan(tspan)
        solver_args_            = solver_args if solver_args else {'method': 'LSODA'}
        
        utm.check_names(state_names, param_names, input_names)
        
        set_attr = super().__setattr__
        
        #Attributes assigned directly
        set_attr('name',        name)
        set_attr('states',      state_names)
        set_attr('params',      param_names)
        set_attr('inputs',      input_names)
        set_attr('meta',        meta)
        set_attr('solver_args', solver_args_)
        set_attr('tspan',       tspan_)
        set_attr('init_vals',   init_vals)
        set_attr('param_vals',  param_vals)
        set_attr('input_vals',  input_vals)
        set_attr('equations',   equations)
        set_attr('code',        None)
        set_attr('func',        None)
        set_attr('exvs',        None)
        set_attr('exv_code' ,   None)
        set_attr('modify',      None)
        
        #Function generation
        if equations:
            model_dict = self.as_dict()
            func, code = coder.model2func(model_dict, use_numba=use_numba)
            set_attr('code', code)
            set_attr('func', func)
        model_dict = self.as_dict()
        if exv_eqns:
            if self.equations:
                exvs, exv_code = coder.exvs2func(model_dict, exv_eqns)
                set_attr('exvs',     exvs)
                set_attr('exv_code', exv_code)
            else:
                raise Exception('Cannot create code for extra variables without model equations.')
        if modify_eqns:
            if self.equations:
                mod_func, mod_code = coder.modify2func(model_dict, modify_eqns, func)
                set_attr('modify',    mod_func)
                set_attr('mode_code', mod_code)
            else:
                raise Exception('Cannot create code for modifying variables without model equations.')
        
    ###############################################################################
    #Immutability
    ###############################################################################
    def __setattr__(self, attr, value):
        invalid_msg = 'Attempted to set "{}" attribute with an invalid value: {}'
        arg_msg     = 'The "{}" attribute for Model {} must have {} arguments: {}.'
        func_msg    = 'The "{}" attribute for Model "{}" must be a function.'
        dict_msg    = 'The "{}" attribute for Model {} must be a dict.'
        if attr == 'init_vals':
            states, value_ = utm.read_init(value)
            if set(states).difference(self.states):
                raise ValueError('Attempted to assign init_vals but names of states do not match those of model.')
            super().__setattr__(attr, value_[list(self.states)])
        elif attr == 'param_vals':
            names, value_ = utm.read_params(value)
            if set(names).difference(self.params):
                raise ValueError('Attempted to assign param_vals but names of params do not match those of model.')
            super().__setattr__(attr, value_[list(self.params)])
        elif attr == 'input_vals':
            names, value_ = utm.read_inputs(value)
            if set(names).difference(self.params):
                raise ValueError('Attempted to assign input_vals but names of inputs do not match those of model.')
            super().__setattr__(attr, value_[list(self.inputs)])
        elif attr == 'tspan':
            value_ = utm.read_tspan(value)
            super().__setattr__(attr, value_)
        elif attr == 'func':
            if value is None:
                pass
            elif not callable(value):
                raise TypeError(func_msg.format(attr, self.name))
            elif value.__code__.co_argcount != 3 and not self.inputs:
                raise ValueError(arg_msg.format(attr, self.name, 3, 't, y, p'))
            elif value.__code__.co_argcount != 4 and self.inputs:
                raise ValueError(arg_msg.format(attr, self.name, 4, 't, y, p, u'))
            else:
                raise ValueError(invalid_msg.format(attr, value))
            super().__setattr__(attr, value)
        elif attr == 'exvs':
            attr_ = 'function in the "exvs"'
            if value is None:
                pass
            if type(value) != dict:
                raise TypeError(dict_msg(attr, self.name))
            for k, v in value.items():
                if not callable(v):
                    raise TypeError(func_msg.format(attr_, self.name))
                elif v.__code__.co_argcount != 3 and not self.inputs:
                    raise ValueError(arg_msg.format(attr_, self.name, 3, 't, y, p'))
                elif v.__code__.co_argcount != 4 and self.inputs:
                    raise ValueError(arg_msg.format(attr_, self.name, 4, 't, y, p, u'))
            super().__setattr__(attr, value)
        elif attr == 'modify':
            if value is None:
                pass
            elif not callable(value):
                raise TypeError(func_msg.format(attr, self.name))
            elif value.__code__.co_argcount < 5 and not self.inputs:
                raise ValueError(arg_msg.format(attr, self.name, 5, 'model_func, init, params, scenario, segment'))
            elif value.__code__.co_argcount < 6 and self.inputs:
                print(attr, self.name, 6, 'model_func')
                raise ValueError(arg_msg.format(attr, self.name, 6, 'model_func, init, params, inputs, scenario, segment'))
            super().__setattr__(attr, value)
        elif attr in ['meta', 'solver_args']:
            super().__setattr__(attr, value)
        elif hasattr(self, attr):
            msg = "Model object's {} attribute is fixed.".format(attr)
            raise AttributeError(msg)
        else:
            msg = "Model object has no attribute called: {}".format(attr)
            raise AttributeError(msg)
            
    ###############################################################################
    #Export
    ###############################################################################
    def as_dict(self):
        model_dict = {'name'      : self.name,
                      'states'    : self.states,
                      'params'    : self.params,
                      'inputs'    : self.inputs,
                      'meta'      : self.meta,
                      'equations' : self.equations
                      }
        return model_dict
    
    def export_code(self, filename=''):
        filename_ = filename if filename else 'model_{}.py'.format(self.name)
        with open(filename_, 'w') as file:
            file.write(self.code)
    
    ###############################################################################
    #Printing
    ###############################################################################
    def __str__(self):
        global display_settings
        if display_settings['verbose']:
            d = self.as_dict()
            s = 'Model({})'.format(d)
            return s
        else:
            s = 'Model({})'.format(self.name)
            return s

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':    
    import _utils_model.integration as itg
    # #Read .ini
    # #Case 1: Basic arguments
    model = read_ini('_test/TestModel_1.ini')['model_1']['model']
    assert model.states == ('x', 's', 'h')
    assert model.params == ('ks', 'mu_max', 'synh', 'ys')
    assert model.inputs == ('b',) 
    
    #Case 2: With exv
    model = read_ini('_test/TestModel_2.ini')['model_1']['model']
    assert model.states == ('x', 's', 'h')
    assert model.params == ('ks', 'mu_max', 'synh', 'ys')
    assert model.inputs == ('b',)
    
    exvs = model.exvs#read_ini('_test/TestModel_2.ini')['model_1']['exvs']
    assert len(exvs) == 1
    
    #Test attributes related to integration   
    model    = read_ini('_test/TestModel_1.ini')['model_1']['model']
    tspan    = model.tspan
    assert len(tspan) == 2
    assert all( np.isclose(tspan[0], np.linspace(  0, 300, 31)) )
    assert all( np.isclose(tspan[1], np.linspace(300, 600, 31)) )
    
    init = model.init_vals
    y    = init.loc[0].values
    assert all(y == 1)
    
    params = model.param_vals
    p      = params.loc[0].values
    assert all(p == [20, 0.1, 1, 2])
    
    inputs = model.input_vals
    u      = inputs.loc[0].values
    u0     = u[0]
    assert all(u0 == [2])
    
    #Test model function
    t = 0
    f = model.func
    
    r = f(t, y, p, u0)
    assert all(r)
    
    #Test integration
    y_model, t_model = itg.piecewise_integrate(model.func, tspan, y, p, u, scenario=0)
    assert y_model.shape == (3, 62)
    
    #Test exv function
    model  = read_ini('_test/TestModel_2.ini')['model_1']['model']
    exvs   = model.exvs
    exv_1  = exvs['growth']
    
    t1 = t_model[:2]
    y1 = np.array([y, y+r]).T
    p1 = np.array([p, p]).T
    u1 = np.array([u0, u0]).T 
    
    xo1, yo1 = exv_1(t1, y1, p1, u1)
    assert all(xo1 == t_model[:2])
    assert np.isclose(yo1[0], r[0])
    
    
    
    
    