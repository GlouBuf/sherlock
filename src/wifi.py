# -*- coding: utf-8 -*-
from location import *
import sqlite3
import utils
from datetime import datetime, timedelta, timezone
from functools import reduce
import operator
import copy
from logging_utils import *




# TODO: Définir la classe WifiLogsLocationProvider
class WifiLogsLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur
    def __init__(self, db_filename, username : str):
        self.__username = username
        self.__db_filename = db_filename
        #à compléter

        #aller chercher les localisations dans la BD wifi
        self.__samples = [] # pour que ça marche en attendant...

        try :
            log("analyse du fichier" + str(db_filename) + " de log wifi en cours " )
            db_wifi = sqlite3.connect(db_filename)
            db_wifi.row_factory = utils.dict_factory #pour utiliser les résultats sous forme de dict
            cursor = db_wifi.cursor()

            for row in cursor.execute("SELECT name, timestamp, latitude, longitude from location_samples join users on location_samples.uid == users.id join hotspots on location_samples.hid == hotspots.id where users.name == ? order by location_samples.timestamp asc", (self.__username,)):
                tstamp = row['timestamp']
                date = datetime.fromtimestamp(tstamp)
                lat = row['latitude']
                long = row['longitude']
                ls = LocationSample(date, Location(lat, long), "wifi")
                self.__samples.append(ls)
                log("Location sample trouvée : " + str(ls))

        except Exception :
            log("Fichier de log wifi " + str(db_filename) + " non trouvé.")

        # Appel du constructeur de la classe mere
        super().__init__(self.__samples)
        log("Fin de l'analyse.")

    # TODO: Redéfinir la méthode str
    def __str__(self):
        # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'egravier', 4 location samples)
        return "WIFILocationProvider (source: " + str(self.__db_filename) + ", user : '" + str(self.__username) + "', " +\
               str(len(self.get_location_samples())) + " location samples)"

    # TODO: (Optionnel) Redéfinir la méthode get_surrounding_temporal_location_sample pour effectuer les calculs dans la requête SQL
    def get_closest_spatial_location_sample():
        pass

    def get_surrounding_temporal_location_sample(self, date : datetime):
        db_wifi = sqlite3.connect(self.__db_filename)
        db_wifi.row_factory = utils.dict_factory  # pour utiliser les résultats sous forme de dict
        cursor = db_wifi.cursor()
        ts = datetime.timestamp(date)
        #print("ts = ",ts)

        avant = None
        # Technique SQL : on trie par ordre du plus récent au plus vieux (ordre DESC) et on ne garde que le premier (limit 1)
        query = "SELECT timestamp, latitude, longitude from location_samples join users on \
                location_samples.uid == users.id join hotspots on location_samples.hid == hotspots.id where users.name == '" + \
                self.__username + "' and  location_samples.timestamp < '" + str(ts) + \
                "' order by location_samples.timestamp desc limit 1"
        #print(query)

        row_avant = cursor.execute(query).fetchone()
        if(row_avant != None):
            tstamp = row_avant['timestamp']
            date = datetime.fromtimestamp(tstamp)
            lat = row_avant['latitude']
            long = row_avant['longitude']
            avant = LocationSample(date, Location(lat, long))
            #print("avant = ", avant)

        # Technique SQL : on trie par ordre du plus vieux au plus récent (ordre ASC) et on ne garde que le premier (limit 1)
        query = "SELECT timestamp, latitude, longitude FROM location_samples JOIN users ON \
                location_samples.uid == users.id JOIN hotspots ON location_samples.hid == hotspots.id WHERE users.name == '" + \
                self.__username + "' AND  location_samples.timestamp > '" + str(ts) + \
                "' ORDER BY location_samples.timestamp ASC LIMIT 1"
        #print(query)

        row_apres = cursor.execute(query).fetchone()
        if(row_apres != None):
            tstamp = row_apres['timestamp']
            date = datetime.fromtimestamp(tstamp)
            lat = row_apres['latitude']
            long = row_apres['longitude']
            apres = LocationSample(date, Location(lat, long))
            #print("après = ", apres)


        return (avant, apres)

if __name__ == '__main__':
    Configuration.get_instance().add_element("verbose", True)

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # -t Z4bLkruoqSp0JXJfJGTaMQEZo -u gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc -g AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito -lat 46.522662 -lng 6.577305 -d "06/05/2019 10:19:23" -s "../data/suspects.json"

    Location.set_api_key("AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito")

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    #Configuration.get_instance().add_element("verbose", True)
    lp = WifiLogsLocationProvider('../data/db/wifi.db', 'lpalmer')
    #print(" --- Liste des Locations samples de lpalmer ---")
    #lp.print_location_samples()
    lp.show_location_samples()

    # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'egravier', 4 location samples)