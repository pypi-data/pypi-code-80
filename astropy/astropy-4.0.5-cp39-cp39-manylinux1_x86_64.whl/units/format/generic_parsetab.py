# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

# This file was automatically generated from ply. To re-generate this file,
# remove it from this folder, then build astropy and run the tests in-place:
#
#   python setup.py build_ext --inplace
#   pytest astropy/units
#
# You can then commit the changes to this file.


# generic_parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'DOUBLE_STAR STAR PERIOD SOLIDUS CARET OPEN_PAREN CLOSE_PAREN FUNCNAME UNIT SIGN UINT UFLOAT\n            main : product_of_units\n                 | factor product_of_units\n                 | factor product product_of_units\n                 | division_product_of_units\n                 | factor division_product_of_units\n                 | factor product division_product_of_units\n                 | inverse_unit\n                 | factor inverse_unit\n                 | factor product inverse_unit\n                 | factor\n            \n            division_product_of_units : division_product_of_units division product_of_units\n                                      | product_of_units\n            \n            inverse_unit : division unit_expression\n            \n            factor : factor_fits\n                   | factor_float\n                   | factor_int\n            \n            factor_float : signed_float\n                         | signed_float UINT signed_int\n                         | signed_float UINT power numeric_power\n            \n            factor_int : UINT\n                       | UINT signed_int\n                       | UINT power numeric_power\n                       | UINT UINT signed_int\n                       | UINT UINT power numeric_power\n            \n            factor_fits : UINT power OPEN_PAREN signed_int CLOSE_PAREN\n                        | UINT power OPEN_PAREN UINT CLOSE_PAREN\n                        | UINT power signed_int\n                        | UINT power UINT\n                        | UINT SIGN UINT\n                        | UINT OPEN_PAREN signed_int CLOSE_PAREN\n            \n            product_of_units : unit_expression product product_of_units\n                             | unit_expression product_of_units\n                             | unit_expression\n            \n            unit_expression : function\n                            | unit_with_power\n                            | OPEN_PAREN product_of_units CLOSE_PAREN\n            \n            unit_with_power : UNIT power numeric_power\n                            | UNIT numeric_power\n                            | UNIT\n            \n            numeric_power : sign UINT\n                          | OPEN_PAREN paren_expr CLOSE_PAREN\n            \n            paren_expr : sign UINT\n                       | signed_float\n                       | frac\n            \n            frac : sign UINT division sign UINT\n            \n            sign : SIGN\n                 |\n            \n            product : STAR\n                    | PERIOD\n            \n            division : SOLIDUS\n            \n            power : DOUBLE_STAR\n                  | CARET\n            \n            signed_int : SIGN UINT\n            \n            signed_float : sign UINT\n                         | sign UFLOAT\n            \n            function_name : FUNCNAME\n            \n            function : function_name OPEN_PAREN main CLOSE_PAREN\n            '
    
