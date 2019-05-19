# -*- coding: utf-8 -*-
import argparse
from datetime import datetime, timedelta, timezone
from suspects import *
from configuration import *

def conversion_date(d) :
    return datetime.strptime(d, "%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    #try:
        DESCRIPTION = "Identifie les suspects les plus plausibles à partir de leurs traces de mobilité (issues de sources " \
                      "multiples incluant les tweets géo-taggés, les traces Wi-Fi et les flux de photos géo-taggées) pour un crime spécifié " \
                      "par une date/heure et une localisation"

        parser = argparse.ArgumentParser(description=DESCRIPTION)

        # TODO: Ajouter les différents arguments de la ligne de commande à l'analyseur "parser"
        parser.add_argument('-v', '--verbose', help = "affiche les détails de l'exécution du programme et les avertissements", required = False, type = bool, default = False)
        parser.add_argument('-s', '--suspect', help = "fichier contenant la liste des suspect.e.s et les sources de données de localisatier", required = True, type = str)
        parser.add_argument('-t', '--twitter_api_key', help = "clé pour l'accès à l'API Twitter", required = True, type = str)
        parser.add_argument('-u', '--twitter_api_key_secret', help = "clé secrète pour l'accès à l'API Twitter",required = True, type = str)
        parser.add_argument('-g', '--google_api_key', help = "clé pour l'accès à l'API Google",required = True, type = str)
        parser.add_argument('-d', '--date', help = "date et heure du crime",required = True, type = str)
        parser.add_argument('-lat', '--latitude', help = "latitude de la scène de crime",required = True, type = float)
        parser.add_argument('-lng', '--longitude', help = "longitude de la scène de crime",required = True, type = float)

        args = parser.parse_args()
        d= args.date
        print("date = " + d)


        # TODO: Stocker les paramètres importants dans un objet Configuration accessible depuis tous les modules du programme
        conf = Configuration()
        conf.add_element("verbose", args.verbose)
        conf.add_element("suspects", args.suspect) #todo : vérifier que le nom du fichier est bien xx.json
        conf.add_element("twitter_api_key", args.twitter_api_key)
        conf.add_element("twitter_api_key_secret", args.twitter_api_key_secret)
        conf.add_element("google_api_key", args.google_api_key)
        date_crime = conversion_date(args.date)
        conf.add_element("date", date_crime)
        conf.add_element("latitude", args.latitude)
        conf.add_element("longitude", args.longitude)
        Location.set_api_key(conf.get_element('google_api_key'))
        lieu_crime = Location(args.latitude, args.longitude)

        #-t Z4bLkruoqSp0JXJfJGTaMQEZo -u gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc -g AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito -lat 46.522662 -lng 6.577305 -d "06/05/2019 10:19:23" -s "../data/suspects.json"

        print(conf)
        '''print(conf)
        print(lieu_crime)
        print(date_crime)'''

        # TODO: Afficher le message d'accueil du logiciel
        print("Investigation liée au crime du " + str(date_crime) + " @" + str(lieu_crime.get_name()))


        # TODO: Lire le fichier suspect, l'analyser, construire les objets Suspect correspondants et les stocker dans une liste. Utiliser les méthodes createObjectFromXMLFile() / createObjectFromJSONFile()
        suspects = Suspect.create_suspects_from_JSON_file(args.suspect)
        print("-------------------------------------------------------------")
        print("### Affichage des suspects et de leurs location providers ###")
        print("-------------------------------------------------------------")
        print('\n'.join(map(str, suspects)))



        # TODO: Pour chaque suspect, déterminer s'il a pu se rendre et repartir du lieu du crime.
        print(" ")
        print("-----------SUSPECTS POSSIBLES POUR LE CRIME :")

        crime = LocationSample(date_crime, lieu_crime)
        #print(crime)


        for s in suspects:
            print()
            print("--------------------------------------")
            print("########### On examine le suspect : ", s.get_name(), "##########")
            print("--------------------------------------")
            clp = s.get_location_provider()

            if clp != [] :
                if clp.could_have_been_there(crime) :
                    # On le met ici car avec True comme second paramètre ça va afficher le chemin
                    #  avant - crime - apres, et si on a pas un avant ou un apres ça buggue
                    ls = clp.show_location_samples(crime, True, s.get_name() + " peut avoir commis le crime !")

                    print("CONCLUSION : ", s.get_name(), "a eu le temps de commettre le crime")
                else :
                    ls = clp.show_location_samples(crime, True, s.get_name() + " n'a pas pu commettre le crime !")

                    print("CONCLUSION : ", s.get_name(), "n'a pas eu le temps de commettre le crime ou bien nous ne disposons pas de suffisement d'information")
            else :
                print("CONCLUSION : ", s.get_name(), "n'a pas de location provider")


    #except Exception as e :
        #print("[Erreur] L’erreur suivante est survenue durant l’exécution du programme : ", e)