# -*- coding: utf-8 -*-
from location import *
import tweepy
import sys
import time
from configuration import *
import html
from datetime import datetime, timezone, timedelta

# TODO: Définir la classe TwitterLocationProvider
class TwitterLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur où l'on construit une liste de LocationSample
    def __init__(self, key, key_secret):
        self.__key = key
        self.__key_secret = key_secret

    # TODO: Définir des attributs pour les clefs de l'API ainsi que les setters correspondants
    def set_api_key(self, ):


    def set_api_key_secret():
        pass


    # TODO: Redéfinir la méthode str
    def __str__():
        pass

    # TODO: Implémenter la méthode _extract_location_sample_from_tweet qui prend en paramètre un tweet et renvoie un tuple (temps, latitude, longitude)
    # Comme pour la méthode de Picture, vérifier que les paramètres sont bien présents dans le tweet
    def _extract_location_sample_from_tweet():
        pass



if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # Configuration.get_instance().add_element("verbose", True)
    # TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    # TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')
    #
    #lp = TwitterLocationProvider('teaching_isplab', '842358721544101888-iYq4rs0UrXRkI0xHoO2AFp6LWPU0RgN', 'jeLmhcYrzcNDWthJMYywXMTqxlEw5MQ2eT8niDXUoNmbf')
    # lp = TwitterLocationProvider('egravier1994','996422909735391233-kLWsObS61ghUmpgS2ZXTZElQ2n5Tt9Z','BXqtUZI2pBUOgDyOVY21svUHyP8iabA98kdT4GpZlWWNC')
    # print(lp)
    # lp.print_location_samples()
    # lp.show_location_samples()

    # Warning: Skipping tweet (Missing time and/or location information (996680525313200128))
    # TwitterLocationProvider (user 'egravier1994' aka 'Émile Gravier', 11 location samples)
    # LocationSample [datetime: 2018-05-16 09:11:19+00:00, location: Location [latitude: 46.52102, longitude: 6.57430]]
    # LocationSample [datetime: 2018-05-16 09:12:42+00:00, location: Location [latitude: 46.52108, longitude: 6.57451]]
    # LocationSample [datetime: 2018-05-16 09:13:57+00:00, location: Location [latitude: 46.52110, longitude: 6.57512]]
    # LocationSample [datetime: 2018-05-16 09:15:02+00:00, location: Location [latitude: 46.52092, longitude: 6.57585]]
    # LocationSample [datetime: 2018-05-16 09:16:50+00:00, location: Location [latitude: 46.52030, longitude: 6.57656]]
    # LocationSample [datetime: 2018-05-16 09:23:08+00:00, location: Location [latitude: 46.52085, longitude: 6.57820]]
    # LocationSample [datetime: 2018-05-16 09:24:40+00:00, location: Location [latitude: 46.52144, longitude: 6.57789]]
    # LocationSample [datetime: 2018-05-16 09:26:15+00:00, location: Location [latitude: 46.52246, longitude: 6.57951]]
    # LocationSample [datetime: 2018-05-16 09:27:03+00:00, location: Location [latitude: 46.52246, longitude: 6.57951]]
    # LocationSample [datetime: 2018-05-16 09:28:04+00:00, location: Location [latitude: 46.52259, longitude: 6.57958]]
    # LocationSample [datetime: 2018-05-16 09:29:11+00:00, location: Location [latitude: 46.52266, longitude: 6.58023]]

