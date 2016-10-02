# \#UnToitPourCaramel
_Un programme inspiré par [VikParuchuri/apartment-finder](https://github.com/VikParuchuri/apartment-finder) 
qui récupère les annonces immoblières de SeLoger, Logic-Immo, PAP et Leboncoin pour les aggréger dans un tableau
Trello._

## Pré-requis
* Python 3
* [peewee](http://docs.peewee-orm.com/en/latest/)
* [Requests](https://requests.readthedocs.io/en/master/)

## Le processus d'ingénierie inversée
Puisque les sites exploités ne proposent pas publiquement d'API permettant de récupérer les annonces,
il m'a fallu étudier les requêtes effectuées et les réponses reçues par les applications Android de
ces sites à l'aide de [Packet Capture](https://play.google.com/store/apps/details?id=app.greyshirts.sslcapture).

~~Image de Packet Capture~~

Une fois Packet Capture installé et configuré, il n'y avait plus qu'à lancer les applications et pour chacune
d'entre elle faire une première recherche avec tous les critères possibles afin d'identifier la requête et
les critères ; et une seconde qui retourne au moins deux résultat pour pouvoir étudier l'objet retourné par
l'API.

~~Requête avec tous les paramètres~~

~~Une réponse~~

Avec ces deux informations, on sait donc comment interroger le service avec les critères que l'on souhaite et
quelle réponse il renvoit.

~~Requête d'une annonce~~

La procédure est ensuite répétée pour obtenir le contenu des annonces. Les requêtes et les réponses sont situées
dans le dossier `sample-requests` pour votre analyse (et pour tirer partie des paramètres propres à chaque service).
```
- annonce :
    - rep.xml / rep.json : Corps de la réponse contenant l'annonce
    - req.log : En-têtes de la requête pour obtenir l'annonce
- recherche :
    - rep.xml / rep.json : Corps de la réponse contenant les résultats de la recheche
    - req.full.log : En-têtes de la requête de recherche avec tous les paramètres proposés par l'application
    - req.norm.log : En-têtes de la requête d'une recherche dans un cas d'utilisation normale
    Cas spécifique de Leboncoin : les résultats de recherche sont en plusieurs parties et nécessitent plusieures requêtes
```

## Paramétrer \#UnToitPourCaramel pour ses besoins
Le fichier `main.py` contient un dictionnaire nommé `parameters` qui contient les paramètres communs à chaque service.
```
parameters = {
    # ('Ville', Code postal, Code Insee)
    'cities': [
        ('Nanterre', 92000, 92050),
        ('Chaville', 92370, 92022),
        ('Issy les Moulineaux', 92130, 92040),
        ('Montrouge', 92120, 92049)
    ],
    # (min, max)
    'price': (200, 950),
    'surface': (25, 70),
    'rooms': (2, 5),
    'bedrooms': 1,
}
```
Ces paramètres sont passés aux modules de scrapping situés dans `scrapping_modules` et utilisés dans le dictionnaire
nommé `payload` qui contient les paramètres passés à l'API. Vous pouvez y ajouter les paramètres propres à chaque
service comme tel :
```
payload = {
        'px_loyermin': parameters['price'][0],
        [...]

        # Paramètres "bonus"
        'si-terrasse': 1,

        # Paramètres Se Loger
        'etDtCreationMax': 1
    }
```