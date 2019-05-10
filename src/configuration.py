# -*- coding: utf-8 -*-
import utils


# TODO: Créer une classe Configuration contenant:
#           -une structure de données adéquate pour stocker des couples clefs-valeurs pour les paramètres de configuration
#           -une méthode add_element pour ajouter un nouvel élément
#           -une méthode get_element pour récupérer la valeur d'un paramètre à partir de sa clef
# TODO: Utiliser le patron de conception Singleton pour cette classe, pour manipuler la configuration de manière globale dans tout le programme

class Configuration:
    __instance = None
    def __init__(self):
        self.__store = {}

    def add_element(self, key, valeur):
        self.__store[key] = valeur

    def get_element(self, key, default = None):
        if key in self.__store.keys() :
            return self.__store[key]
        else :
            return default

    def __str__(self):
        return str(self.__store)

    @classmethod
    def get_instance(cls):
        if cls.__instance == None :
            cls.__instance = Configuration()
        return cls.__instance



if __name__ == '__main__':
    conf = Configuration.get_instance()
    conf.add_element('verbose', True)
    conf.add_element('N', 6)
    print(conf)

    max = conf.get_element('max', 42)
    print(max, conf.get_element('nax'), conf.get_element('verbose'))

    print(conf == Configuration.get_instance())

    # {'verbose': True, 'N': 6}
    # 42 None True
    # True
