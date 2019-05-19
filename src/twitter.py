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
    def __init__(self, name : str, token, token_secret):
        self.__name = name
        self.__token = token
        self.__token_secret = token_secret

        #todo : aller chercher les tweet et appeler extract location sample from tweet FAIRE COMME DANS PICTURES
        consumer_key = TwitterLocationProvider.__api_key
        consumer_secret = TwitterLocationProvider.__api_key_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # set access token
        auth.set_access_token(self.__token, self.__token_secret)

        client = tweepy.API(auth)

        user = client.me()  # obtenir les information sur l'utilisateur connecté
        print(client, auth)

        self.__samples = []
        #self.__samples = self._extract_location_sample_from_tweet()


        # Appel du constructeur de la classe mere
        super().__init__(self.__samples)



    # TODO: Définir des attributs pour les clefs de l'API ainsi que les setters correspondants
    @classmethod
    def set_api_key(cls, key):
        cls.__api_key = key

    @classmethod
    def set_api_key_secret(cls, key_secret):
        cls.__api_key_secret = key_secret


    # TODO: Redéfinir la méthode str
    def __str__(self):
        return "TwitterLocationProvider (source: " +  str(len(self.get_location_samples())) + " location samples)"

    # TODO: Implémenter la méthode _extract_location_sample_from_tweet qui prend en paramètre un tweet et renvoie un tuple (temps, latitude, longitude)
    # Comme pour la méthode de Picture, vérifier que les paramètres sont bien présents dans le tweet
    def _extract_location_sample_from_tweet(self):



        return []


if __name__ == '__main__':

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    Configuration.get_instance().add_element("verbose", True)
    TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    lp = TwitterLocationProvider('1_isp','1124333850858074115-q2xK5TcnlRLGMk9QO1vMSi9RTcH6Sk','B8YQzoO01Dze2D3CaJLukuvXKRZn0VtSpPuCtYccdKYSZ')



    #lp = TwitterLocationProvider('egravier1994','996422909735391233-kLWsObS61ghUmpgS2ZXTZElQ2n5Tt9Z','BXqtUZI2pBUOgDyOVY21svUHyP8iabA98kdT4GpZlWWNC')
    #lp = TwitterLocationProvider('egravier1994', '996422909735391233-kLWsObS61ghUmpgS2ZXTZElQ2n5Tt9Z',
    #                             'BXqtUZI2pBUOgDyOVY21svUHyP8iabA98kdT4GpZlWWNC')
    #lp = TwitterLocationProvider('egravier1994', 'Z4bLkruoqSp0JXJfJGTaMQEZ',
    #                                                          'gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    # CLES VALIDES ICI (je les ai demandées à twitter), mais le code fourni ne fonctionne pas.
    # exécute testTweepy.py tu va voir, ça ouvre une page Web chez twitter qui affiche un code que tu dois
    # ensuite saisir pour que çà marche... et visiblement le code de tes profs
    # date de l'an dernier et je pense que cela a changé depuis....
    # demande moi ma clé secrete, il ne faut pas la mettre sur github
    #lp = TwitterLocationProvider('egravier1994', 'lSjQ9ctPFYbN4UwAAKPJ2PLIh',)                                                              '')


    #print(lp)
    #lp.print_location_samples()
    #lp.show_location_samples()

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

