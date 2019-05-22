from configuration import *

def log(str) :
    verbose = Configuration.get_instance().get_element('verbose')

    if verbose :
        print(str)