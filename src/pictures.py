# -*- coding: utf-8 -*-
from location import *
from functools import reduce
import os
import utils
import sys
import time
import exifread
from _datetime import *
from datetime import datetime, timezone, timedelta
from configuration import *


# TODO: Définir la classe PictureLocationProvider qui désigne des objets LocationProvider obtenus à partir d'images
class PictureLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur
    def __init__(self, directory: str):
        self.__dir = str(directory)
        #samples doit contenir des couples (String: source_pic_file, LocationSample: sample) de sorte à garder une trace de l'origine de chaque objet LocationSample
        __samples = []
        # TODO: scanner le répertoire contenant les photos prises par le suspect et extraire un objet LocationSample pour les photos ayant une extension valide (et qui contiennent des informations de localisation)
        liste_suffix = [".jpg", ".jpeg", ".JPG", ".JPEG"]
        for fichier in os.scandir(directory) :
            for suffix in liste_suffix:
                if fichier.name.endswith(suffix):
                    source_pic_file = str(fichier)
                    try :
                        photo = os.path.join(self.__dir, fichier.name)
                        elements_de_ls = PictureLocationProvider._extract_location_sample_from_picture(photo) #on obtient un datetime, une latitude et une longitude
                        location_de_ls = Location(elements_de_ls[1], elements_de_ls[2])
                        ls = LocationSample(elements_de_ls[0], location_de_ls, "Picture", photo)  # on crée un LocationSample
                        __samples.append(ls)
                    except ValueError :
                        print("PAS DE DONNEES EXIF DANS L'image " + fichier.name + " fichier ignoré : on passe au fichier suivant.")


        super().__init__(__samples)


    # TODO: Définir les extensions valides et un getter pour y accéder
    def get_list_valid_extensions(self):
        return copy.deepcopy(self.__samples)

    # TODO: Redéfinir la méthode str pour afficher les objets sous la forme suivante :
    # PictureLocationProvider (source: ’ ../ data/pics /jdoe’ (JPG,JPEG,jpg,jpeg), 2 location samples)
    def __str__(self):
        return "PictureLocationProvider (source: " + self.__dir + " (JPG,JPEG,jpg,jpeg)," + str(len(self.get_location_samples()))  + " location samples)"

    # TODO: Compléter la méthode _extract_location_sample_from_picture
    @staticmethod
    def _extract_location_sample_from_picture(filename: str):
        """
        Returns the time, latitude, and longitude, if available, from the EXIF data extracted from the file specified by filename
        """
        (t, lat, lng) = (None, None, None)

        with open(filename, 'rb') as f:
            #print("Picture LocationProvider, on lit l'image : " + filename)
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
            ldate = str(date).split(':')
            timestamp = utils.get_if_exists(exif_data, 'GPS GPSTimeStamp')
            #print("date = " + str(date) + " timestamp = " + str(timestamp) + " lat = " + str(lat) + " long = " + str(lng))

            # Si on n'a pas de localisation ou de date dans les données EXIF on ne peut créer de LocationSample
            # On renvoie None, None, None
            if((date == None) or (timestamp == None) or (lat == None) or (lng == None)):
                raise ValueError
                return
            else:
                try:
                    ltimestamp = datetime.strptime(str(timestamp), "[%H, %M, %S]")
                except ValueError as e:
                    #print("bad timestamp value, let's check and fix them in case they are of type exifread.utils.Ratio")
                    #print("that cannot be converted using datetime.strptime(...) ex [9, 9, 645/24]")
                    print("Converted timestamp values from Ratio to int")
                    timestamp = PictureLocationProvider.fix_timestamp_values(timestamp)

                    ltimestamp = datetime.strptime(str(timestamp), "[%H, %M, %S]")

                d = ltimestamp - datetime(1900, 1, 1)
                # TODO: Convertir la date (au format textuel) contenue dans le EXIF tag en datetime et le stocker dans la variable t
                tUTC = datetime(int(ldate[0]), int(ldate[1]), int(ldate[2])) + d
                t = utc2local(tUTC)

        return t, lat, lng

    @staticmethod
    def fix_timestamp_values(timestamp):
        index = 0
        for val in timestamp.values:
            if isinstance(val, exifread.utils.Ratio):
                timestamp.values[index] = PictureLocationProvider.ratio_to_int(val);
            index = index + 1
        timestamp.printable = str(timestamp.values)
        return timestamp

    @staticmethod
    def ratio_to_int(ratio):
         # Takes exif tag value ratio as input and outputs float

            if not isinstance(ratio, exifread.utils.Ratio):
                raise ValueError("You passed something to ratio_to_float that isn't "
                     "a GPS ratio.")

            # GPS metadata is given as a number and a density
            return int(ratio.num / ratio.den)


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    Configuration.get_instance().add_element("verbose", True)
    lp = PictureLocationProvider('../data/pics/bhorne')
    print(lp)
    lp.show_location_samples()
    lp2 = PictureLocationProvider('../data/pics/lpalmer')
    print(lp2)
    lp2.show_location_samples()
    # Warning: Skipping file 'unil.jpg' (Missing time and/or location information)
    # PictureLocationProvider(source: '../data/pics/jdoe'(JPG, JPEG, jpg, jpeg), 2 location samples)
    # LocationSample[datetime: 2017-02-21 13:29:04, location: Location [latitude: 46.51744, longitude: 6.56905]]
    # LocationSample[datetime: 2017-03-08 10:36:00, location: Location[latitude: 46.52206, longitude: 6.58417]]
