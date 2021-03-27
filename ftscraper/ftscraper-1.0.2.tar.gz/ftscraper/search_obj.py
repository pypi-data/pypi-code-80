import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import date


class SearchObj(object):
    """Class which contains each search result when searching data in Financial Times.
    
    This class contains the search results of the ft.com search made with the function
    call `ftscraper.search(search)` which returns a :obj:`list` 
    of instances of this class with the formatted retrieved information.
    """

    def __init__(self, sec_name, symbol, sec_type, similarity_score):
        self.sec_name = sec_name
        self.symbol = symbol
        self.sec_type = sec_type
        self.similarity_score = similarity_score

    def get_summary(self):
        """
        Get summary of the fund
        """

        url = 'https://markets.ft.com/data/funds/tearsheet/summary'
        payload = {'s': self.symbol}
        page = requests.get(url, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        profile = soup.find(class_='mod-ui-table mod-ui-table--two-column mod-profile-and-investment-app__table--profile')
        atts = {'sec_name':self.sec_name,'sec_type':self.sec_type,'symbol':self.symbol}
        atts['income treatment'] = None
        for att in profile.findAll('tr'):
            key = att.find('th').text.lower()
            value = att.find('td').text
            atts[key] = value
        
        atts['xid'] = self.get_idx()

        return atts
    
    def get_idx(self):
        """
        Get ID of the fund (This ID is unique for ft.com)
        """
        url = 'https://markets.ft.com/data/funds/tearsheet/charts'
        payload = {'s': self.symbol}
        page = requests.get(url, params=payload)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = soup.find(class_="mod-app clearfix mod-ichart")
        xid = re.search('&quot;baseXid&quot;:&quot;(.*)&quot;,&quot;days&quot;', str(soup)).group(1)

        return xid
    
    def get_historical(self):
        """
        Get historical prices of the fund
        """

        d0 = date(1970, 1, 1)
        d1 = date.today()
        delta = d1 - d0

        headers = {
            'content-type': 'application/json',
        }
        payload = {"days":delta.days,
                "dataNormalized":'false',
                "dataPeriod":"Day",
                "returnDateType":"ISO8601",
                "elements":[{
                            "Type":"price",
                            "Symbol":self.get_idx(),
                            }]
                }
        response = requests.post('https://markets.ft.com/data/chartapi/series', headers=headers, data=json.dumps(payload))
        response = response.json()
        dates = response['Dates']
        dates = [date.split('T')[0] for date in dates]
        dates = {'date':dates}
        component_series = response['Elements'][0]['ComponentSeries']
        prices = {component['Type'].lower(): component['Values'] for component in component_series}

        result = {**dates,**prices}
        df = pd.DataFrame(result)

        return df

    
