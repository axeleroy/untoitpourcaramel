import configparser
from trello import TrelloClient
from models import Annonce
from ast import literal_eval

def get_list():
    '''
    Retourne la liste Trello indiquée dans trello.ini
    '''

    config = configparser.ConfigParser()
    config.read('trello.ini')

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
        print("List " + config['TRELLO']['ListName'] + " not found on board " + config['TRELLO']['BoardName'] + ".")
        exit()

    return list

def post():
    '''
    Poste les annonces sur Trello
    '''

    _list = get_list()
    for annonce in Annonce.select().where(Annonce.posted2trello == False):
        title = "%s de %sm² à %s @ %s€" % (annonce.title, annonce.surface, annonce.city, annonce.price)
        description = "Créé le : %s\n\n>%s\n\n %s pièces, %s chambre(s)\nCharges : %s" % \
                      (annonce.created.strftime("%Y-%m-%d %H:%M:%S"), annonce.description, annonce.rooms,
                       annonce.bedrooms,
                       annonce.charges)

        card = _list.add_card(title, desc=description)

        card.attach(url=annonce.link)

        # On s'assure que ce soit bien un tableau
        if annonce.picture is not None and annonce.picture.startswith("["):
            # Conversion de la chaîne de caractère représentant le tableau d'images en tableau
            for picture in literal_eval(annonce.picture):
                card.attach(url=picture)
        # Il n'y a qu'une photo
        elif annonce.picture is not None and annonce.picture.startswith("http"):
            card.attach(url=annonce.picture)

        annonce.posted2trello = True
        annonce.save()
