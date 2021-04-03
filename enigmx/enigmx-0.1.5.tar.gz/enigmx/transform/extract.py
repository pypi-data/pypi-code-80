from enigmx.transform.extractor import Extractor

list_stocks=['ACIW']

Extractor(
    list_stocks = list_stocks,
    start_date = "2021-01-04",
    end_date= "2021-03-26",
    path = "C:/data/", 
    api_key='c04f66748v6u76cjieag',
    threads=1,
    tupleTimeZone = (9,10)
    )



