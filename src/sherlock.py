# -*- coding: utf-8 -*-
import argparse
from datetime import datetime, timedelta, timezone
'''from suspects import *
from configuration import *'''

if __name__ == '__main__':
    # try:

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

    '''args = parser.parse_args()
    d= args.date
    print("date = " + d)'''



    # TODO: Stocker les paramètres importants dans un objet Configuration accessible depuis tous les modules du programme

    # TODO: Afficher le message d'accueil du logiciel

    # TODO: Lire le fichier suspect, l'analyser, construire les objets Suspect correspondants et les stocker dans une liste. Utiliser les méthodes createObjectFromXMLFile() / createObjectFromJSONFile()

    # TODO: Pour chaque suspect, déterminer s'il a pu se rendre et repartir du lieu du crime.
