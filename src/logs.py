# -*- coding: utf-8 -*-
from location import *
from functools import reduce
import os
import utils
import time
import re
from datetime import datetime, timezone, timedelta
from logging_utils import *


# TODO: Définir la classe PictureLocationProvider qui désigne des objets LocationProvider obtenus à partir de logs
class LogsLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur où l'on définit en attribut le nom du fichier de log
    #  et où l'on construit la liste de samples
    def __init__(self, filename):
        self.__filename = filename
        self.__samples = []
        # L'attribut contenant le nom du fichier est privé et l'attribut __samples est hérité de ListLocationProvider
        # TODO: parcourir les logs et filtrer ceux qui contiennent des appels GPS valides (coordonnées + temps).
        #  Générer un sample pour chaque log valide et l'ajouter à une liste temporaire.
        #  Appeler ensuite super en passant cette liste temporaire pour définir l'attribut __samples

        try :
            log("Analyse du fichier de log : " + self.__filename)
            with open(self.__filename, "r") as f:
                for line in f.readlines():
                    tuple = LogsLocationProvider._extract_location_sample_from_log(line)
                    if tuple != None :
                        ls = LocationSample(tuple[0], Location(tuple[1], tuple[2]), "logs")
                        #print(r.groups())
                        self.__samples.append(ls)
        except FileNotFoundError :
            log("Fichier " + str(self.__filename) + " non trouvé.")

        # Appel du constructeur de la classe mere
        super().__init__(self.__samples)
        log("Fin de l'analyse.")


    # TODO: Implémenter la méthode __str__ pour afficher les objets de la forme suivante
    # LogsLocationProvider (source: ../data/logs/jdoe.log, 2 location samples)
    def __str__(self):
        return "LogsLocationProvider (source: " + self.__filename + ", " + str(len(self.get_location_samples())) + " location samples)"

    # TODO: Implémenter la méthode _extract_location_sample_from_picture
    @staticmethod
    def _extract_location_sample_from_log(ligne: str):
        """
        Returns the time, latitude, and longitude, if available, from a given log
        """
        # TODO: filtrer le log et extraire les données temporelles, créer un datetime
        # TODO: filtrer le log et extraire les données GPS
        # TODO: retourner un triplet contenant le datetime, la latitude et la longitude
        r = re.match("^\[(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}\.\d{3})\].*\((.*), (.*)\), source: GPS$", ligne)
        if r != None:
            log("Ligne trouvée avec date et localisation GPS ")
            log(str(ligne))
            dt = datetime(int(r.groups()[0]), int(r.groups()[1]), int(r.groups()[2]), int(r.groups()[3]), int(r.groups()[4]), round(float(r.groups()[5])))
            lat = float(r.groups()[6])
            long = float(r.groups()[7])
            log("Valeurs extraites (date, latitude, longitude) : " + "("+ str(dt) + ", " + str(lat) + ", " + str(long) + ")")
            return dt, lat, long
        else :
            return None



if __name__ == '__main__':
    Configuration.get_instance().add_element("verbose", True)

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # -t Z4bLkruoqSp0JXJfJGTaMQEZo -u gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc -g AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito -lat 46.522662 -lng 6.577305 -d "06/05/2019 10:19:23" -s "../data/suspects.json"

    Location.set_api_key("AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito")
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    lp = LogsLocationProvider('../data/logs/bhorne.log')
    print(lp)
    lp.show_location_samples()
    lp.print_location_samples()

    # LogsLocationProvider (source: ../data/logs/michael/michael.log, 3 location samples)
    # LocationSample [datetime: 2019-03-21 13:07:40, location: Location [latitude: 46.52145, longitude: 6.58138]]
    # LocationSample [datetime: 2019-03-21 13:08:23, location: Location [latitude: 46.52165, longitude: 6.58329]]
    # LocationSample [datetime: 2019-03-21 13:10:22, location: Location [latitude: 46.52194, longitude: 6.58569]]
