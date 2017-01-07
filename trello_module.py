import json
from trello import TrelloClient
from models import Annonce
from ast import literal_eval


def get_board():
    '''
    Retourne la liste Trello indiquée dans trello.ini
    '''

    # Chargement des paramètres et identifiants Trello depuis le fichier JSON
    with open("trello.json") as parameters_data:
        config = json.load(parameters_data)

    trello = TrelloClient(
        api_key=config['ApiKey'],
        api_secret=config['ApiSecret'],
        token=config['Token'],
        token_secret=config['TokenSecret']
    )

    for b in trello.list_boards():
        if b.name == config['BoardName']:
            return b

    print("Board " + config['BoardName'] + " not found.")
    exit()


def get_list(site):
    board = get_board()

    for l in board.all_lists():
        if l.name == site:
            return l

    # Liste pas trouvée, on la crée
    return board.add_list(site)

def post():
    '''
    Poste les annonces sur Trello
    '''

    for annonce in Annonce.select().where(Annonce.posted2trello == False).order_by(Annonce.site.asc()):
        title = "%s de %sm² à %s @ %s€" % (annonce.title, annonce.surface, annonce.city, annonce.price)
        description = "Créé le : %s\n\n" \
                      "%s pièces, %s chambre(s)\n" \
                      "Charges : %s\n" \
                      "Tel : %s\n\n" \
                      ">%s" % \
                      (annonce.created.strftime("%a %d %b %Y %H:%M:%S"), annonce.rooms, annonce.bedrooms, annonce.charges,
                       annonce.telephone, annonce.description.replace("\n", "\n>"))

        card = get_list(annonce.site).add_card(title, desc=description)

        # On s'assure que ce soit bien un tableau
        if annonce.picture is not None and annonce.picture.startswith("["):
            # Conversion de la chaîne de caractère représentant le tableau d'images en tableau
            for picture in literal_eval(annonce.picture):
                card.attach(url=picture)
            # Il n'y a qu'une photo
        elif annonce.picture is not None and annonce.picture.startswith("http"):
            card.attach(url=annonce.picture)

        card.attach(url=annonce.link)

        annonce.posted2trello = True
        annonce.save()
