from pymongo import MongoClient

import re

db = MongoClient().app
kb = db.kb

### EXAMPLES ###
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
        'olive oil',
        'white sugar',
        'baking powder',
        'salt',
        'egg'
    ]
}


### ACTUAL ###
def fuzzy_search_for_ingredient(name):
    attempt = kb.find_one({'name': name})
    if attempt:
        return attempt

    attempt = kb.find_one({'name': name[:len(name)-1]}) # if plural in name
    if attempt:
        return attempt

    attempt = kb.find_one({'name': name + 's'}) # if plural in kb
    if attempt:
        return attempt

    attempt = kb.find_one({'name': {'$regex': r'\b' + name + '(s,|,).*'}})
    if attempt:
        return attempt
    
    # measurement filter?
    # attempts = kb.find({'name': {'$regex': r'\b' + name + r'\b'}})
    attempt = kb.find_one({'name': {'$regex': r'\b' + name + r'(s\b|\b)'}})
    if attempt:
        return attempt

    words = name.strip('.,()').split(' ')
    for word in reversed(words): #if any predecessors, usually adjectives
        attempt = kb.find_one({'name': word})
        if attempt:
            return attempt
        attempt = kb.find_one({'name': {'$regex': r'\b' + word + r'\b'}})
        if attempt:
            return attempt

    return

def transform_to_diet(recipe, diet):
    replacement_ingredients = []
    for ingredient in recipe['ingredients']:
        # print ingredient['name']
        kb_ingredient = fuzzy_search_for_ingredient(ingredient['name'].lower())
        # print kb_ingredient
        if kb_ingredient and not kb_ingredient['diet_descriptor'] is None:
            if diet in kb_ingredient['diet_descriptor']:
                # replacement_ingredients.append(kb_ingredient['name'])
                replacement_ingredients.append(ingredient['name'])
            else:
                # print 'Replacing ' + ingredient['name'] + ': '
                # print 'Details: '
                # print kb_ingredient
                # print
                added = False
                for substitute in kb_ingredient['substitutes']:
                    sub_item = fuzzy_search_for_ingredient(substitute)
                    if sub_item and diet in sub_item['diet_descriptor']:
                        # print 'Found substitute: '
                        # print substitute
                        # print sub_item
                        # print
                        replacement_ingredients.append(sub_item['name'])
                        added = True
                        break

                if not added:
                    # print 'Could not find substitute.'
                    rand_ingredient = find_best_diet_replacement(kb_ingredient, diet, replacement_ingredients)
                    replacement_ingredients.append(rand_ingredient['name'])
                    # print rand_ingredient
                    # print
                    added = True
        else:
            replacement_ingredients.append(ingredient['name'])

    return replacement_ingredients

def find_best_diet_replacement(kb_ingredient, diet, replacement_ingredients):
    # options = kb.find({'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})
    # for i in options:
    return kb.find_one({'name': {'$nin': replacement_ingredients}, \
        'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})

# pretty similar to above
def transform_healthiness(recipe, healthy):
    replacement_ingredients = []
    for ingredient in recipe['ingredients']:
        kb_ingredient = fuzzy_search_for_ingredient(ingredient['name'].lower())
        if kb_ingredient and not kb_ingredient['healthy_descriptor'] is None:
            if healthy in kb_ingredient['healthy_descriptor']:
                replacement_ingredients.append(ingredient['name'])
            else:
                added = False
                for substitute in kb_ingredient['substitutes']:
                    sub_item = fuzzy_search_for_ingredient(substitute)
                    if sub_item and healthy in sub_item['healthy_descriptor']:
                        replacement_ingredients.append(sub_item['name'])
                        added = True
                        break

                if not added:
                    rand_ingredient = find_best_healthy_replacement(kb_ingredient, healthy, replacement_ingredients)
                    if rand_ingredient:
                        replacement_ingredients.append(rand_ingredient['name'])
                        added = True
        else:
            replacement_ingredients.append(ingredient['name'])

    return replacement_ingredients

def find_best_healthy_replacement(kb_ingredient, healthy, replacement_ingredients):
    # options = kb.find({'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})
    # for i in options:
    return kb.find_one({'name': {'$nin': replacement_ingredients}, \
        'type': kb_ingredient['type'], 'healthy_descriptor': healthy, 'composition': kb_ingredient['composition']})

def transform_cuisine(recipe, cuisine):
    replacement_ingredients = []
    for ingredient in recipe['ingredients']:
        kb_ingredient = fuzzy_search_for_ingredient(ingredient['name'].lower())
        if kb_ingredient and not kb_ingredient['cuisine_descriptor'] is None:
            if cuisine in kb_ingredient['cuisine_descriptor']:
                replacement_ingredients.append(ingredient['name'])
            else:
                added = False
                for substitute in kb_ingredient['substitutes']:
                    sub_item = fuzzy_search_for_ingredient(substitute)
                    if sub_item and cuisine in sub_item['cuisine_descriptor']:
                        replacement_ingredients.append(sub_item['name'])
                        added = True
                        break

                if not added:
                    rand_ingredient = find_best_cuisine_replacement(kb_ingredient, cuisine, replacement_ingredients)
                    if rand_ingredient:
                        replacement_ingredients.append(rand_ingredient['name'])
                        added = True
        else:
            replacement_ingredients.append(ingredient['name'])

    return replacement_ingredients

def find_best_cuisine_replacement(kb_ingredient, cuisine, replacement_ingredients):
    # options = kb.find({'type': kb_ingredient['type'], 'diet_descriptor': diet, 'composition': kb_ingredient['composition']})
    # for i in options:
    return kb.find_one({'name': {'$nin': replacement_ingredients}, \
        'type': kb_ingredient['type'], 'cuisine_descriptor': cuisine, 'composition': kb_ingredient['composition']})

### DISCARDING ###

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




