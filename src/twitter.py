# -*- coding: utf-8 -*-
from location import *
import tweepy
import sys
import time
from configuration import *
import html
from datetime import datetime, timezone, timedelta
import json

# TODO: Définir la classe TwitterLocationProvider
class TwitterLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur où l'on construit une liste de LocationSample
    def __init__(self, name : str, token, token_secret):
        # nom en clair du suspect
        self.__name = name
        self.__token = token
        self.__token_secret = token_secret

        #todo : aller chercher les tweet et appeler extract location sample from tweet FAIRE COMME DANS PICTURES

        # TODO : faire un try / catch et afficher une message d'erreur si on arrive pas à obtenir des infos
        # sur le compte (ex: erreur de connexion twitter)
        # Dans énoncé du projet : Warning: Could not extract teaching isplab ’s Twitter account information ( details sur l’erreur)
        consumer_key = TwitterLocationProvider.__api_key
        consumer_secret = TwitterLocationProvider.__api_key_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # set access token
        auth.set_access_token(self.__token, self.__token_secret)

        client = tweepy.API(auth)
        user = client.me()

        # nom twitter
        self.nom = user.name
        print("Nom twitter :", self.nom)

        public_tweets = client.user_timeline()

        self.__samples = []
        tuple = None

        for tweet in public_tweets:
            try :
                #print(tweet.text)
                tuple = self._extract_location_sample_from_tweet(tweet)
                date = tuple[0]
                lat = tuple[1]
                long = tuple[2]

                ls = LocationSample(date, Location(lat, long), "twitter")
                #print(ls)
                self.__samples.append(ls)
            except ValueError as e:
                print("Warning: Skipping tweet (Missing time and/or location information (" + str(e) + "))")

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
        return "TwitterLocationProvider (user '" + self.__name + "' aka '" + self.nom + "', " +  str(len(self.get_location_samples())) + " location samples)"

    # TODO: Implémenter la méthode _extract_location_sample_from_tweet qui prend en paramètre un tweet et renvoie un tuple (temps, latitude, longitude)
    # Comme pour la méthode de Picture, vérifier que les paramètres sont bien présents dans le tweet
    def _extract_location_sample_from_tweet(self, tweet):
        #print(json.dumps(tweet._json, indent=3))
        #print(tweet._json["created_at"])

        try :
            #date = datetime.strptime(tweet._json["created_at"], "%a %b %d %H:%M:%S +0000 %Y")

            # Les dates des tweets sont dans la timezone UTC, il faut convertir dans la timezone locale
            # au moment du tweet. On utilise pour cela la fonction utc2local récupéré sur le web
            # Voir post 36 de https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime/4771733#4771733
            # la version en bas du post.
            # On a mis la fonction dans utils.py
            dateUTC = tweet.created_at
            print("Date UTC = " + str(dateUTC))
            date = utc2local(dateUTC)

            print("Date local time: " + str(date))

            #lat = tweet.place.bounding_box.coordinates[0][0][1]
            #long = tweet.place.bounding_box.coordinates[0][0][0]
            lat = tweet.coordinates["coordinates"][1]
            long = tweet.coordinates["coordinates"][0]
        except:
            raise ValueError(tweet.id)
            return

        return (date, lat, long)





if __name__ == '__main__':

    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    Configuration.get_instance().add_element("verbose", True)
    TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    lp = TwitterLocationProvider('1_isp','1124333850858074115-q2xK5TcnlRLGMk9QO1vMSi9RTcH6Sk','B8YQzoO01Dze2D3CaJLukuvXKRZn0VtSpPuCtYccdKYSZ')
    print(lp)
    print("-----")
    lp.print_location_samples()
    lp.show_location_samples()

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

