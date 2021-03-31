import re
from copy import copy
from .exceptions import (
    InvalidType,
    InvalidName,
    CircularReference,
    DangerousFormula,
    MissingParameter,
    FailedCalculation
)

REGEX_VARIABLE_NAME = "{\s?\w+\s?}"  # NOQA
REGEX_ONLY_MATH = "[0-9+.^()/*-]"  # NOQA


class Element(object):
    def __init__(self, name, value):
        self.name = name
        if not self.is_valid_input(value):
            raise InvalidType("Wrong value type. Must be float or int.")
        self._value = value

    def is_valid_input(self, input_value):
        input_type = type(input_value).__name__
        return input_type in ['float', 'int']

    @property
    def value(self):
        return self._value


class Cell(object):

    ADMISSIBLE_INPUTS = ['Element', 'Cell']
    reserved_names = []

    def _set_initial_values(self):
        self._solved = False
        self._value = None
        self.input_names = set()
        self._in_formula_variables = set()
        self.input_values = {}
        self._math_ready_formula = None
        self._unused_variables = set()

    def __init__(self, *, name: str, inputs: list, formula: str):
        self._set_initial_values()
        self.inputs = inputs
        self.formula = formula
        self.validate_inputs()
        self.formula_analisys()
        self.name = self._allowed_name(name)
        self._check_named_used_are_in_inputs()

    def formula_analisys(self):
        formula = self.formula
        self._in_formula_variables = set(
            self._extract_variables_names(formula))

    def validate_inputs(self):
        if not type(self.inputs) == list:
            raise TypeError("Inputs parameter must be a List")
        for xinput in self.inputs:
            self._validate_type_of_input(xinput)
            input_name = self._extract_input_name(xinput)
            if input_name in self.input_names:
                raise InvalidName(f"Input {input_name} is duplicated")
            self.input_names.add(input_name)

    def _allowed_name(self, name) -> str:
        if not name:
            raise InvalidName("Empty name is not valid")
        if name in self.reserved_names:
            raise InvalidName(
                f"Name {name} is not valid. Already used in another element"
            )
        if name in self._in_formula_variables:
            raise CircularReference(
                f"Name {name} is not valid."
                "Circular reference (used in formula)"
            )
        return name

    @staticmethod
    def _validate_type_of_input(input_via):
        input_type = type(input_via).__name__
        if input_type not in __class__.ADMISSIBLE_INPUTS:
            raise TypeError('{} is not a valid input'.format(repr(input_via)))

    @staticmethod
    def _extract_input_name(input_via) -> str:
        return getattr(input_via, "name", "[-no-name-]")

    def _check_named_used_are_in_inputs(self):
        undeclared_inputs = self._in_formula_variables\
            .difference(self.input_names)
        if len(undeclared_inputs):
            raise MissingParameter(
                f"There are undeclared inputs: {undeclared_inputs}"
            )
        self._unused_variables = self.input_names\
            .difference(self._in_formula_variables)

    @staticmethod
    def _extract_variables_names(formula) -> list:
        found_variables = re.compile(REGEX_VARIABLE_NAME).findall(formula)
        cleaned_names = [name[1:-1].strip() for name in found_variables]
        return cleaned_names

    @property
    def used_variables(self):
        return self._in_formula_variables

    @property
    def unused_variables(self):
        return self._unused_variables

    @property
    def solved(self):
        return self._solved

    @property
    def value(self):
        if not self._solved:
            self.solve()
        return self._value

    def solve(self):
        self._assign_values_to_inputs()
        self._value = self._calculate_formula_result()
        self._solved = True
        return self._value

    def _assign_values_to_inputs(self):
        for xinput in self.inputs:
            self.input_values[xinput.name] = xinput.value

    def _calculate_formula_result(self):
        self._clean_spaces_from_formula()
        self._replace_formula_with_each_value()
        if self._math_ready_formula:
            return self._solve_formula_matematically()
        raise Exception("Formula cannot be calculated")

    def _clean_spaces_from_formula(self):
        self.formula = self.formula.replace(" ", "")

    def _replace_formula_with_each_value(self):
        tmp_formula = copy(self.formula)
        for input_name in self.input_names:
            tmp_formula = tmp_formula.replace(
                "{" + input_name + "}",
                str(self.input_values[input_name]))
        self._math_ready_formula = tmp_formula

    def _solve_formula_matematically(self):
        self.prevent_unsecure_formula()
        try:
            calculated = eval(self._math_ready_formula)
        except ZeroDivisionError:
            raise FailedCalculation(
                f"Division by zero. Evaluated {self._math_ready_formula}"
            )
        except SyntaxError:
            raise FailedCalculation(
                f"Invalid sintax. Evaluated {self._math_ready_formula}"
            )

        if not type(calculated) in [float, int]:
            raise FailedCalculation(
                f"Evaluation result: {calculated}"
            )
        return calculated

    def prevent_unsecure_formula(self):
        insecure_chars = re.sub(
            REGEX_ONLY_MATH, "", self._math_ready_formula, 0, re.MULTILINE)
        if insecure_chars:
            raise DangerousFormula(
                f"Insecure chars found in formula: {insecure_chars}"
            )


if __name__ == "__main__":
    x = Element("variable", 100)
    c = Cell(name="test", inputs=[x], formula="{variable}-200")
    d = Cell(name="padre", inputs=[x, c], formula="{test}+50")
    d = Cell(name="abuelo", inputs=[x, c], formula="{test}+50")
