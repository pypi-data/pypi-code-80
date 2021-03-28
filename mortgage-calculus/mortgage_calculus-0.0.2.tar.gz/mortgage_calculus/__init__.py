"""
Mortgage Calculus module for Python
===================================

mortgage_calculus is a Python module to
analyze mortgages and their cashflows.
"""

__version__ = "0.0.1"

from .interest_and_redemption import determine_redemption
from .cashflows import cashflows_happy_flow, cashflows_happy_flow_df
