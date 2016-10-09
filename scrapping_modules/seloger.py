import requests
import xml.etree.ElementTree as ET
from models import Annonce
from datetime import datetime
'''Module qui récupère les annonces de SeLoger.com'''


def search(parameters):
    # Préparation des paramètres de la requête
    payload = {
        'px_loyermin': parameters['price'][0],
        'px_loyermax': parameters['price'][1],
        'surfacemin': parameters['surface'][0],
        'surfacemax': parameters['surface'][1],
        # Si parameters['rooms'] = (2, 4) => "2,3,4"
        'nbpieces': list(range(parameters['rooms'][0], parameters['rooms'][1] + 1)),
        # Si parameters['bedrooms'] = 2 => "1,2"
        'nb_chambres': list(range(1, parameters['bedrooms'] + 1)),
        'ci': [int(cp[2]) for cp in parameters['cities']],

        # Paramètres propres à se loger
        'idtt': 1,  # 1 : location, 2 : vente
        'idtypebien': '1,2',  # Appartement & Maison / Villa,
        'si_terrasse': 1,
        'getDtCreationMax': 1  # ¯\_(ツ)_/¯
    }

    headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)'}

    request = requests.get("http://ws.seloger.com/search_4.0.xml", params=payload, headers=headers)

    xmlRoot = ET.fromstring(request.text)

    for annonceNode in xmlRoot.findall('annonces/annonce'):
        photos = list()
        for photo in annonceNode.find("photos"):
            photos.append(photo.find("stdUrl").text)

        annonce, created = Annonce.create_or_get(
            id='seloger-' + annonceNode.find('idAnnonce').text,
            site='seloger',
            # SeLoger peut ne pas fournir de titre pour une annonce T_T
            title="Appartement " + annonceNode.find('nbPiece').text + " pièces" if annonceNode.find('titre').text is None else annonceNode.find('titre').text,
            created=datetime.strptime(annonceNode.find('dtCreation').text, '%Y-%m-%dT%H:%M:%S'),
            price=annonceNode.find('prix').text,
            charges=annonceNode.find('charges').text,
            surface=annonceNode.find('surface').text,
            rooms=annonceNode.find('nbPiece').text,
            bedrooms=annonceNode.find('nbChambre').text,
            city=annonceNode.find('ville').text,
            link=annonceNode.find('permaLien').text,
            picture=photos
        )

        if created:
            annonce.save()
