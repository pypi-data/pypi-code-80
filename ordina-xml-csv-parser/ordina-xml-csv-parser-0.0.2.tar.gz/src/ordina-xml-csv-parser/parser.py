import pandas as pd
import numpy as np

import xml.etree.ElementTree as ET

from datetime import datetime

ns={
    'ns0': 'urn:ndov:cdm:trein:reisinformatie:messages:3',
    'ns1': 'urn:ndov:cdm:trein:reisinformatie:data:2'
}

data = {
    # Ride
    'RideId':[],
    'RideTime': [],

    # Departure station
    'DepartureStationCode': [],
    'DepartureStationUIC': [],
    'DepartureStationType': [],

    # Train
    'TrainId': [],
    'TrainType': [],
    'TrainOperator': [],

    # Planned destination
    'PlannedDestinationStationCode': [],
    'PlannedDestinationStationUIC': [],
    'PlannedDestinationStationType': [],

    # Actual destination
    'ActualDestinationStationCode': [],
    'ActualDestinationStationUIC': [],
    'ActualDestinationStationType': [],

    # Departure times
    'PlannedDepartureTime': [],
    'ActualDepartureTime': [],
    'ExactDepartureDelay': [],
    'RoundedDepartureDelay': [],

    # Departure platforms
    'PlannedDeparturePlatform': [],
    'ActualDeparturePlatform': [],

    # Stop stations
    'PlannedStopStations': [],
    'ActualStopStations': [],

    # Matirial type
    'MaterialType': [],
    'MaterialDesignation': [],
    'MaterialLength': [],

    # Change
    'HasChange': [],
    'ChangeType': [],

    # Trip tip
    'TripTipCode': [],
    'TripTipStations' : [],

    # Planned Shortened route
    'PlannedShortenedStationCode': [],
    'PlannedShortenedStationUIC': [],
    'PlannedShortenedStationType': [],

    # Actual Shortened route
    'ActualShortenedStationCode': [],
    'ActualShortenedStationUIC': [],
    'ActualShortenedStationType': []
}


def extract_station_info(data, node, prefix):
  if node:
    data[prefix + 'Code'].append(node.find('./ns1:StationCode', ns).text)
    data[prefix + 'UIC'].append(int(node.find('./ns1:UICCode', ns).text))
    data[prefix + 'Type'].append(int(node.find('./ns1:Type', ns).text))
  else:
    data[prefix + 'Code'].append(np.NaN)
    data[prefix + 'UIC'].append(np.NaN)
    data[prefix + 'Type'].append(np.NaN)


def parse_timestamp(date_string):
  return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')


def encode_list(nodes, sufix):
  UIC_codes = [node.find(sufix, ns).text for node in nodes]
  return ';'.join(UIC_codes)


