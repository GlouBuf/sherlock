# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import folium
import googlemaps
import os
from configuration import *
import tempfile
import pathlib
from math import asin, sqrt, sin, cos, radians
from _datetime import *
import copy
from utils import *
from logging_utils import *


# TODO: Définir la classe Location désignant des objets contenant une latitude et une longitude
class Location():

    # TODO: Implémenter le constructeur et les getters
    def __init__(self, latitude: float, longitude: float):
        if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
            raise Exception("Problème de location")
        self.__latitude = latitude
        self.__longitude = longitude

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    def distance(self, other):
        Rt = 6371
        D = 2 * Rt * asin(sqrt((sin(radians(other.get_latitude()) - radians(self.__latitude)) / 2) ** 2 + cos(radians(self.__latitude)) * cos(radians(other.get_latitude())) * (sin((radians(other.get_longitude()) - radians(self.__longitude)) / 2)) ** 2))
        return D

    # TODO: Créer des attributs *privés* permettant de stocker la clef (api_key) pour l'accès à l'API de Google et l'objet Client (module googlemaps) correspondant (api_client)

    # TODO: Créer la méthode correspondante : set_api_key (*optionnel* : et __check_api_init pour vérifier que les attributs ci-dessus ont bien été initialisés)
       # VOIR DOCUMENTATION ICI : https://github.com/googlemaps/google-maps-services-python qu'on trouve en cherchant
        # sur Google "python googlemaps example". Ensuite à la fois utiliser le debugger pour comprendre
        # le format des résultats mais aussi aller voir la doc de Google sur Geocoding API (adresse dans la doc
        # de la librairie python googlmemaps précédente. Doc Google ici : python googlemaps example
        # https://developers.google.com/maps/documentation/geocoding/start

    @staticmethod
    def set_api_key(key):
        if not Location.__check_api_init():
            #print("INIT")
            Location.__api_key = key
            try :
                log("tentative de connexion à l'api googlemaps ...")
                Location.__gmaps_client = googlemaps.Client(Location.__api_key)
                log("Connecté.")
            except Exception :
                log("Erreur de connexion à google map, clef sans doute invalide : " + str(key))
        else:
            log("Déjà connecté à googlemap.")


    @staticmethod
    def __check_api_init():
        try:
            Location.__api_key
            return True
        except:
            return False

    # TODO: Implémenter la méthode str pour afficher une Location de la forme suivante (en limitant le nombre de décimales à 5)
    # Location [latitude: 48.85479, longitude: 2.34756]
    def __str__(self):
        return "Location [latitude : " + str(self.__latitude) + ", longitude : " + str(self.__longitude) + "]"

    # TODO: Définir une méthode get_name(self) -> str qui retourne, en utilisant l'API Google reverse geocoding, le nom correspondant aux coordonées contenues dans l'objet Location
    # "Avenue de la Gare 46, 1003 Lausanne, Suisse" pour 46.517738, 6.632233
    def get_name(self):
        # VOIR DOCUMENTATION ICI : https://github.com/googlemaps/google-maps-services-python qu'on trouve en cherchant
        # sur Google "python googlemaps example". Ensuite à la fois utiliser le debugger pour comprendre
        # le format des résultats mais aussi aller voir la doc de Google sur Geocoding API (adresse dans la doc
        # de la librairie python googlmemaps précédente. Doc Google ici : python googlemaps example
        # https://developers.google.com/maps/documentation/geocoding/start

        #googlemaps.configure(self.__api_key)
        lat = self.__latitude
        long = self.__longitude
        log("Utilisation du service de reverse geocoding avec longitude/latitude ...")
        adresse = None

        try :
            destination = Location.__gmaps_client.reverse_geocode((lat, long))
            adresse = destination[0]["formatted_address"] + "," + " pour " + str(lat) + ", " + str(long)
            log("Adresse obtenue : " + str(adresse))
        except Exception :
            log("Impossible de se connecter au service.")

        return adresse


    # TODO: Implémenter la méthode get_travel_distance_and_time qui renvoie le couple (distance, temps) pour atteindre le lieu correspondant à un autre objet Location
    def get_travel_distance_and_time(self, other):
        log("Calcul de la distance et du temps pour aller de : " + str(self) + " à " + str(other))
        latlong_arrivee = (self.__latitude, self.__longitude)
        latlong_depart = (other.__latitude, other.__longitude)
        arrivee = [latlong_arrivee]
        depart = [latlong_depart]
        distance = None
        temps_reel = None

        log("Connexion au service  distance_matrix ...")
        try :
            results = Location.__gmaps_client.distance_matrix(origins=depart, destinations=arrivee, mode="walking")
            # print(results)
            distance = results['rows'][0]['elements'][0]['distance']['value'] #en m
            temps = results['rows'][0]['elements'][0]['duration']['value'] #en seconde
            temps_reel = temps / 2

            log("distance = " + str(distance) + " et Temps = " + str(temps_reel))

            return (distance, temps_reel)
        except Exception :
            log("Impossible d'utiliser distance_matrix.")