_lr_action_items = {'OPEN_PAREN':([0,3,6,7,8,9,10,11,12,13,14,16,17,18,19,21,23,26,27,28,29,34,36,38,39,41,42,43,46,47,53,54,55,57,59,60,63,64,65,67,68,73,74,77,78,79,80,82,83,],[13,13,13,-14,-15,-16,13,-34,-35,13,35,-17,-50,41,45,-56,13,-48,-49,13,13,58,-21,-51,-52,13,45,-38,-54,-55,-36,-23,45,-28,-27,-22,-29,-18,45,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'UINT':([0,14,15,16,17,19,20,34,37,38,39,41,42,44,45,46,47,55,56,58,61,65,70,84,85,],[14,33,-46,40,-50,-47,46,57,63,-51,-52,14,-47,68,-47,-54,-55,-47,74,75,74,-47,81,-47,86,]),'SOLIDUS':([0,2,3,4,6,7,8,9,11,12,14,16,19,22,23,24,26,27,30,36,41,43,46,47,48,49,51,52,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,81,82,83,],[17,-12,17,17,-33,-14,-15,-16,-34,-35,-20,-17,-39,-12,17,17,-48,-49,-32,-21,17,-38,-54,-55,-12,17,-11,-31,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,17,-26,-25,]),'UNIT':([0,3,6,7,8,9,10,11,12,13,14,16,17,19,23,26,27,28,29,36,41,43,46,47,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,82,83,],[19,19,19,-14,-15,-16,19,-34,-35,19,-20,-17,-50,-39,19,-48,-49,19,19,-21,19,-38,-54,-55,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'FUNCNAME':([0,3,6,7,8,9,10,11,12,13,14,16,17,19,23,26,27,28,29,36,41,43,46,47,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,82,83,],[21,21,21,-14,-15,-16,21,-34,-35,21,-20,-17,-50,-39,21,-48,-49,21,21,-21,21,-38,-54,-55,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'SIGN':([0,14,17,19,33,34,35,38,39,40,41,42,45,55,58,65,84,],[15,37,-50,15,56,61,56,-51,-52,56,15,15,15,15,61,15,15,]),'UFLOAT':([0,15,20,41,45,58,61,70,],[-47,-46,47,-47,-47,-47,-46,47,]),'$end':([1,2,3,4,5,6,7,8,9,11,12,14,16,19,22,24,25,30,31,36,43,46,47,48,49,50,51,52,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,82,83,],[0,-1,-10,-4,-7,-33,-14,-15,-16,-34,-35,-20,-17,-39,-2,-5,-8,-32,-13,-21,-38,-54,-55,-3,-6,-9,-11,-31,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'CLOSE_PAREN':([2,3,4,5,6,7,8,9,11,12,14,16,19,22,24,25,30,31,32,36,43,46,47,48,49,50,51,52,53,54,57,59,60,62,63,64,66,67,68,69,71,72,73,74,75,76,77,78,79,80,81,82,83,86,],[-1,-10,-4,-7,-33,-14,-15,-16,-34,-35,-20,-17,-39,-2,-5,-8,-32,-13,53,-21,-38,-54,-55,-3,-6,-9,-11,-31,-36,-23,-28,-27,-22,77,-29,-18,79,-37,-40,80,-43,-44,-24,-53,82,83,-30,-19,-57,-41,-42,-26,-25,-45,]),'STAR':([3,6,7,8,9,11,12,14,16,19,36,43,46,47,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,82,83,],[26,26,-14,-15,-16,-34,-35,-20,-17,-39,-21,-38,-54,-55,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'PERIOD':([3,6,7,8,9,11,12,14,16,19,36,43,46,47,53,54,57,59,60,63,64,67,68,73,74,77,78,79,80,82,83,],[27,27,-14,-15,-16,-34,-35,-20,-17,-39,-21,-38,-54,-55,-36,-23,-28,-27,-22,-29,-18,-37,-40,-24,-53,-30,-19,-57,-41,-26,-25,]),'DOUBLE_STAR':([14,19,33,40,],[38,38,38,38,]),'CARET':([14,19,33,40,],[39,39,39,39,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'main':([0,41,],[1,66,]),'product_of_units':([0,3,6,13,23,28,29,41,],[2,22,30,32,48,51,52,2,]),'factor':([0,41,],[3,3,]),'division_product_of_units':([0,3,23,41,],[4,24,49,4,]),'inverse_unit':([0,3,23,41,],[5,25,50,5,]),'unit_expression':([0,3,6,10,13,23,28,29,41,],[6,6,6,31,6,6,6,6,6,]),'factor_fits':([0,41,],[7,7,]),'factor_float':([0,41,],[8,8,]),'factor_int':([0,41,],[9,9,]),'division':([0,3,4,23,24,41,49,81,],[10,10,28,10,28,10,28,84,]),'function':([0,3,6,10,13,23,28,29,41,],[11,11,11,11,11,11,11,11,11,]),'unit_with_power':([0,3,6,10,13,23,28,29,41,],[12,12,12,12,12,12,12,12,12,]),'signed_float':([0,41,45,58,],[16,16,71,71,]),'function_name':([0,3,6,10,13,23,28,29,41,],[18,18,18,18,18,18,18,18,18,]),'sign':([0,19,34,41,42,45,55,58,65,84,],[20,44,44,20,44,70,44,70,44,85,]),'product':([3,6,],[23,29,]),'power':([14,19,33,40,],[34,42,55,65,]),'signed_int':([14,33,34,35,40,58,],[36,54,59,62,64,76,]),'numeric_power':([19,34,42,55,65,],[43,60,67,73,78,]),'paren_expr':([45,58,],[69,69,]),'frac':([45,58,],[72,72,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> main","S'",1,None,None,None),
  ('main -> product_of_units','main',1,'p_main','generic.py',193),
  ('main -> factor product_of_units','main',2,'p_main','generic.py',194),
  ('main -> factor product product_of_units','main',3,'p_main','generic.py',195),
  ('main -> division_product_of_units','main',1,'p_main','generic.py',196),
  ('main -> factor division_product_of_units','main',2,'p_main','generic.py',197),
  ('main -> factor product division_product_of_units','main',3,'p_main','generic.py',198),
  ('main -> inverse_unit','main',1,'p_main','generic.py',199),
  ('main -> factor inverse_unit','main',2,'p_main','generic.py',200),
  ('main -> factor product inverse_unit','main',3,'p_main','generic.py',201),
  ('main -> factor','main',1,'p_main','generic.py',202),
  ('division_product_of_units -> division_product_of_units division product_of_units','division_product_of_units',3,'p_division_product_of_units','generic.py',214),
  ('division_product_of_units -> product_of_units','division_product_of_units',1,'p_division_product_of_units','generic.py',215),
  ('inverse_unit -> division unit_expression','inverse_unit',2,'p_inverse_unit','generic.py',225),
  ('factor -> factor_fits','factor',1,'p_factor','generic.py',231),
  ('factor -> factor_float','factor',1,'p_factor','generic.py',232),
  ('factor -> factor_int','factor',1,'p_factor','generic.py',233),
  ('factor_float -> signed_float','factor_float',1,'p_factor_float','generic.py',239),
  ('factor_float -> signed_float UINT signed_int','factor_float',3,'p_factor_float','generic.py',240),
  ('factor_float -> signed_float UINT power numeric_power','factor_float',4,'p_factor_float','generic.py',241),
  ('factor_int -> UINT','factor_int',1,'p_factor_int','generic.py',254),
  ('factor_int -> UINT signed_int','factor_int',2,'p_factor_int','generic.py',255),
  ('factor_int -> UINT power numeric_power','factor_int',3,'p_factor_int','generic.py',256),
  ('factor_int -> UINT UINT signed_int','factor_int',3,'p_factor_int','generic.py',257),
  ('factor_int -> UINT UINT power numeric_power','factor_int',4,'p_factor_int','generic.py',258),
  ('factor_fits -> UINT power OPEN_PAREN signed_int CLOSE_PAREN','factor_fits',5,'p_factor_fits','generic.py',276),
  ('factor_fits -> UINT power OPEN_PAREN UINT CLOSE_PAREN','factor_fits',5,'p_factor_fits','generic.py',277),
  ('factor_fits -> UINT power signed_int','factor_fits',3,'p_factor_fits','generic.py',278),
  ('factor_fits -> UINT power UINT','factor_fits',3,'p_factor_fits','generic.py',279),
  ('factor_fits -> UINT SIGN UINT','factor_fits',3,'p_factor_fits','generic.py',280),
  ('factor_fits -> UINT OPEN_PAREN signed_int CLOSE_PAREN','factor_fits',4,'p_factor_fits','generic.py',281),
  ('product_of_units -> unit_expression product product_of_units','product_of_units',3,'p_product_of_units','generic.py',300),
  ('product_of_units -> unit_expression product_of_units','product_of_units',2,'p_product_of_units','generic.py',301),
  ('product_of_units -> unit_expression','product_of_units',1,'p_product_of_units','generic.py',302),
  ('unit_expression -> function','unit_expression',1,'p_unit_expression','generic.py',313),
  ('unit_expression -> unit_with_power','unit_expression',1,'p_unit_expression','generic.py',314),
  ('unit_expression -> OPEN_PAREN product_of_units CLOSE_PAREN','unit_expression',3,'p_unit_expression','generic.py',315),
  ('unit_with_power -> UNIT power numeric_power','unit_with_power',3,'p_unit_with_power','generic.py',324),
  ('unit_with_power -> UNIT numeric_power','unit_with_power',2,'p_unit_with_power','generic.py',325),
  ('unit_with_power -> UNIT','unit_with_power',1,'p_unit_with_power','generic.py',326),
  ('numeric_power -> sign UINT','numeric_power',2,'p_numeric_power','generic.py',337),
  ('numeric_power -> OPEN_PAREN paren_expr CLOSE_PAREN','numeric_power',3,'p_numeric_power','generic.py',338),
  ('paren_expr -> sign UINT','paren_expr',2,'p_paren_expr','generic.py',347),
  ('paren_expr -> signed_float','paren_expr',1,'p_paren_expr','generic.py',348),
  ('paren_expr -> frac','paren_expr',1,'p_paren_expr','generic.py',349),
  ('frac -> sign UINT division sign UINT','frac',5,'p_frac','generic.py',358),
  ('sign -> SIGN','sign',1,'p_sign','generic.py',364),
  ('sign -> <empty>','sign',0,'p_sign','generic.py',365),
  ('product -> STAR','product',1,'p_product','generic.py',374),
  ('product -> PERIOD','product',1,'p_product','generic.py',375),
  ('division -> SOLIDUS','division',1,'p_division','generic.py',381),
  ('power -> DOUBLE_STAR','power',1,'p_power','generic.py',387),
  ('power -> CARET','power',1,'p_power','generic.py',388),
  ('signed_int -> SIGN UINT','signed_int',2,'p_signed_int','generic.py',394),
  ('signed_float -> sign UINT','signed_float',2,'p_signed_float','generic.py',400),
  ('signed_float -> sign UFLOAT','signed_float',2,'p_signed_float','generic.py',401),
  ('function_name -> FUNCNAME','function_name',1,'p_function_name','generic.py',407),
  ('function -> function_name OPEN_PAREN main CLOSE_PAREN','function',4,'p_function','generic.py',413),
]