def parse_data(df):
    for root_text in df['xml_obj'].values:
        root = ET.fromstring(root_text)

        # Ride
        ride = root.find('./ns1:ReisInformatieProductDVS/ns1:DynamischeVertrekStaat', ns)
        data['RideId'].append(int(ride.find('ns1:RitId', ns).text))
        date_string = root.find('./ns1:ReisInformatieProductDVS/ns1:RIPAdministratie/ns1:ReisInformatieTijdstip',
                                ns).text
        data['RideTime'].append(parse_timestamp(date_string))

        # Train
        train = ride.find('./ns1:Trein', ns)
        data['TrainId'].append(train.find('./ns1:TreinNummer', ns).text)
        data['TrainType'].append(train.find('./ns1:TreinSoort', ns).text)
        data['TrainOperator'].append(train.find('./ns1:Vervoerder', ns).text)

        # Planned destination
        plannedDest = train.find('./ns1:TreinEindBestemming[@InfoStatus="Gepland"]', ns)
        extract_station_info(data, plannedDest, 'PlannedDestinationStation')

        # Planned destination
        actualDest = train.find('./ns1:TreinEindBestemming[@InfoStatus="Actueel"]', ns)
        extract_station_info(data, actualDest, 'ActualDestinationStation')

        # Departure station
        extract_station_info(data, ride.find('./ns1:RitStation', ns), 'DepartureStation')

        data['PlannedDeparturePlatform'].append(
            int(train.find('./ns1:TreinVertrekSpoor[@InfoStatus="Gepland"]/ns1:SpoorNummer', ns).text))
        data['ActualDeparturePlatform'].append(
            int(train.find('./ns1:TreinVertrekSpoor[@InfoStatus="Actueel"]/ns1:SpoorNummer', ns).text))

        # Departure times
        date_string = train.find('./ns1:VertrekTijd[@InfoStatus="Gepland"]', ns).text
        data['PlannedDepartureTime'].append(parse_timestamp(date_string))

        date_string = train.find('./ns1:VertrekTijd[@InfoStatus="Actueel"]', ns).text
        data['ActualDepartureTime'].append(parse_timestamp(date_string))

        data['ExactDepartureDelay'].append(train.find('./ns1:ExacteVertrekVertraging', ns).text)
        data['RoundedDepartureDelay'].append(train.find('./ns1:GedempteVertrekVertraging', ns).text)

        # Stop stations
        wagons = train.find('./ns1:TreinVleugel', ns)
        stop_stations = wagons.findall('./ns1:StopStations[@InfoStatus="Gepland"]/ns1:Station', ns)
        data['PlannedStopStations'].append(encode_list(stop_stations, './ns1:UICCode'))

        stop_stations = wagons.findall('./ns1:StopStations[@InfoStatus="Actueel"]/ns1:Station', ns)
        data['ActualStopStations'].append(encode_list(stop_stations, './ns1:UICCode'))

        # Material
        material = wagons.find('./ns1:MaterieelDeelDVS', ns)
        if material:
            data['MaterialType'].append(material.find('./ns1:MaterieelSoort', ns).text)
            data['MaterialDesignation'].append(material.find('./ns1:MaterieelAanduiding', ns).text)
            data['MaterialLength'].append(material.find('./ns1:MaterieelLengte', ns).text)
        else:
            data['MaterialType'].append(np.NaN)
            data['MaterialDesignation'].append(np.NaN)
            data['MaterialLength'].append(np.NaN)

        # Change
        changes = root.findall('.//ns1:Wijziging', ns)
        if changes:
            data['HasChange'].append(True)
            data['ChangeType'].append(encode_list(changes, './ns1:WijzigingType'))
        else:
            data['HasChange'].append(False)
            data['ChangeType'].append(np.NaN)

        # Trip tip
        tip = train.find('./ns1:ReisTip', ns)
        if tip:
            data['TripTipCode'].append(tip.find('./ns1:ReisTipCode', ns).text)
            data['TripTipStations'].append(encode_list(tip.findall('./ns1:ReisTipStation', ns), './ns1:UICCode'))
        else:
            data['TripTipCode'].append(np.NaN)
            data['TripTipStations'].append(np.NaN)

        # Shortened route
        plannedShort = train.find('./ns1:VerkorteRoute[@InfoStatus="Gepland"]', ns)
        if plannedShort:
            extract_station_info(data, plannedDest, 'PlannedShortenedStation')
        else:
            extract_station_info(data, None, 'PlannedShortenedStation')

        actualShort = train.find('./ns1:VerkorteRoute[@InfoStatus="Actueel"]', ns)
        if actualShort:
            extract_station_info(data, plannedDest, 'ActualShortenedStation')
        else:
            extract_station_info(data, None, 'ActualShortenedStation')


def parser():
    file_path = str(input('Enter the file path to store your data: '))  # specify the directory where the file will be stored
    file_name = str(input('Enter the file name of your data: '))  # specify the name of the file with out the type

    # specify a range of days you want to store
    start_date = str(input('Enter the start date in format: month/day/year: '))
    end_date = str(input('Enter the end date in format: month/day/year: '))

    time_period = np.array(pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d'))  # create all dates
    # loop through all days
    for day in time_period:
        print(day)
        df = pd.read_csv(f'https://trein.fwrite.org/AMS-Aurora-archive/{day[:7]}/DVS_{day}.csv.xz',
                         header=None,
                         names=['date', 'xml_obj', 'uuid'])
        parse_data(df)  # parse all the rows of a day into the right format

    # convert the data into a dataframe
    df_flat = pd.DataFrame(data)
    print(df_flat.shape)  # view how big the dataset is
    # save the file to a csv
    df_flat.to_csv(f'{file_path}/{file_name}.csv.zip', index=False,
                   compression=dict(method='zip', archive_name=f'{file_name}.csv'))



