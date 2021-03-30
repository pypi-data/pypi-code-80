from requests import get
from bs4 import BeautifulSoup

subs = []

def get_subs(company_name):
    res = get(f"https://www.google.com/search?q={company_name}+subsidiaries")
    html_data = BeautifulSoup(res.text, 'html.parser')
    sub_body = html_data.find_all('a' ,class_ = 'BVG0Nb')
    if(len(sub_body) > 0):
        for sub in sub_body:
            name = sub["href"].split("&stick")[0].split("&q=")[1].replace("+"," ")
            subs.append(name)
        return {"status" : "200" , "msg" : "subsidiaries data found" , "data" : subs}
    else:
        return {"status" : "400" , "msg" : "subsidiaries not available" , "data" : []}