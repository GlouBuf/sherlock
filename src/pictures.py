# -*- coding: utf-8 -*-
from location import *
from functools import reduce
import os
import utils
import sys
import time
import exifread
from datetime import datetime, timezone, timedelta

# TODO: Définir la classe PictureLocationProvider qui désigne des objets LocationProvider obtenus à partir d'images
class PictureLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur
    def __init__(self, directory: str):
        self.__dir = str(directory)
        #samples doit contenir des couples (String: source_pic_file, LocationSample: sample) de sorte à garder une trace de l'origine de chaque objet LocationSample
        samples = []
        # TODO: scanner le répertoire contenant les photos prises par le suspect et extraire un objet LocationSample pour les photos ayant une extension valide (et qui contiennent des informations de localisation)

    # TODO: Définir les extensions valides et un getter pour y accéder
    def get_list_valid_extensions():
        pass

    # TODO: Redéfinir la méthode str pour afficher les objets sous la forme suivante :
    # PictureLocationProvider (source: ’ ../ data/pics /jdoe’ (JPG,JPEG,jpg,jpeg), 2 location samples)


    # TODO: Compléter la méthode _extract_location_sample_from_picture
    @staticmethod
    def _extract_location_sample_from_picture(filename: str):
        """
        Returns the time, latitude, and longitude, if available, from the EXIF data extracted from the file specified by filename
        """
        (t, lat, lng) = (None, None, None)

        with open(filename, 'rb') as f:
            exif_data = exifread.process_file(f)

            gps_latitude = utils.get_if_exists(exif_data, 'GPS GPSLatitude')
            gps_latitude_ref = utils.get_if_exists(exif_data, 'GPS GPSLatitudeRef')
            gps_longitude = utils.get_if_exists(exif_data, 'GPS GPSLongitude')
            gps_longitude_ref = utils.get_if_exists(exif_data, 'GPS GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = utils.convert_to_degrees(gps_latitude)
                if gps_latitude_ref.values[0] != 'N':
                    lat = -lat

                lng = utils.convert_to_degrees(gps_longitude)
                if gps_longitude_ref.values[0] != 'E':
                    lng = -lng

            date = utils.get_if_exists(exif_data, 'GPS GPSDate')
            timestamp = utils.get_if_exists(exif_data, 'GPS GPSTimeStamp')
            # TODO: Convertir la date (au format textuel) contenue dans le EXIF tag en datetime et le stocker dans la variable t

        return t, lat, lng


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    #Configuration.get_instance().add_element("verbose", True)
    #lp = PictureLocationProvider('../data/pics/michael')
    #print(lp)
    #lp.show_location_samples()
    # Warning: Skipping file 'unil.jpg' (Missing time and/or location information)
    # PictureLocationProvider(source: '../data/pics/jdoe'(JPG, JPEG, jpg, jpeg), 2 location samples)
    # LocationSample[datetime: 2017-02-21 13:29:04, location: Location [latitude: 46.51744, longitude: 6.56905]]
    # LocationSample[datetime: 2017-03-08 10:36:00, location: Location[latitude: 46.52206, longitude: 6.58417]]
