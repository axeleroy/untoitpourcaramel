from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteDatabase('annonces.db')

class BaseModel(Model):
    class Meta:
        database = db

class Annonce(BaseModel):
