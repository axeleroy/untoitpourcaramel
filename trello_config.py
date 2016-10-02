import configparser
from trello import TrelloClient

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