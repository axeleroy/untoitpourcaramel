# \#UnToitPourCaramel
_Un programme inspiré par [VikParuchuri/apartment-finder](https://github.com/VikParuchuri/apartment-finder) qui récupère les annonces immoblières de SeLoger, PAP et Leboncoin
pour les aggréger dans un tableau Trello._

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