import requests
from datetime import datetime
from bs4 import BeautifulSoup
from models import Annonce

"""Module qui récupère les annonces de LeBonCoin"""


def search(parameters):
    # Préparation des paramètres de la requête
    payload = {
        'mrs': parameters['price'][0],  # Loyer min
        'mre': parameters['price'][1],  # Loyer max
        'sqs': round(parameters['surface'][0]),  # Surface min
        'sqe': round(parameters['surface'][1]),  # Surface max
        'ret': list(range(parameters['rooms'][0], parameters['rooms'][1] + 1)),  # Pièces
        'zipcode': ','.join(str(cp[1]) for cp in parameters['cities']),
        'city': ','.join(cp[0] for cp in parameters['cities']),

        'c': '10',  # Locations
        # ¯\_(ツ)_/¯
        'ca': '12_s',
        'w': '1',
        'f': 'a',
        'sp': '0',
    }

    header = {'User-Agent': 'fr.leboncoin.android , Sony D5803 , 6.0.1',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Connection': 'Keep-Alive',
              'Accept-Encoding': 'gzip'
              }
    # Token de l'application Android Leboncoin
    body = "app_id=leboncoin_android&key=d2c84cdd525dddd7cbcc0d0a86609982c2c59e22eb01ee4202245b7b187f49f1546e5f027d48b8d130d9aa918b29e991c029f732f4f8930fc56dbea67c5118ce"

    request = requests.post("https://mobile.leboncoin.fr/templates/api/list.json", params=payload, headers=header,
                            data=body)
    data = request.json()

    for ad in data['ads']:
        _payload = {'ad_id': ad['list_id']}
        _request = requests.post("https://mobile.leboncoin.fr/templates/api/view.json", params=_payload, headers=header,
                                 data=body)

        _data = _request.json()

        rooms, surface = 0, 0

        for param in _data.get('parameters'):
            if param['id'] == 'rooms':
                rooms = param['value']
            if param['id'] == 'square':
                surface = param['value'].replace(" m&sup2;", "")

        annonce, created = Annonce.create_or_get(
            id='lbc-' + _data.get('list_id'),
            site='lbc',
            created=datetime.strptime(_data.get('formatted_date'), "%d/%m/%Y &agrave; %Hh%M"),
            # Utilisation de BeautifulSoup pour retirer tout le formatage HTML
            title=BeautifulSoup(_data.get('subject'), "lxml").text,
            description=BeautifulSoup(_data.get('body'), "lxml").text,
            price=_data.get('price'),
            surface=surface,
            rooms=rooms,
            city=_data.get('zipcode'),
            link="https://www.leboncoin.fr/locations/%s.htm?ca=12_s" % _data.get('list_id'),
            picture=_data.get('images')
        )

        if created:
            annonce.save()