# TODO: Définir la classe LocationSample désignant des objets contenant un datetime et un objet Location
class LocationSample():
    # TODO: Implémenter le constructeur ainsi que les getters
    # TODO: Définir les opérateurs de comparaison
    def __init__(self, date : datetime, location : Location, source = None, imageURL = None):
        if not isinstance(date, datetime) :
            raise Exception
        elif not isinstance(location, Location) :
            raise Exception
        self.__date = date
        self.__location = location

        self.__source = source
        self.__imageURL = imageURL

    def __str__(self):
        state = "LocationStample [datetime : " + self.__date.strftime("%d-%m-%Y, à %H:%M:%S") + ", Location [" + str(self.__location) + "]]"
        return state

    def get_timestamp(self):
        return self.__date

    def get_location(self):
        return self.__location

    def get_source(self):
        return  self.__source

    def spatial_distance(self, other):
        return other.distance(self.__location)

    def __eq__(self, other):
        if other == None :
            return  False

        if isinstance(other, LocationSample):
            if self.__date - other.get_timestamp() == 0 :
                return self.__date, " = ", other.get_timestamp()
            else:
                return self.__date, "≠", other.get_timestamp()
        else:
            raise TypeError("mauvaise valeur")

    def __lt__(self, other):
        if isinstance(other, LocationSample):
            if self.__date - other.get_timestamp() < timedelta(0):
                return True
            else:
                return False
        else:
            raise TypeError("mauvaise valeur")

    def __gt__(self, other):
        return not self.__lt__(other)

    def __ge__(self, other):
        if self.__gt__(other) or self.__eq__(other) == True :
            return True
        else :
            return False

    def __le__(self, other):
        if self.__lt__(other) or self.__eq__(other) == True :
            return True
        else :
            return False


    '''renvoie une représentation HTML de l’objet LocationSample'''
    def get_description(self):
        #stateHTML = "LocationStample [datetime : " + self.__date.strftime("%d-%m-%Y, à %H:%M:%S") + ", Location [" + str(self.__location) + "]]"

        stateHTML = "<ul><li><b>Date</b> : " + self.__date.strftime("%d-%m-%Y, à %H:%M:%S")
        stateHTML = stateHTML + "</li><li><b>Position</b> : Lng : " + str(self.__location.get_longitude())
        stateHTML = stateHTML + " Lat : " +  str(self.__location.get_latitude()) + "</li></ul>"

        if self.__imageURL != None :
            stateHTML = stateHTML + "<img src= '"+ os.getcwd() + "/" + self.__imageURL + "' width=200 >"

        return stateHTML




