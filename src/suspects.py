# -*- coding: utf-8 -*-
from location import *
import xml.etree.ElementTree as xml_et
import os
import json
from configuration import *
from twitter import *
from wifi import *
from pictures import *
from logs import *



# TODO: Définir la classe Suspect qui décrit des informations contenues dans un fichier (nom, LocationProvider)
class Suspect:
    # TODO: Implémenter le constructeur et les getters
    def __init__(self, name : str, sources):
        self.__name = name
        self.__sources = sources

    def get_name(self):
        return self.__name

    def get_sources(self):
        return self.__sources


    # TODO: Définir la méthode str pour afficher un Suspect de la manière suivante :
    # [Suspect] Name: jdoe, Location provider: PictureLocationProvider (source: ’ ../ data/pics /jdoe’ (JPG,JPEG,jpg,jpeg), 2 location samples)
    def __str__(self):
        return "[Suspect] Name : " + str(self.__name) + ",Location provider (source : " + str(self.__sources) + ")"

    # TODO: Implémenter une méthode create_suspects_from_XML_file qui prend un nom de fichier XML en paramètre et le parse pour créer une liste de suspects
    # TODO: (Alternative) implémenter une méthode similaire pour les fichiers JSON
    ''''@classmethod
    def create_suspects_from_XML_file(cls, filename):

        list_suspects = []
        # Lire un fichier xml et ajouter les suspects à la liste...
        tree1 = xml_et.parse(filename)
        root = tree1.getroot()
        suspect = root.findall('suspect/name')
        for personne in suspect :
            list_suspects.append(personne.text)
            #for
        return list_suspects'''



    @classmethod
    def create_suspects_from_JSON_file(cls, filename):
        list_suspects = []
        # Lire un fichier json et ajouter les suspects à la liste...
        with open(filename, 'r') as f:
            p = json.load(f)

        for s in p["suspects"]:
            name = s["name"]
            print()
            print("### create_suspects_from_JSON_file on traite le suspect : " + name + " ###")
            print()
            list_lp = []
            try:
                l = s["sources"]
                el = None
                for source in l :
                    if source["type"] == "Twitter" :
                        el = TwitterLocationProvider(name, source["token"], source["token-secret"])
                    elif source["type"] == "Photographs" :
                        el = PictureLocationProvider(source["dir"])
                    elif source["type"] == "Wi-Fi" :
                        el = WifiLogsLocationProvider(source["db"], source["username"])
                    elif source["type"] == "Logs" :
                        el = LogsLocationProvider(source["file"])
                    list_lp.append(el)

                clp = reduce(lambda x, y :CompositeLocationProvider(x, y), list_lp) #composite est une classe

                list_suspects.append(Suspect(name, clp))
            except KeyError:
                print("Le suspect " + name + " n'a pas de sources de LocationProvider associé dans le fichier JSON")
                print()
                list_suspects.append(Suspect(name, []))


        return list_suspects


if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # Configuration.get_instance().add_element("verbose", True)
    #TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    #TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    john = Suspect('Patrick Biales', PictureLocationProvider('../data/pics/biales'))
    print(john)
    #
    # suspects = Suspect.create_suspects_from_XML_file('../data/suspects.xml')
    # print('\n'.join(map(str, suspects)))

    suspects = Suspect.create_suspects_from_JSON_file('../data/suspects.json')
    print("-------------------------------------------------------------")
    print("### Affichage des suspects et de leurs location providers ###")
    print("-------------------------------------------------------------")
    print('\n'.join(map(str, suspects)))

    #john.get_sources()[0].show_location_samples()

    # [Suspect] Name: jdoe, Location provider: PictureLocationProvider (source: '../data/pics/jdoe' (JPG,JPEG,jpg,jpeg), 2 location samples)
    # [Suspect] Name: jdoe, Location provider: CompositeLocationProvider (12 location samples)
    #  +	CompositeLocationProvider (5 location samples)
    # 	 +	WifiLogsLocationProvider (source: '../data/../data/db/wifi.db', user 'jdoe', 3 location samples)
    # 	 +	PictureLocationProvider (source: '../data/../data/pics/jdoe' (JPG,JPEG,jpg,jpeg), 2 location samples)
    #  +	TwitterLocationProvider (user 'teaching_isplab' aka 'Teaching ISPLab UNIL', 7 location samples)
    # [Suspect] Name: bob, Location provider: CompositeLocationProvider (4 location samples)
    #  +	WifiLogsLocationProvider (source: '../data/../data/db/wifi.db', user 'bob', 3 location samples)
    #  +	PictureLocationProvider (source: '../data/../data/pics/Bob' (JPG,JPEG,jpg,jpeg), 1 location samples)
    # [Suspect] Name: alice, Location provider: WifiLogsLocationProvider (source: '../data/../data/db/wifi.db', user 'alice', 3 location samples)
