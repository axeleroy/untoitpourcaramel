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
        'sqs': surface_value(parameters['surface'][0]),  # Surface min
        'sqe': surface_value(parameters['surface'][1]),  # Surface max
        'ros': parameters['rooms'][0],  # Pièces min
        'roe': parameters['rooms'][1],  # Pièces max
        'zipcode': ','.join(str(cp[1]) for cp in parameters['cities']),
        'city': ','.join(cp[0] for cp in parameters['cities'])
    }
    # Insertion des paramètres propres à LeBonCoin
    payload.update(parameters['leboncoin'])

    header = {'User-Agent': 'fr.leboncoin.android , Sony D5803 , 6.0.1',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Connection': 'Keep-Alive',
              'Accept-Encoding': 'gzip'
              }
    # Token de l'application Android Leboncoin
    token = "app_id=leboncoin_android&key=d2c84cdd525dddd7cbcc0d0a86609982c2c59e22eb01ee4202245b7b187f49f1546e5f027d48b8d130d9aa918b29e991c029f732f4f8930fc56dbea67c5118ce"

    request = requests.post("https://mobile.leboncoin.fr/templates/api/list.json", params=payload, headers=header,
                            data=token)
    data = request.json()

    for ad in data['ads']:
        _payload = {'ad_id': ad['list_id']}
        _request = requests.post("https://mobile.leboncoin.fr/templates/api/view.json", params=_payload, headers=header,
                                 data=token)

        _data = _request.json()

        rooms, surface = 0, 0

        for param in _data.get('parameters'):
            if param['id'] == 'rooms':
                rooms = param['value']
            if param['id'] == 'square':
                surface = param['value'].replace(" m²", "")

        annonce, created = Annonce.get_or_create(
            id='lbc-' + _data.get('list_id'),
            defaults={
                'site': "Leboncoin Pro" if ad['company_ad'] == 1 else "Leboncoin Particulier",
                'created': datetime.strptime(_data.get('formatted_date'), "%d/%m/%Y &agrave; %Hh%M"),
                'title': BeautifulSoup(_data.get('subject'), "lxml").text,
                'description': BeautifulSoup(_data.get('body').replace("<br />", "\n"), "lxml").text,
                'telephone': _data.get("phone"),
                'price': _data.get('price').replace(" ", ""),
                'surface': surface,
                'rooms': rooms,
                'city': _data.get('zipcode'),
                'link': "https://www.leboncoin.fr/locations/%s.htm?ca=12_s" % _data.get('list_id'),
                'picture': _data.get('images')
            }
        )

        if created:
            annonce.save()


def surface_value(surface):
    if surface == 0:
        return 0
    elif surface <= 20:
        return 1
    elif surface <= 25:
        return 2
    elif surface <= 30:
        return 3
    elif surface <= 35:
        return 4
    elif surface <= 40:
        return 5
    elif surface <= 50:
        return 6
    elif surface <= 60:
        return 7
    elif surface <= 70:
        return 8
    elif surface <= 80:
        return 9
    elif surface <= 90:
        return 10
    elif surface <= 100:
        return 11
    elif surface <= 110:
        return 12
    elif surface <= 120:
        return 13
    elif surface <= 150:
        return 14
    elif surface <= 300:
        return 15
    else:
        return 16
