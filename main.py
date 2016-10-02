import os
import sys
import models
import trello_config
from scrapping_modules import seloger
from models import Annonce

os.chdir(os.path.dirname(sys.argv[0]))

# region configuration
models.create_tables()

parameters = {
    # ('Ville', Code postal, Code Insee)
    'cities': [
        ('Nanterre', 92000, 920050),
        ('Chaville', 92370, 920022),
        ('Issy les Moulineaux', 92130, 920040),
        ('Montrouge', 92120, 920049),
        ('Saint-Cloud', 92210, 920064),
        ('Meudon', 92190, 920048)
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

_list = trello_config.get_list()
for annonce in Annonce.select().where(Annonce.posted2trello == False):
    title = "%s de %sm² à %s @ %s€" % (annonce.title, annonce.surface, annonce.city, annonce.price)
    description = "Créé le : %s\n>%s\n\n %s pièces, %s chambre(s)\nCharges : %s" % \
                  (annonce.created.strftime("%Y-%m-%d %H:%M:%S"), annonce.description, annonce.rooms, annonce.bedrooms,
                   annonce.charges)

    card = _list.add_card(title, desc=description)

    card.attach(url=annonce.link)
    if annonce.picture:
        card.attach(url=annonce.picture)

    annonce.posted2trello = True
    annonce.save()
