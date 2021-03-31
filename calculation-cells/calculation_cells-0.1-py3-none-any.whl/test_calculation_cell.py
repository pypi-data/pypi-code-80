from unittest import TestCase
from .calculation_cell import Cell, Element
from .exceptions import (
    InvalidType,
    InvalidName,
    CircularReference,
    DangerousFormula,
    MissingParameter,
    FailedCalculation
)
class TestElement(TestCase):
    def test_ok_to_instance(self):
        x = Element("my_element_name", 100)
        self.assertIsInstance(x, Element)
    
    def test_wrong_type_to_raise(self):
        with self.assertRaises(InvalidType):
            x = Element("my_element_name", "xxx")
        with self.assertRaises(InvalidType):
            x = Element("my_element_name", False)


class TestCellAlone(TestCase):

    # Error cases

    def test_parameter_none_to_raise(self):
        with self.assertRaises(Exception):
            cell = Cell()

    def test_parameter_no_named_parameters_to_raise(self):
        with self.assertRaises(Exception):
            cell = Cell("name", [], "")

    def test_parameter_no_named_cell_to_raise(self):
        with self.assertRaises(InvalidName):
            cell = Cell(name="", inputs=[], formula="")

    def test_parameter_no_wrong_input_parameter_to_raise(self):
        with self.assertRaises(TypeError):
            cell = Cell(name="", inputs="", formula="")

    def test_parameter_no_wrong_input_parameter_to_raise(self):
        with self.assertRaises(MissingParameter):
            e1 = Element("declared_variable", 100)
            cell = Cell(name="only_cell", inputs=[e1], formula="{another_variable_not_declared}")

    def test_wrong_formula_to_raise(self):
        with self.assertRaises(FailedCalculation):
            cell = Cell(name="only_cell", inputs=[], formula="*100")
            cell.value
    
    def test_bad_things_in_formula(self):
        with self.assertRaises(DangerousFormula):
            cell = Cell(name="only_cell", inputs=[], formula="100 + 20; import os")  
            cell.value

    # Ok cases

    def test_one_element_to_output_ok(self):
        e1 = Element("declared_variable", 100)
        cell = Cell(name="only_cell", inputs=[e1], formula="{declared_variable}")
        self.assertEqual(cell.value, 100)

    def test_parameter_most_input_that_need(self):
        e1 = Element("declared_variable", 100)
        e2 = Element("not_used", 100)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{declared_variable}")
        self.assertEqual(cell.unused_variables, {'not_used'} )

    def test_parameter_sum_ok(self):
        e1 = Element("one", 100)
        e2 = Element("two", 50)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{one}+{two}")

        self.assertEqual(cell.value, 150)

    def test_parameter_rest_ok(self):
        e1 = Element("one", 100)
        e2 = Element("two", 50)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{one}-{two}")

        self.assertEqual(cell.value, 50)
    
    def test_parameter_mult_ok(self):
        e1 = Element("one", 100)
        e2 = Element("two", 50)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{one}*{two}")

        self.assertEqual(cell.value, 5000)

    def test_parameter_div_ok(self):
        e1 = Element("one", 100)
        e2 = Element("two", 50)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{one}/{two}")

        self.assertEqual(cell.value, 2)

    def test_parameter_exp_ok(self):
        e1 = Element("one", 4)
        e2 = Element("two", 2)
        cell = Cell(name="only_cell", inputs=[e1, e2], formula="{one}**{two}")

        self.assertEqual(cell.value, 16)
    
    def test_precedence_ok(self):
        e1 = Element("one", 2)
        e2 = Element("two", 3)
        e3 = Element("three", 4)
        cell = Cell(name="only_cell", inputs=[e1, e2, e3], formula="({one}+{two})*{three}")

        self.assertEqual(cell.value, 20)

class TestMultiCells(TestCase):

    def test_cascade_sum_ok(self):
        e1 = Element("one", 10)
        e2 = Element("two", 20)
        e3 = Element("three", 30)
        child_cell = Cell(name="child", inputs=[e1, e2, e3], formula="{one}+{two}+{three}") # 60
        parent_cell = Cell(name="parent", inputs=[e1, child_cell, e3], formula="{child}+{three}+{one}") # 100
        grandparent_cell = Cell(name="grandparent", inputs=[parent_cell], formula="{parent}*2") # 200

        self.assertEqual(grandparent_cell.value, 200)
