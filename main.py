import models
import configparser
from scrapping_modules import seloger
from models import Annonce
from trello import TrelloClient

# region configuration
models.create_tables()
config = configparser.ConfigParser()
config.read('trello.ini')

parameters = {
    # ('Ville', Code postal, Code Insee)
    'cities': [
        ('Nanterre', 92000, 920050),
        ('Chaville', 92370, 920022),
        ('Issy les Moulineaux', 92130, 920040),
        ('Montrouge', 92120, 920049)
    ],
    # (min, max)
    'price': (200, 950),
    'surface': (25, 70),
    'rooms': (2, 5),
    'bedrooms': 1,
}

trello = TrelloClient(
    api_key=config['TRELLO']['ApiKey'],
    api_secret=config['TRELLO']['ApiSecret'],
    token=config['TRELLO']['Token'],
    token_secret=config['TRELLO']['TokenSecret']
)

for b in trello.list_boards():
    if b.name == config['TRELLO']['BoardName']:
        board = b
        break

if not board:
    print("Board " + config['TRELLO']['BoardName'] + " not found.")
    exit()

for l in board.all_lists():
    if l.name == config['TRELLO']['ListName']:
        list = l
        break

if not list:
    print("List " + config['TRELLO']['ListName'] + " not found on board " + config['TRELLO']['BoardName'] +".")
    exit()
# endregion

# Recherche et insertion en base
seloger.search(parameters)

for annonce in Annonce.select().where(Annonce.posted2trello == False):
    card = list.add_card(
        annonce.title + " de " + str(annonce.surface) + "m² à " + annonce.city + " @ " + str(annonce.price) + "€",
        "Créé le : " + annonce.created.strftime("%Y-%m-%d %H:%M:%S") + "\n>" +
        annonce.description + "\n" +
        annonce.rooms + " pièces, " + annonce.bedrooms + " chambre(s)\n" +
        "Charges : " + str(annonce.charges) if type(annonce.charges) == "NoneType" else "N/A"
    )

    card.attach(url=annonce.link)
    if annonce.picture:
        card.attach(url=annonce.picture)

    annonce.posted2trello = True
    annonce.save()