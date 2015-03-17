from pymongo import MongoClient
from enum import Enum

import re

db = MongoClient().app
kb = db.kb

def insert_fixtures():
    if kb.count() == 0:
        examples = [
            {
                'name': 'chicken',
                'type': 'protein',
                'composition': 'solid',
                'diet_descriptor': ['non-veg'],   
                'healthy_descriptor': [''],
                'substitutes': ['wheat gluten' , ''],
                'cuisine': [], # some long list of cuisine types
            },
            {
                'name': 'broccoli',
                'type': 'vegetable',
                'composition': 'solid',
                'diet_descriptor': ['vegetarian'],
                'healthy_descriptor': [],
                'substitutes': [],
                'cuisine': []
            }
        ]
        kb.insert_many(examples);

example_recipe = {
    'ingredients': [
        'chicken',
        'butter',
        'flour',
        'white sugar',
        'baking powder',
        'salt',
        'egg'
    ]
}

def fuzzy_search_for_ingredient(name):
    attempt = kb.find_one({'name': name})
    if attempt:
        return attempt
    
    # measurement filter?
    # attempts = kb.find({'name': {'$regex': r'\b' + name + r'\b'}})
    attempt = kb.find_one({'name': {'$regex': r'\b' + name + r'\b'}})
    if attempt:
        return attempt

    words = name.strip('.,()').split(' ')
    for word in reversed(words): #if any predecessors, usually adjectives
        attempt = kb.find_one({'name': {'$regex': r'\b' + word + r'\b'}})
        if attempt:
            return attempt

    return

def transform_to_diet(recipe, diet):
    replacement_ingredients = []
    for ingredient in recipe['ingredients']:
        kb_ingredient = fuzzy_search_for_ingredient(ingredient)
        if kb_ingredient:
            if diet in kb_ingredient['diet_descriptor']:
                replacement_ingredients.append(kb_ingredient['name'])
            else:
                print 'Replacing ' + ingredient + ': '
                print 'Details: '
                print kb_ingredient
                print
                added = False
                for substitute in kb_ingredient['substitutes']:
                    sub_item = fuzzy_search_for_ingredient(substitute)
                    if sub_item and diet in sub_item['diet_descriptor']:
                        print 'Found substitute: '
                        print substitute
                        print sub_item
                        print
                        replacement_ingredients.append(sub_item['name'])
                        added = True
                        break

                if not added:
                    print 'Could not find substitute.'
                    rand_ingredient = find_best_diet_replacement(kb_ingredient, diet)
                    replacement_ingredients.append(rand_ingredient['name'])
                    print rand_ingredient
                    added = True
        else:
            replacement_ingredients.append(ingredient)

    return replacement_ingredients

def find_best_diet_replacement(kb_ingredient, diet):
    # options = kb.find({'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})
    # for i in options:
    return kb.find_one({'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})

## IN PROGRESS
# direction: up, down
# NUTRIENT = ''
# def transform_healthiness(recipe, nutrient, direction):
#     global NUTRIENT
#     NUTRIENT = nutrient
#     replacement_ingredients = []

#     if direction == 'up':
#         direct = True
#     elif direction == 'down':
#         direct = False
#     else
#         return

#     for ingredient in recipe['ingredients']:
#         kb_ingredient = fuzzy_search_for_ingredient(ingredient)

#         if kb_ingredient:
#             substitutes = [fuzzy_search_for_ingredient[sub] for sub in kb_ingredient['substitutes']]
#             if substitutes:
#                 substitutes.sort(key=nutrient_key, reverse=direct)
#                 if substitutes[0]['nutrients'][nutrient][0] != -1:
#                     replacement_ingredients.a



#             if diet in kb_ingredient['diet_descriptor']:
#                 replacement_ingredients.append(kb_ingredient['name'])
#             else:
#                 print 'Replacing ' + ingredient + ': '
#                 print 'Details: '
#                 print kb_ingredient
#                 print
#                 added = False
#                 for substitute in kb_ingredient['substitutes']:
#                     sub_item = fuzzy_search_for_ingredient(substitute)
#                     if sub_item and diet in sub_item['diet_descriptor']:
#                         print 'Found substitute: '
#                         print substitute
#                         print sub_item
#                         print
#                         replacement_ingredients.append(sub_item['name'])
#                         added = True
#                         break

#                 if not added:
#                     print 'Could not find substitute.'
#                     rand_ingredient = find_best_rand_replacement(kb_ingredient, diet)
#                     replacement_ingredients.append(rand_ingredient['name'])
#                     print rand_ingredient
#                     added = True
#         else:
#             replacement_ingredients.append(ingredient)

#     return replacement_ingredients

# def nutrient_key(ingredient):
#     if ingredient['nutrients']:
#         return ingredient['nutrients'][NUTRIENT][0]
#     else:
#         return -1

## DISCARDING?

# not sure what this does?
# def transform_to_vegan(recipe, ingredient_list):

#     for ingredient in ingredient_list:
#         total_ingredients = kb.find({'name': ingredient, 'diet_descriptor' : 'vegan'}, { 'name': 1, '_id': 0})
#         substitute_list = kb.find({'name': ingredient, 'diet_descriptor' : {'$ne':'vegan'}}, { 'substitutes' : 1, '_id': 0})

#         for name in substitute_list:
#             change_ingredients = kb.find({'name ' : name,'diet_descriptor' : 'vegan' },  { 'name': 1, '_id': 0})

#     total_ingredients.append(change_ingredients)

    
# def transform_to_vegetarian(recipe, ingredient_list):

#     for ingredient in ingredient_list:
#         total_ingredients = kb.find({'name': ingredient, 'diet_descriptor' : 'vegatarian'}, { 'name': 1, '_id': 0})
#         substitute_list = kb.find({'name': ingredient, 'diet_descriptor' : {'$ne':'vegetarian'}}, { 'substitutes' : 1, '_id': 0})

#         for name in substitute_list:
#             change_ingredients = kb.find({'name ' : name,'diet_descriptor' : 'vegetarian' },  { 'name': 1, '_id': 0})

#     total_ingredients.append(change_ingredients)




