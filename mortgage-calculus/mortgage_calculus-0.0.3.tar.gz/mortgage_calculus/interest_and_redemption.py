"""This module provides functions related to redemptions and interest."""

from typing import Optional, Union, Tuple
import pandas as pd
import numpy as np


def determine_annuity(
    months_to_legal_maturity: int, outstanding_balance: float, interest_rate:
        float) -> float:
    """Calculate the (monthly) annuity.
    For mortgage with specified months_to_legal_maturity (>=1), outstanding
    balance, and interest rate (decimal, annual).
    """
    tau = interest_rate / 12
    kappa = (1 + tau) ** months_to_legal_maturity
    return outstanding_balance * tau * kappa / (kappa - 1)


def determine_interest(outstanding_balance: float, interest_rate:
                       float) -> float:
    """Determine the interest of a mortgage.
    In a month in case the principal at start of the month is given by
    outstanding_balance and the interest rate is given by interest_rate
    (as decimal, annual).
    """
    return outstanding_balance * interest_rate / 12


def determine_redemption_linear(
    months_to_legal_maturity: int, outstanding_balance: float
) -> float:
    """Determine the redemption of linear mortgage.
    
    In month t in case the principal at start of the month is given by outstanding_balance
    """
    return outstanding_balance / months_to_legal_maturity


def determine_redemption_bullet(months_to_legal_maturity: int, outstanding_balance: float
) -> float:
    """Determine the redemption of bullet mortgage.
    
    In a month in case the principal at start of the month is given by outstanding_balance.
    """
    return outstanding_balance if months_to_legal_maturity == 1 else 0


def determine_redemption_annuity(
    months_to_legal_maturity: int,
    outstanding_balance: float,
    interest_rate: float,
    annuity: Optional[float] = None,
) -> float:
    """Calculate the redemption of an annuity mortgage.
    
    On basis of the outstanding_balance at the start of the month, the interest rate, and the
    months to legal maturity. The annuity can optionally be given in case it has
    been calculated elsewhere.
    """
    if annuity is None:
        annuity = determine_annuity(
            months_to_legal_maturity, outstanding_balance, interest_rate
        )
    return annuity - determine_interest(outstanding_balance, interest_rate)


def determine_redemption(
    months_to_legal_maturity: int,
    outstanding_balance: float,
    mortgage_type: str,
    interest_rate: Optional[float] = None,
) -> float:
    """Determine the redemption of mortgage.
    
    For mortgage of type mortgage_type, in a month in case the principal at
    start of the month is given by outstanding_balance. In case of
    annuity the interest_rate is required as input.
    """
    if mortgage_type == "bullet":
        return determine_redemption_bullet(
            months_to_legal_maturity, outstanding_balance
        )
    elif mortgage_type == "linear":
        return determine_redemption_linear(
            months_to_legal_maturity, outstanding_balance
        )
    elif mortgage_type == "annuity":
        return determine_redemption_annuity(
            months_to_legal_maturity, outstanding_balance, interest_rate, None
        )

