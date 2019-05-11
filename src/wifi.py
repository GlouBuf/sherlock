# -*- coding: utf-8 -*-
from location import *
import sqlite3
import utils
from datetime import datetime, timedelta, timezone
from functools import reduce
import operator
import copy



# TODO: Définir la classe WifiLogsLocationProvider
class WifiLogsLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur
    def __init__(self, db_filename, username : str):
        self.__username = username
        self.__db_filename = db_filename
        #à compléter

        #aller chercher les localisations dans la BD wifi
        self.__samples = [] # pour que ça marche en attendant...

        db_wifi = sqlite3.connect(db_filename)
        db_wifi.row_factory = utils.dict_factory #pour utiliser les résultats sous forme de dict
        cursor = db_wifi.cursor()


        for row in cursor.execute("SELECT name, timestamp, latitude, longitude from location_samples join users on location_samples.uid == users.id join hotspots on location_samples.hid == hotspots.id where users.name == '" + self.__username + "' order by location_samples.timestamp asc"):
            tstamp = row['timestamp']
            date = datetime.fromtimestamp(tstamp)
            lat = row['latitude']
            long = row['longitude']
            ls = LocationSample(date, Location(lat, long))
            self.__samples.append(ls)

        # Appel du constructeur de la classe mere
        super().__init__(self.__samples)

    # TODO: Redéfinir la méthode str
    def __str__(self):
        # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'egravier', 4 location samples)
        return "WIFILocationProvider (source: " + str(self.__db_filename) + ", user : '" + str(self.__username) + "', " +\
               str(len(self.get_location_samples())) + " location samples)"

    # TODO: (Optionnel) Redéfinir la méthode get_surrounding_temporal_location_sample pour effectuer les calculs dans la requête SQL
    def get_closest_spatial_location_sample():
        pass

    def get_surrounding_temporal_location_sample(self, date : datetime):
        pass
        db_wifi = sqlite3.connect(self.__db_filename)
        db_wifi.row_factory = utils.dict_factory  # pour utiliser les résultats sous forme de dict
        cursor = db_wifi.cursor()
        ts = datetime.timestamp(date)

        avant = None
        for row in cursor.execute("SELECT timestamp, latitude, longitude from location_samples join users on location_samples.uid == users.id join hotspots on location_samples.hid == hotspots.id where users.name == '" + self.__username + "' and  location_samples.timestamp < '" + str(ts) + "'  order by location_samples.timestamp asc"):
            print(row)
        '''if rows.arraysize != 0 :
            row_avant = rows[0]
            tstamp = row_avant['timestamp']
            date = datetime.fromtimestamp(tstamp)
            lat = row_avant['latitude']
            long = row_avant['longitude']
            avant = LocationSample(date, Location(lat, long))
            print(avant)'''

if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    #Configuration.get_instance().add_element("verbose", True)
    lp = WifiLogsLocationProvider('../data/db/wifi.db', 'egravier')
    print(lp)
    print(lp.get_surrounding_temporal_location_sample(datetime(2018,5,16,11,27,23)))
    lp.show_location_samples()

    # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'egravier', 4 location samples)