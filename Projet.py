import suspects
from location import *
from pictures import *
import xml.etree.ElementTree as xml_et
import os
import json
from configuration import *

# TODO: Définir la classe Suspect qui décrit des informations contenues dans un fichier (nom, LocationProvider)
class Suspect():
    def __init__(self, nom : str):
        self.__nom = nom
    # TODO: Implémenter le constructeur et les getters

    # TODO: Définir la méthode str pour afficher un Suspect de la manière suivante :
    # [Suspect] Name: jdoe, Location provider: PictureLocationProvider (source: ’ ../ data/pics /jdoe’ (JPG,JPEG,jpg,jpeg), 2 location samples)

    # TODO: Implémenter une méthode create_suspects_from_XML_file qui prend un nom de fichier XML en paramètre et le parse pour créer une liste de suspects
    # TODO: (Alternative) implémenter une méthode similaire pour les fichiers JSON
    def create_suspects_from_XML_file():
        pass

    def create_suspects_from_JSON_file():
        pass


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    # Configuration.get_instance().add_element("verbose", True)
    #TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    #TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    #john = Suspect('jdoe', PictureLocationProvider('../data/pics/jdoe'))
    #print(john)

    #suspects = Suspect.create_suspects_from_XML_file('../data/suspects.xml')
    #print('\n'.join(map(str, suspects)))

    #suspects = Suspect.create_suspects_from_JSON_file('../data/suspects.json')
    #print('\n'.join(map(str, suspects)))

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
