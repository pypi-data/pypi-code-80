import pandas as pd
import os
import wget
from prediction_module.io import url_db_pre, url_vis, path_target, C_names
from download import download
from shapely.geometry import Point


class Load_db_predict:

    def __init__(self, url_db=url_db_pre, path_target=path_target):
        download(url_db, path_target, replace=False)

    @staticmethod
    def save_as_df():
        df_bikes = pd.read_csv(path_target, na_values="", low_memory=False,
                               converters={'data': str, 'heure': str})
        return df_bikes.iloc[:, 0:4].dropna()


class Load_db_vis:
    name = C_names
    urls = url_vis

    # Download jsons files and fix them to be opened as DFs
    def __init__(self, urls=urls, name=name):
        i = 0
        for url in urls:
            path_target_txt = os.path.join(os.path.dirname(
                                           os.path.realpath(__file__)),
                                           "..", "data/compteurs", name[i] +
                                           ".txt")
            if os.path.isfile(path_target_txt):
                os.remove(path_target_txt)
            wget.download(url, path_target_txt)
            path_target2 = os.path.join(os.path.dirname(os.path.realpath(
                                        __file__)), "..",
                                        "data/compteurs", name[i]+".json")
            file = open(path_target_txt, "r")
            if os.path.isfile(path_target2):
                os.remove(path_target2)
            newfile = open(path_target2, 'x')
            for line in file:
                newfile.write(line.replace('}{', '}\n{'))
            file.close()
            os.remove(path_target_txt)
            i += 1

    @staticmethod
    def save_as_df2(name):
        # return the df well formated for scattermapbox
        path_target2 = os.path.join(os.path.dirname(
                                    os.path.realpath(__file__)), "..",
                                    "data/compteurs",
                                    name+".json")
        df_bikes = pd.read_json(path_target2, lines=True)
        del df_bikes['laneId']
        # format date for scatter_mapbox
        temp = df_bikes['dateObserved']
        l_date = []
        temp = list(temp)
        for i in temp:
            l_date.append(i.split('T')[0])
        df_bikes['dateObserved'] = l_date
        df_bikes = df_bikes.iloc[:, 0:3]
        lat = Point(list(df_bikes['location'])[0]['coordinates']).y
        df_bikes['lat'] = [lat]*len(df_bikes)
        lon = Point(list(df_bikes['location'])[0]['coordinates']).x
        df_bikes['lon'] = [lon]*len(df_bikes)
        del df_bikes['location']
        return df_bikes.iloc[:, 0:4]
