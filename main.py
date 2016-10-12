import os
import sys
import models
import trello_module
from scrapping_modules import seloger
from scrapping_modules import leboncoin

os.chdir(os.path.dirname(sys.argv[0]))

# region configuration
models.create_tables()

parameters = {
    # ('Ville', Code postal, Code Insee)
    'cities': [
        ('Nanterre', 92000, 920050),
        ('Chaville', 92370, 920022),
        ('Issy-les-Moulineaux', 92130, 920040),
        ('Montrouge', 92120, 920049),
        ('Saint-Cloud', 92210, 920064),
        ('Meudon', 92190, 920048),
        ('Rueil-Malmaison', 92500, 920063)
    ],
    # (min, max)
    'price': (200, 950),
    'surface': (25, 70),
    'rooms': (2, 5),
    'bedrooms': 1,
}
# endregion

# Recherche et insertion en base
seloger.search(parameters)
leboncoin.search(parameters)

# Envoi des annonces sur Trello
trello_module.post()