# TODO: Définir la classe abstraite LocationProvider qui permet de produire une liste d'objets LocationSample
class LocationProvider():
    app = None
    web = None

    # TODO: Définir le constructeur de la classe abstraite
    def __init__(self):
        pass

    # TODO: Définir la méthode str de sorte à afﬁcher un objet LocationProvider sous la forme suivante :
    # LocationProvider (5 location samples)
    def __str__(self):
        return self.__class__.__name__ + " (" + str(len(self.get_location_samples())) + " location samples)"

    def __add__(self, other):
        if isinstance(other, LocationProvider) :
            return CompositeLocationProvider(self, other)
        else :
            raise TypeError

    # TODO: Spécifier l'existence d'une méthode abstraite get_location_samples
    def get_location_samples(self):
        raise NotImplementedError

    # TODO: Implémenter la méthode print_location_samples en utilisant get_location_samples (renvoyant une liste de LocationSample), qui renvoie une chaîne de caractères décrivant des objets LocationSamples
    def print_location_samples(self):
        print("\n".join(map(str, self.get_location_samples())))

    # Fournie
    def show_location_samples(self, marker: LocationSample = None, showPath=False, title=None):
        if self.__class__.app is None:
            self.__class__.app = QApplication([])
            self.__class__.web = QWebEngineView()

        samples = self.get_location_samples()
        if len(samples) == 0:
            return

        #for s in samples:
        #    print(s.get_location())

        coordinates = [(sample.get_location().get_latitude(), sample.get_location().get_longitude()) for sample in
                       samples]
        timestamps = [sample.get_timestamp() for sample in samples]
        data = [sample.get_description() for sample in samples]
        source = [sample.get_source() for sample in samples]

        # Creating the html map, zoom in location defined by the first coordinate
        map_ = folium.Map(location=coordinates[0], zoom_start=15, detect_retina=False,
                          API_key='pk.eyJ1IjoiaXNwbGFiLXVuaWwiLCJhIjoiY2oxeGl4eTFuMDAwYTJxbzB0bXg1dmxzcCJ9.d14dldYH5NpracBPF3X4pg',
                          tiles='https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaXNwbGFiLXVuaWwiLCJhIjoiY2oxeGl4eTFuMDAwYTJxbzB0bXg1dmxzcCJ9.d14dldYH5NpracBPF3X4pg',
                          attr='Mapbox')

        folium.PolyLine(locations=coordinates).add_to(map_)  # draw a line connecting all the points

        for i in range(0, len(coordinates)):
            popup = folium.Popup(folium.Html(
                '<strong>%s</strong></br> Source: %s' % (timestamps[i].strftime('%Y-%m-%d at %I:%M:%S%p %Z'), source[i] + data[i]),
                script=True))
            folium.Marker(coordinates[i], popup=popup).add_to(map_)  # put markers on each and annotate with timestamps

        if marker is not None:
            coordinate = (marker.get_location().get_latitude(), marker.get_location().get_longitude())
            popup = folium.Popup(folium.Html('<strong>%s</strong></br>%s' % (
                marker.get_timestamp().strftime('%Y-%m-%d at %I:%M:%S%p %Z'), marker.get_description()), script=True))
            folium.Marker(coordinate, popup=popup, icon=folium.Icon(color='red')).add_to(map_)
            coordinates.append(coordinate)

            if showPath:
                # get LocationSamples right before and right after
                (ls_before, ls_after) = self.get_surrounding_temporal_location_samples(marker.get_timestamp())

                # determine the compatibility based on the time needed and the actual time (elapsed)

                # If one is none we can't display
                if(ls_before == None or ls_after == None):
                    return

                dt_before_actual = marker.get_timestamp() - ls_before.get_timestamp()
                _, dt_before_needed = ls_before.get_location().get_travel_distance_and_time(marker.get_location())

                dt_after_actual = ls_after.get_timestamp() - marker.get_timestamp()
                _, dt_after_needed = marker.get_location().get_travel_distance_and_time(ls_after.get_location())

                for s, ls, dt_actual, dt_needed in [('vers', ls_before, dt_before_actual, dt_before_needed),
                                                    ('depuis', ls_after, dt_after_actual, dt_after_needed)]:
                    popup = folium.Popup(folium.Html(
                        'Temps %s le lieu du crime :</br><ul style="margin-left:-2em;"><li>Réel : %s</li><li>Google Maps : %s</li></ul>' % (
                            s, dt_actual, dt_needed), script=True))

                    folium.PolyLine(popup=popup,
                                    locations=[
                                        (sample.get_location().get_latitude(), sample.get_location().get_longitude())
                                        for sample in [ls, marker]], color='red', weight=2).add_to(map_)

        map_.fit_bounds(coordinates)

        # path = os.path.abspath('./map.html')
        (_, path) = tempfile.mkstemp()
        if Configuration.get_instance().get_element("verbose", False):
            print('Creating temporary file for the map to be displayed \'{:s}\''.format(path), file=sys.stderr)
        map_.save(path)
        url = pathlib.Path(os.path.abspath(path)).as_uri()

        self.__class__.web.setWindowTitle('Trace de mobilité' + (' (' + title + ')' if title is not None else ''))
        self.__class__.web.load(QUrl(url))
        self.__class__.web.show()
        status = self.__class__.app.exec_()

        if status != 0 and Configuration.get_instance().get_element("verbose", False):
            print('Warning: The QApplication displaying the web-based map finished with exit code {:d}'.format(status),
                  file=sys.stderr)

        try:
            os.unlink(path)
        except Exception as e:
            if Configuration.get_instance().get_element("verbose", False):
                print('Warning: An error as occured while removing a temporary file ({:s})'.format(str(e)),
                      file=sys.stderr)

    # TODO: Implémenter la méthode get_surrounding_temporal_location_samples qui prend en paramètre un datetime et renvoie les objets LocationSample (via get_location_samples) situés juste avant et après le datetime
    def get_surrounding_temporal_location_samples(self, date : datetime):
        # on recupère les LocationSample
        ls = self.get_location_samples()
        ls.sort()
        #liste contenant les LS avant ou apres date
        avant = list(filter(lambda x: x.get_timestamp() < date, ls))
        apres = list(filter(lambda x: x.get_timestamp() > date, ls))

        if len(avant) != 0 and len(apres) != 0 :
            # renvoie l'élément juste avant et celui juste après date
            return (avant[-1], apres[0])
        elif len(apres) == 0 :
            return (avant[-1], None)
        else :
            return (None, apres[0])


    # TODO: Implémenter la méthode could_have_been_there qui prend en paramètre un LocationSample et renvoie si un suspect a eu le temps de s'y rendre
    def could_have_been_there(self, crime : LocationSample):
        # crime = la date et le lieu du crime
        lieu_crime = crime.get_location()
        date_crime = crime.get_timestamp()

        # Plus proches LocationSample d'un suspect (ceux qui sont juste avant et après la date du crime)
        plusproche_ls = self.get_surrounding_temporal_location_samples(date_crime)


        # Calcul des temps pour que ces suspects aient pu se rendre sur le lieu/date du crime
        ls1 = plusproche_ls[0]
        ls2 = plusproche_ls[1]

        print("Avant :", ls1)
        print("Date et lieu du crime : ", date_crime, lieu_crime)
        print("Après :", ls2)
        print("-----")

        if (ls1 == None or ls2 == None) :
            return False

        try :
            #calcul du temps pour aller de avant jusqu'au lieu du crime
            dist_et_temps1 = ls1.get_location().get_travel_distance_and_time(lieu_crime)
            temps1 = dist_et_temps1[1]

            #calcul du temps pour aller du crime à après
            dist_et_temps2 = lieu_crime.get_travel_distance_and_time(ls2.get_location())
            temps2 = dist_et_temps2[1]

            #temps entre avant et crime
            delta_t1 = (crime.get_timestamp() - ls1.get_timestamp()).total_seconds()

            #temps entre crime et après
            delta_t2 = (ls2.get_timestamp() - crime.get_timestamp()).total_seconds()

            # on renvoie true si on a eu le temps pour aller jusqu'au crime et le temps pour en revenir
            #sinon on renvoie false
            print("temps1 gmap pour déplacement de avant jq crime) =", sec2time(temps1), "delta_t1 (date crime - date avant) =", sec2time(delta_t1))
            possible1 = (temps1 - delta_t1) < 0

            if(possible1):
                msg1 = "POSSIBLE"
            else:
                msg1 = "IMPOSSIBLE"

            print("Déplacement avant -> crime", msg1, "(" + sec2time(temps1) + " < " + sec2time(delta_t1))


            print("temps2 gmap pour déplacement crime jq après) =", sec2time(temps2), "delta_t2 (date après - date crime) =", sec2time(delta_t2))
            possible2 = (temps2 - delta_t2) < 0

            if (possible2):
                msg2 = "POSSIBLE"
            else:
                msg2 = "IMPOSSIBLE"

            print("Déplacement crime -> après", msg2, "(" + sec2time(temps2) + " < " + sec2time(delta_t2))
        except Exception :
            log("Impossible de calculer la distance et le temps.")
            return False


        # Crime possible pour ce suspect si il a pu se rendre de avant jq crime et de crime jq apres
        return (possible1 and possible2)





