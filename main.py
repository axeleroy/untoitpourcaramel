import os
import sys
import json
import models
import trello_module
import logging
from scrapping_modules import logic_immo
from scrapping_modules import seloger
from scrapping_modules import leboncoin
from scrapping_modules import pap


logging.basicConfig(level=logging.INFO)

os.chdir(os.path.dirname(sys.argv[0]))
models.create_tables()


# Chargement des paramètres de recherche depuis le fichier JSON
with open("parameters.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)

# Recherche et insertion en base
if "logic_immo" in parameters['ad-providers']:
    logging.info("Retrieving from logic_immo")
    logic_immo.search(parameters)

if "seloger" in parameters['ad-providers']:
    logging.info("Retrieving from seloger")
    seloger.search(parameters)

if "leboncoin" in parameters['ad-providers']:
    logging.info("Retrieving from leboncoin")
    leboncoin.search(parameters)

if "pap" in parameters['ad-providers']:
    logging.info("Retrieving from pap")
    pap.search(parameters)

# Envoi des annonces sur Trello
posted = trello_module.post()
logging.info("%s new ads posted to Trello" % posted)
