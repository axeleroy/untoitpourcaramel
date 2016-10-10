# \#UnToitPourCaramel
_Un programme inspiré par [VikParuchuri/apartment-finder](https://github.com/VikParuchuri/apartment-finder) 
qui récupère les annonces immoblières de SeLoger et Leboncoin pour les aggréger dans un tableau Trello._

## Pré-requis
* Python 3
* [peewee](http://docs.peewee-orm.com/en/latest/)
* [Requests](https://requests.readthedocs.io/en/master/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [py-trello](https://pypi.python.org/pypi/py-trello/0.6.1) 
    (et [ses dépendances](https://github.com/sarumont/py-trello/blob/master/requirements.txt))


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

Avec cette méthodologie on peut déterminer comment interroger le service avec les critères que l'on souhaite et
quelles réponses il renvoit.

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
### Authentification Trello
Avant de commencer à utiliser \#UnToitPourCaramel, il vous faut créer le fichier `trello.ini` qui contiendra vos
jetons pour Trello ainsi que le nom de votre tableau et de votre liste :
```
[TRELLO]
ApiKey=your-key
ApiSecret=your-secret
Token=your-oauth-token-key
TokenSecret=your-oauth-token-secret
BoardName=Recherche appartement
ListName=Nouveaux appartements
```
`ApiKey` et `ApiSecret` sont [à obtenir ici](https://trello.com/1/appKey/generate) tandis que `Token`
et `Token Secret` sont à générer avec l'utilitaire `util.py` de `py-trello` :
```
TRELLO_API_KEY=ApiKey TRELLO_API_SECRET=ApiSecret python3 /path/to/py-trello/folder/util.py
```

### Paramètres de recherche
Le fichier `main.py` contient un dictionnaire nommé `parameters` qui contient les paramètres communs à chaque service.
```python
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
```
Ces paramètres sont passés aux modules de scrapping situés dans `scrapping_modules` et utilisés dans le dictionnaire
nommé `payload` qui contient les paramètres passés à l'API. Vous pouvez y ajouter les paramètres propres à chaque
service comme tel (ici `seloger.py`) :
```python
payload = {
    'px_loyermin': parameters['price'][0],
    [...]

    # Paramètres propres à SeLoger
    'idtt': 1,  # 1 : location, 2 : vente
    'idtypebien': '1,2',  # Appartement & Maison / Villa,
    'si_terrasse': 1,

    # Paramètres propres à se loger
    'idtt': 1,  # 1 : location, 2 : vente
    'idtypebien': '1,2',  # Appartement & Maison / Villa,
    'si_terrasse': 1
}
```

## Déploiement sur un Raspberry Pi
_Testé sur un Raspberry Pi sous Raspbian Jessie._

1. Installer `python3-pip` et ``python3-lxml`
    ```
    sudo apt install python3-pip python3-lxml -y
    ```
2. Installer les dépendances
    ```
    sudo pip3 install peewee requests requests_oauthlib py-trello pytz python-dateutil beautifulsoup4
    ```
3. Clonner ce projet
    ```
    git clone https://github.com/axeleroy/untoitpourcaramel.git
    ```
3. Créer une tâche `cron` pour lancer ce script régulièrement (dans mon cas toutes les 2h)
    ```
    crontab -e
    ```
    ```
    * */2 * * * python3 /home/pi/untoitpourcaramel/main.py
    ```