# TODO: Créer une classe qui implémente le patron de conception Composite pour la classe LocationProvider
# La classe CompositeLocationProvider contient "deux" LocationProvider
class CompositeLocationProvider(LocationProvider):
    # TODO: Définir le constructeur
    def __init__(self, lp1 : LocationProvider, lp2 : LocationProvider):
        super().__init__()
        self.__lp1 = lp1
        self.__lp2 = lp2

    # TODO: Implémenter la méthode get_location_samples
    def get_location_samples(self):
        liste = self.__lp1.get_location_samples() + self.__lp2.get_location_samples()
        liste.sort()
        return liste



    # TODO: Définir la méthode str
    def __str__(self):
        ls = self.get_location_samples()
        # Pour avoir un affichage comme dans l'énoncé, il faudra que les sous classe de LocationProvider
        # redéfinissent __str__
        return "CompositeLocationProvider (" + str(len(self.get_location_samples())) + " location samples)" + \
               "\n" + indent(str(self.__lp1)) + "\n" + indent(str(self.__lp2))



# TODO: Implémenter la classe ListLocationProvider
class ListLocationProvider(LocationProvider):
    # TODO: Définir le constructeur contenant une liste de LocationSample
    def __init__(self, list_location_samples):
        list_location_samples.sort()
        self.__list_location_samples = list_location_samples

    # TODO: Implémenter la méthode get_location_samples qui renvoie la liste de LocationSample
    def get_location_samples(self):
        return copy.deepcopy(self.__list_location_samples)

