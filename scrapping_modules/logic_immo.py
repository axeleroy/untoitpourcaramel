from pprint import pprint

import requests
from datetime import datetime
from bs4 import BeautifulSoup
from models import Annonce

"""Module qui récupère les annonces de Logic-Immo"""

header = {
    'User-Agent': 'logicimmo-android/8.5.1',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def search(parameters):
    # Préparation des paramètres de la requête
    payload = {
        'client': "v8.a.3",
        'price_range': "%s,%s" % (parameters['price'][0], parameters['price'][1]),  # Loyer
        'area_range': "%s,%s" % (parameters['surface'][0], parameters['surface'][1]),  # Surface
        'rooms_range': "%s,%s" % (parameters['rooms'][0], parameters['rooms'][1]),  # Pièces
        'bedrooms_range': "%s,%s" % (parameters['bedrooms'][0], parameters['bedrooms'][1]),  # Chambres
        'localities': ','.join(key for key in search_city_code(parameters['cities']))
    }

    # Insertion des paramètres propres à LeBonCoin
    payload.update(parameters['logic-immo'])

    request = requests.post("http://lisemobile.logic-immo.com/li.search_ads.php", params=payload, headers=header)
    data = request.json()

    for ad in data['items']:

        annonce, created = Annonce.create_or_get(
            id='logic-immo-' + ad['identifiers']['main'],
            site="Logic Immo",
            created=datetime.fromtimestamp(ad['info']['firstOnlineDate']),
            title="%s %s pièces" % (ad['info']['propertyType']['name'], ad['properties']['rooms']),
            description=ad['info']['text'],
            telephone=ad['contact'].get('phone'),
            price=ad['pricing']['amount'],
            surface=ad['properties']['area'],
            rooms=ad['properties']['rooms'],
            bedrooms=ad['properties'].get('bedrooms'),
            city=ad['location']['city']['name'],
            link=ad['info']['link'],
            picture=[picture.replace("[WIDTH]", "1440").replace("[HEIGHT]", "956").replace("[SCALE]", "3.5")
                     for picture in ad.get('pictures')]
        )

        if created:
            annonce.save()


def search_city_code(cities):
    keys = list()

    for city in cities:
        payload = {
            'client': "v8.a",
            'fulltext': city[1]
        }

        request = requests.post("http://lisemobile.logic-immo.com/li.search_localities.php", params=payload,
                                headers=header)
        data = request.json()
        keys.append(data['items'][0]['key'])

    return keys
