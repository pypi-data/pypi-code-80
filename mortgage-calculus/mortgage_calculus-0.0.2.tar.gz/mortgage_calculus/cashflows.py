"""This module provides functions related to cashflows."""

from .interest_and_redemption import determine_interest, determine_redemption 

from typing import Optional, Union, Tuple
import pandas as pd
import numpy as np

def cashflows_happy_flow(
    balance: float,
    months_to_legal_maturity: int,
    interest_rate: Union[float, np.array],
    mortgage_type: float,
) -> Tuple[np.array, np.array, np.array]:
    """Determine the evolution of the interest, redemption and outstanding balance.
    For a mortgage of type mortgage_type, a specified balance with months_to_legal_maturity to go,
    and a specified interest rate. The interest_rate can be a float or a numpy array with the
    prevailing interest rate as values.
    """
    # initialization:
    interest = np.zeros(months_to_legal_maturity + 1)
    redemption = np.zeros(months_to_legal_maturity + 1)
    outstanding_balance = np.zeros(months_to_legal_maturity + 1)
    interest[0] = 0
    redemption[0] = 0
    outstanding_balance[0] = balance
    # check type input for interest_rate:
    if isinstance(interest_rate, float):
        r = interest_rate
        interest_rate = np.zeros(months_to_legal_maturity + 1)
        interest_rate[0] = np.nan
        interest_rate[1:] = np.ones(months_to_legal_maturity) * r
    else:
        interest_rate = np.append(np.nan, interest_rate)     
    for t in range(1, months_to_legal_maturity + 1):
        interest[t] = determine_interest(outstanding_balance[t - 1], interest_rate[t])
        redemption[t] = determine_redemption(
            months_to_legal_maturity - (t - 1),
            outstanding_balance[t - 1],
            mortgage_type,
            interest_rate[t],
        )
        outstanding_balance[t] = outstanding_balance[t - 1] - redemption[t]
    return interest, redemption, outstanding_balance

def cashflows_happy_flow_df(
    balance: float,
    months_to_legal_maturity: int,
    interest_rate: Union[float, np.array], mortgage_type: float) -> pd.DataFrame:
    """Determine the evolution of the interest, redemption and outstanding balance.
    
    For a mortgage of type mortgage_type, a specified balance with months_to_legal_maturity to go,
    and a specified interest rate. The interest_rate can be a float or a numpy array with the
    prevailing interest rate as values.
    """
    interest, redemption, outstanding_balance = cashflows_happy_flow(
    balance,
    months_to_legal_maturity,
    interest_rate,
    mortgage_type)
    if isinstance(interest_rate, float):
        r = interest_rate
        interest_rate = np.zeros(months_to_legal_maturity + 1)
        interest_rate[0] = np.nan
        interest_rate[1:] = np.ones(months_to_legal_maturity) * r
    else:
        interest_rate = np.append(np.nan, interest_rate)  
    balances_df = pd.DataFrame([outstanding_balance, interest, redemption, interest_rate]).transpose()
    balances_df.columns = ["balance", "interest", "redemption", "interest_rate"]
    balances_df["gross_installment"] = (
        balances_df["interest"] + balances_df["redemption"]
    )
    return balances_df