if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # Configuration.get_instance().add_element("verbose", True)
    Configuration.get_instance().add_element("verbose", True)

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # -t Z4bLkruoqSp0JXJfJGTaMQEZo -u gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc -g AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito -lat 46.522662 -lng 6.577305 -d "06/05/2019 10:19:23" -s "../data/suspects.json"

    Location.set_api_key("AAIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito")


    paris = Location(48.854788, 2.347557)

    print("--- TEST DE LA REVERSE GEOLOCALISATION methode get_name() de la classe Location ---")
    lausanne = Location(46.517738, 6.632233)
    print(lausanne.get_name())
    print("-----")

    print("-----test get travel")
    print(lausanne.get_travel_distance_and_time(paris))
    print("-----")


    sample1 = LocationSample(datetime(2017, 3, 3, 12, 25), paris)
    '''print(sample1.get_location())
    print(sample1.get_timestamp())
    print(sample1)
    print("HTML : " + sample1.get_description())'''

    sample2 = LocationSample(datetime(2017, 3, 3, 14, 56, 5), lausanne)
    #print(sample1 < sample2)

    a = [sample2, sample1]
    a.sort()

    #print([str(x) for x in a])

    crime = LocationSample(datetime(2017, 3, 31, 18, 30, 20), Location(46.520336, 6.572844))
    #print(crime.get_location().get_travel_distance_and_time(Location(46.521045, 6.574664)))

    locationsamples = ListLocationProvider([sample1, sample2])
    #print(locationsamples.get_location_samples())

    #locationsamples.show_location_samples()
    result = locationsamples.get_surrounding_temporal_location_samples(crime.get_timestamp())

    print("avant : ", result[0])
    print("apres : ", result[1])


    # Test composite
    locationsamples2 = ListLocationProvider([crime])

    clp = CompositeLocationProvider(locationsamples, locationsamples2)
    print(clp)

    # Test du add sur LocationProvider, doir renvoyer un composite
    locationsamples3 = locationsamples + clp
    print(locationsamples3)

    #print(locationsamples + locationsamples)

    # Avenue de la Gare 46, 1003 Lausanne, Suisse
    # Location [latitude: 48.85479, longitude: 2.34756]
    # 2017-03-03 12:25:00
    # LocationSample [datetime: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]
    # True
    # ['LocationSample [datetime: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]', 'LocationSample [datetime: 2017-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]']
    # (179, datetime.timedelta(0, 131))
    # [LocationSample [datetime: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]], LocationSample [datetime: 2017-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]]
    # CompositeLocationProvider (4 location samples)
    #  +	ListLocationProvider (2 location samples)
    #  +	ListLocationProvider (2 location samples)
