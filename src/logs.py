# -*- coding: utf-8 -*-
from location import *
from functools import reduce
import os
import utils
import time
import re
from datetime import datetime, timezone, timedelta

# TODO: Définir la classe PictureLocationProvider qui désigne des objets LocationProvider obtenus à partir de logs
class LogsLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur où l'on définit en attribut le nom du fichier de log
    #  et où l'on construit la liste de samples
    def __init__(self, filename):
        self.__filename = filename
        # L'attribut contenant le nom du fichier est privé et l'attribut __samples est hérité de ListLocationProvider
        #test

        # TODO: parcourir les logs et filtrer ceux qui contiennent des appels GPS valides (coordonnées + temps).
        #  Générer un sample pour chaque log valide et l'ajouter à une liste temporaire.
        #  Appeler ensuite super en passant cette liste temporaire pour définir l'attribut __samples
        self.__samples = []  # pour que ça marche en attendant...

        # Appel du constructeur de la classe mere
        super().__init__(self.__samples)


    # TODO: Implémenter la méthode __str__ pour afficher les objets de la forme suivante
    # LogsLocationProvider (source: ../data/logs/jdoe.log, 2 location samples)
    def __str__(self):
        return "LogsLocationProvider (source: " + self.__filename + ", " + str(len(self.get_location_samples())) + " location samples)"

    # TODO: Implémenter la méthode _extract_location_sample_from_picture
    @staticmethod
    def _extract_location_sample_from_log(log: str):
        pass
        """
        Returns the time, latitude, and longitude, if available, from a given log
        """
        # TODO: filtrer le log et extraire les données temporelles, créer un datetime
        # TODO: filtrer le log et extraire les données GPS
        # TODO: retourner un triplet contenant le datetime, la latitude et la longitude


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # lp = LogsLocationProvider('../data/logs/michael/michael.log')
    # print(lp)
    # lp.show_location_samples()
    # lp.print_location_samples()

    # LogsLocationProvider (source: ../data/logs/michael/michael.log, 3 location samples)
    # LocationSample [datetime: 2019-03-21 13:07:40, location: Location [latitude: 46.52145, longitude: 6.58138]]
    # LocationSample [datetime: 2019-03-21 13:08:23, location: Location [latitude: 46.52165, longitude: 6.58329]]
    # LocationSample [datetime: 2019-03-21 13:10:22, location: Location [latitude: 46.52194, longitude: 6.58569]]
