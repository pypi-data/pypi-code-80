# import pathlib
import re
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Cnpj:

    value: str
    _value: str = field(init=False, repr=False)

    @property  # type: ignore
    def value(self) -> str:
        v = self._value
        return f"{v[0:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"

    @value.setter
    def value(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{14}$", v):
            raise ValueError(
                "Cnpj must be a string with 14 decimal numbers (non decimal "
                "characters are discarded), e.g format: XX.XXX.XXX/YYYY-ZZ"
            )
        self._value = v
        if not self.validate():
            raise ValueError("Cnpj failed the validation algorithm")

    def validate(self) -> bool:
        # implementation according to:
        # https://pt.wikipedia.org/wiki/Cadastro_Nacional_da_Pessoa_Jur%C3%ADdica
        vs = [int(v) for v in self._value]

        # check the first verification number
        c1 = 5 * vs[0] + 4 * vs[1] + 3 * vs[2] + 2 * vs[3]
        c1 += 9 * vs[4] + 8 * vs[5] + 7 * vs[6] + 6 * vs[7]
        c1 += 5 * vs[8] + 4 * vs[9] + 3 * vs[10] + 2 * vs[11]
        c1 = 11 - c1 % 11
        c1 = 0 if c1 > 9 else c1

        # check the second verification number
        c2 = 6 * vs[0] + 5 * vs[1] + 4 * vs[2] + 3 * vs[3]
        c2 += 2 * vs[4] + 9 * vs[5] + 8 * vs[6] + 7 * vs[7]
        c2 += 6 * vs[8] + 5 * vs[9] + 4 * vs[10] + 3 * vs[11]
        c2 += 2 * vs[12]
        c2 = 11 - c2 % 11
        c2 = 0 if c2 > 9 else c2

        return c1 == vs[12] and c2 == vs[13]


@dataclass
class Product:
    code: str
    description: str
    unit: str

    qty: str
    _qty: float = field(init=False, repr=False)

    @property  # type: ignore
    def qty(self) -> float:
        return self._qty

    @qty.setter
    def qty(self, v: str):
        q = v.replace(",", ".")
        try:
            self._qty = float(q)
        except ValueError:
            raise ValueError(
                f"Product qty must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    value: str
    _value: float = field(init=False, repr=False)

    @property  # type: ignore
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: str):
        val = v.replace(",", ".")
        try:
            self._value = float(val)
        except ValueError:
            raise ValueError(
                f"Product value must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )

    total: str
    _total: float = field(init=False, repr=False)

    @property  # type: ignore
    def total(self) -> float:
        return self._total

    @total.setter
    def total(self, v: str):
        t = v.replace(",", ".")
        try:
            self._total = float(t)
        except ValueError:
            raise ValueError(
                f"Product total must be a string representing a float, with "
                f"a comma, e.g: XX,YY, instead got: {v}"
            )


@dataclass
class Key:

    value: str
    _value: str = field(init=False, repr=False)

    @property  # type: ignore
    def value(self) -> str:
        return " ".join(textwrap.wrap(self._value, 4))

    @value.setter
    def value(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{44}$", v):
            raise ValueError(
                "Access key must be a string with 44 decimal numbers (non"
                "decimal characters are discarded), e.g format: "
                "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234"
            )
        self._value = v


@dataclass
class AuthProtocol:

    value: str
    _value: str = field(init=False, repr=False)

    @property  # type: ignore
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{15}$", v):
            raise ValueError(
                "Authorization protocol must be a string with 15 decimal "
                "numbers (non decimal characters are discarded), e.g format: "
                "123456789012345"
            )
        self._value = v


@dataclass
class Cpf:

    value: str
    _value: str = field(init=False, repr=False)

    @property  # type: ignore
    def value(self) -> str:
        v = self._value
        return f"{v[0:3]}.{v[3:6]}.{v[6:9]}-{v[9:12]}"

    @value.setter
    def value(self, v: str):
        v = re.sub(r"[^\d]*", "", v)  # remove everything that is non decimal
        if not re.match(r"^\d{11}$", v):
            raise ValueError(
                "Cpf must be a string with 11 decimal numbers (non decimal "
                "characters are discarded), e.g format: XXX.XXX.XXX-YY"
            )
        self._value = v


@dataclass
class Nfe:
    co_name: str
    co_state_reg: int
    co_cnpj: Cnpj
    co_addr: str
    products: List[Product]
    num: int
    series: int
    emission_date: datetime
    key: Key
    auth_protocol: AuthProtocol
    cpf: Cpf
    total: float
    discount: float
