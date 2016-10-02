import annonce
from scrapping_modules import seloger

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

annonce.create_tables()

seloger.search(parameters)

for ann in annonce.Annonce.select():
    print(ann.id, ann.title)