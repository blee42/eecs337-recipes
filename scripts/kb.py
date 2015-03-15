from pymongo import MongoClient
from enum import Enum

db = MongoClient().app
kb = db.kb

class Type(Enum):
    PROTEIN = 0
    VEGETABLE = 1
    FRUIT = 2
    CARB = 3
    DAIRY = 4
    OTHER = 5

class Composition(Enum):
    SOLID = 0
    LIQUID = 1
    POWDER = 2

def insert_fixtures():
    if kb.count() == 0:
        examples = [
            {
                'name': 'chicken',
                'type': Type.PROTEIN,
                'composition': Composition.SOLID,
                'diet_descriptor': ['meat'],
                'healthy_descriptor': [''],
                'substitutes': [],
                'cuisine': [], # some long list of cuisine types
            },
            {
                'name': 'broccoli',
                'type': Type.VEGETABLE,
                'composition': Composition.SOLID,
                'diet_descriptor': [],
                'healthy_descriptor': [],
                'substitutes': [],
                'cuisine': []
            }
        ]
        kb.insert_many(examples);
        kb.find();

