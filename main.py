import os
import sys
import json
import models
import trello_module
from scrapping_modules import logic_immo
from scrapping_modules import seloger
from scrapping_modules import leboncoin
from scrapping_modules import pap

os.chdir(os.path.dirname(sys.argv[0]))

models.create_tables()

# Chargement des paramètres de recherche depuis le fichier JSON
with open("parameters.json") as parameters_data:
    parameters = json.load(parameters_data)

# Recherche et insertion en base
logic_immo.search(parameters)
seloger.search(parameters)
leboncoin.search(parameters)
pap.search(parameters)

# Envoi des annonces sur Trello
trello_module.post()
