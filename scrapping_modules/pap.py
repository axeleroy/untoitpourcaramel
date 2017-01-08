import requests
from urllib.parse import unquote, urlencode
from datetime import datetime
from models import Annonce

"""Module qui récupère les annonces de PAP"""

header = {
    'X-Device-Gsf': '36049adaf18ade77',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def search(parameters):
    # Préparation des paramètres de la requête
    payload = {
        'recherche[prix][min]': parameters['price'][0],  # Loyer min
        'recherche[prix][max]': parameters['price'][1],  # Loyer max
        'recherche[surface][min]': parameters['surface'][0],  # Surface min
        'recherche[surface][max]': parameters['surface'][1],  # Surface max
        'recherche[nb_pieces][min]': parameters['rooms'][0],  # Pièces min
        'recherche[nb_chambres][min]': parameters['bedrooms'][0],  # Chambres min
        'size': 200,
        'page': 1
    }

    # Insertion des paramètres propres à PAP
    payload.update(parameters['pap'])

    params = urlencode(payload)

    # Ajout des villes
    for city in parameters['cities']:
        params += "&recherche[geo][ids][]=%s" % place_search(city[1])

    request = requests.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header)
    data = request.json()

    for ad in data['_embedded']['annonce']:
        _request = requests.get("https://ws.pap.fr/immobilier/annonces/%s" % ad['id'], headers=header)
        _data = _request.json()

        photos = list()
        if _data.get("nb_photos") > 0:
            for photo in _data["_embedded"]['photo']:
                photos.append(photo['_links']['self']['href'])

        annonce, created = Annonce.create_or_get(
            id='pap-%s' % _data.get('id'),
            site="PAP",
            title="%s %s pièces" % (_data.get("typebien"), _data.get("nb_pieces")),
            description=str(_data.get("texte")),
            telephone=_data.get("telephones")[0].replace('.', '') if len(_data.get("telephones")) > 0 else None,
            created=datetime.fromtimestamp(_data.get("date_classement")),
            price=_data.get('prix'),
            surface=_data.get('surface'),
            rooms=_data.get('nb_pieces'),
            bedrooms=_data.get('nb_chambres_max'),
            city=_data["_embedded"]['place'][0]['title'],
            link=_data["_links"]['desktop']['href'],
            picture=photos
        )

        if created:
            annonce.save()


def place_search(zipcode):
    """Retourne l'identifiant PAP pour un code postal donné"""

    payload = {
        "recherche[cible]": "pap-recherche-ac",
        "recherche[q]": zipcode
    }

    request = requests.get("https://ws.pap.fr/gis/places", params=payload, headers=header)
    return request.json()['_embedded']['place'][0]['id']