# -*- coding: utf-8 -*-
import exifread
import time
import itertools


# TODO: Implémenter une fonction indent qui prend en paramètre un texte (sous forme de chaîne de caractère) et un espacement (par défaut '\t') et qui ajoute l'espacement au début de chaque ligne du texte
def indent(txt, space = "\t"):
    l4 = list(txt.split("\n"))
    l5 = list(map(lambda x: space + x, l4))
    return "\n".join(l5)

def dict_factory(cursor, row):
    # Source: https://docs.python.org/3.6/library/sqlite3.html#sqlite3.Connection.row_factory
    # Dictionary factory to be used as a row_factory for SQL connection
    # It enables the use of query results as dictionaries, e.g.,
    # r = con.execute("SELECT age FROM ...).fetchone()"
    # age=r["age"]
    return dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def get_if_exists(data, key, default=None):
    return data[key] if key in data else default

def convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degres in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


if __name__ == '__main__':
    print("zero\n" + indent("one\n" + indent("two\nthree", "\t−")))
