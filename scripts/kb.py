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
#assuming diet-descriptor contains non-veg, vegan, vegetarian, Pescatarian
def insert_fixtures():
    if kb.count() == 0:
        examples = [
            {
                'name': 'chicken',
                'type': Type.PROTEIN,
                'composition': Composition.SOLID,
                'diet_descriptor': ['non-veg'],   
                'healthy_descriptor': [''],
                'substitutes': ['wheat gluten' , ''],
                'cuisine': [], # some long list of cuisine types
            },
            {
                'name': 'broccoli',
                'type': Type.VEGETABLE,
                'composition': Composition.SOLID,
                'diet_descriptor': ['vegetarian'],
                'healthy_descriptor': [],
                'substitutes': [],
                'cuisine': []
            }
        ]
        kb.insert_many(examples);


def transform_to_vegan(recipe, ingredient_list):

    for ingredient in ingredient_list:
        total_ingredients = kb.find({'name': ingredient, 'diet_descriptor' : 'vegan'}, { 'name': 1, '_id': 0})
        substitute_list = kb.find({'name': ingredient, 'diet_descriptor' : {'$ne':'vegan'}}, { 'substitutes' : 1, '_id': 0})

        for name in substitute_list:
            change_ingredients= kb.find({'name ' : name,'diet_descriptor' : 'vegan' },  { 'name': 1, '_id': 0})

    total_ingredients.append(change_ingredients)

    
def transform_to_vegetairan(recipe, ingredient_list):

    for ingredient in ingredient_list:
        total_ingredients = kb.find({'name': ingredient, 'diet_descriptor' : 'vegatarian'}, { 'name': 1, '_id': 0})
        substitute_list = kb.find({'name': ingredient, 'diet_descriptor' : {'$ne':'vegetarian'}}, { 'substitutes' : 1, '_id': 0})

        for name in substitute_list:
            change_ingredients = kb.find({'name ' : name,'diet_descriptor' : 'vegetarian' },  { 'name': 1, '_id': 0})

    total_ingredients.append(change_ingredients)




