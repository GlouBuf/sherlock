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
    def __init__(self, username : str, db):
        self.__username = username
        self.__db = db
        #à compléter

    # TODO: Redéfinir la méthode str

    # TODO: (Optionnel) Redéfinir la méthode get_surrounding_temporal_location_sample pour effectuer les calculs dans la requête SQL
    def get_closest_spatial_location_sample():
        pass

    def get_surrounding_temporal_location_sample():
        pass

if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # Configuration.get_instance().add_element("verbose", True)
    # lp = WifiLogsLocationProvider('../data/db/wifi.db', 'egravier')
    # print(lp)
    # lp.show_location_samples()

    # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'egravier', 4 location samples)