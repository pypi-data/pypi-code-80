import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, date
import operator

from ftscraper.utils import similar, etf_or_fund
from ftscraper.search_obj import SearchObj


def search(query, asset_classes=['etf','fund'], country=None):
    """
    Search assets by a given search string.

    Args
    ----
        search (str) : search string
        asset_classes (list of str) : asset types to filter search result
        country (str) : country to filter search result
    
    Returns
    -------
        search_resuts (list of objects) : search results where each object is the resulting asset 
                                        and has its own attributes (see search_obj.py)
    """
    # --------------------------------------------------------------------------------------
    # Check
    # --------------------------------------------------------------------------------------

    # check search

    asset_class_list = ['etf','fund','equity','index']


    if not query or query.isspace():
        raise ValueError("Please provide a name, partial name or symbol to search.")

    url = 'https://markets.ft.com/data/search'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    countries = soup.find(class_='o-forms__select mod-ui-form__select--event mod-search-app__country')
    countries = [country.text.lower() for country in countries.findAll('option')[1:]]

    sec_types = soup.find(class_='o-forms__select mod-ui-form__select--event mod-search-app__type')
    sec_types = [sec_type.text.lower() for sec_type in sec_types.findAll('option')[1:]]

    # Check if input country is valid
    if (country is not None) and (country not in countries):
        raise ValueError('Input country is not valid, please check the spelling. Available countries are: ' + \
            ', '.join(countries))
    # Check if input asset_class is valid
    if asset_classes is not None:
        for asset_class in asset_classes:
            if asset_class not in asset_class_list:
                raise ValueError('Input asset_class is not valid, please check the spelling. Available asset classes are: ' + \
                    ', '.join(asset_class_list))

    # --------------------------------------------------------------------------------------
    # Start searching
    # --------------------------------------------------------------------------------------

    search_results = []
    for asset_class in asset_classes:

        payload = {
            'query': query,
            'country': country,
            'assetClass': asset_class
        }
        page = requests.get(url, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find(class_='mod-ui-table mod-ui-table--freeze-pane')

        if soup is None:
            continue

        soup = soup.find('tbody')
        soup = soup.findAll('tr')

        for result in soup:
            atts = result.findAll(class_='mod-ui-table__cell--text')
            sec_name = atts[0].text
            symbol = atts[1].text
            similarity_score = similar(query,sec_name)
            search_object = SearchObj(sec_name=sec_name,symbol=symbol,sec_type=asset_class,similarity_score=similarity_score)
            search_results.append(search_object)
    
    sec_type = etf_or_fund(query, search_results)

    search_results = [result for result in search_results if result.sec_type == sec_type]
    for i, result in enumerate(search_results):
        similarity = similar(query,result.sec_name)
        search_results[i].similarity_score = similarity

    return search_results


def select_fund(search_results, income_treatment='accumulation', currency='usd',launch_date='oldest'):
    """
    Pick a fund from search results based on a given criteria.

    Args
    ----
        search_results (list of objects) : search results where each object is the resulting asset 
                                        and has its own attributes (see search_obj.py)
        income_treatment (str)  : a criteria to select a fund. can be either 'accumulation' or 'income'
        currency (str)  : a criteria to select a fund (e.g. 'usd', 'eur', 'thb')
        launch_date (str) : a criteria to select a fund. can be either 'oldest' or 'newest'

    Returns
    -------
        pick (object) : the selected fund
    """
    currency = currency.upper()
    income_treatment = income_treatment.capitalize()
    n = 1

    fund_list = []
    for i, fund in enumerate(search_results):
        summary = fund.get_summary()
        summary = {k: summary[k] for k in ['income treatment', 'launch date', 'price currency', 'xid']}
        d = datetime.strptime(summary['launch date'], '%d %b %Y')
        summary['launch date'] = d.strftime('%Y-%m-%d')

        summary['index'] = i
        summary['similarity_score'] = fund.similarity_score

        fund_list.append(summary)

    
    df = pd.DataFrame(fund_list)

    if len(df) <= 2:
        selection = df[df.similarity_score == df.similarity_score.max()]
        selection_index = selection['index'].values[0]
    else:
        selection = df.loc[(df['income treatment']==income_treatment) & (df['price currency']==currency)]
        if launch_date == 'oldest':
            ascending = True
        elif launch_date == 'newest':
            ascending = False
        selection = selection.sort_values(by='launch date', ascending=ascending)

        selection = selection.iloc[:n]
        selection = selection.to_dict('records')

        selection_index = selection['index'].values[0]
    
    pick = search_results[selection_index]

    return pick

def search_select_fund(query, country=None, asset_class=None, income_treatment='accumulation', currency='usd',launch_date='oldest'):
    """
    Search and pick a fund based on a given criteria.

    Args
    ----
        search (str): search string
        asset_classes (list of str) : asset types to filter search result
        country (str) : country to filter search result
        income_treatment (str)  : a criteria to select a fund. can be either 'accumulation' or 'income'
        currency (str)  : a criteria to select a fund (e.g. 'usd', 'eur', 'thb')
        launch_date (str) : a criteria to select a fund. can be either 'oldest' or 'newest'

    Returns
    -------
        pick (object) : the selected fund
    """
    search_results = search(query)
    pick = select_fund(search_results)
    return pick

            
