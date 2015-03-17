from pymongo import MongoClient
from threading import Thread
from kb import Type, Composition
from time import sleep

import sys
import string
import bs4
import urllib2
import operator
import re

BASE_URL = u'http://www.gourmetsleuth.com/'
KB_SIZE = 2043

db = MongoClient().app
kb = db.kb

def run_async():
    if kb.count() < 1500:
        thread = Thread(target=run, args={})
        thread.daemon = True
        thread.start()
    else:
        refine_kb_entries()
    return

def run():
    kb.remove({})
    print 'Initializing knowledge base...please wait.'
    print ''
    threads = get_ingredients()

    if __name__ == '__main__':
        counter_thread = Thread(target=async_count_print)
        counter_thread.start()

    for thread in threads:
        thread.join()

    refine_kb_entries()

    print '\r{0} of {0} knowledge base entries loaded.'.format(KB_SIZE)
    print 'Knowledge base fully initialized.'
    return

def async_count_print():
    while (kb.count() < KB_SIZE):
        print '\r{0} of {1} knowledge base entries loaded.'.format(kb.count(), KB_SIZE),
        sys.stdout.flush()
        sleep(1)
    return

def get_ingredients():
    ingredients = []
    threads = []

    i = 0
    for letter in string.lowercase:
        letter_soup = get_soup(BASE_URL + 'ingredients/' + letter)
        thread = Thread(target=get_ingredients_from_letter, args=(letter_soup, letter))
        thread.daemon = True
        thread.start()
        # print 'Thread {0} started.'.format(letter)
        threads.append(thread)
        # ingredients += get_ingredients_from_letter(letter_soup)

    return threads

def get_ingredients_from_letter(letter_soup, letter):
    all_ingredients = []
    all_ingredients += get_ingredients_from_letter_page(letter_soup)

    pages = letter_soup.find_all(class_='sf_pagerNumeric')[0].find_all('a')
    # print 'Page 1 from Thread {0} completed.'.format(letter)
    # sys.stdout.flush()
    # count = 1
    for i in pages[1:]: # first item is duplicate
        ext = i.attrs['href'][1:] # skip first /
        page_soup = get_soup(BASE_URL + ext)
        all_ingredients += get_ingredients_from_letter_page(page_soup)

        # count += 1
        # print 'Page {0} from Thread {1} completed.'.format(count, letter)
        sys.stdout.flush()

    # print 'Thread {0} finished.'.format(letter)
    return all_ingredients

def get_ingredients_from_letter_page(letter_soup):
    ingredients = []
    for sec in letter_soup.find_all(class_='portfolio_dscr'):
        try:
            ext = sec.a.attrs['href'][1:]
            ingredient_soup = get_soup(BASE_URL + ext)
            ingredients.append(get_ingredient_details(ingredient_soup))
        except:
            pass
            # print 'Problem!'
            # print ext

    return ingredients

def get_ingredient_details(ingredient_soup):
    ingredient = {}
    ingredient['name'] = ingredient_soup.find('h1').contents[0].contents[0].lower()
    # name = ingredient_soup.find('h1').contents[0].contents[0]

    try:
        taxonomy = ingredient_soup.find(class_='taxa').contents[0].strip('\r\n ').lower()
        ingredient['web_taxonomy'] = taxonomy
    except:
        # print ingredient
        pass

    details = ingredient_soup.find_all(class_='ingredient-summary')
    substitutes = ''
    summary = ''
    for i in details:
        try:
            if 'Substitute' in i.contents[0].contents[0]:
                substitutes = i.contents[1].contents[0].lower()

            elif 'About' in i.contents[0].contents[0]:
                summary = i.contents[1].contents[0]
                while True:
                    try:
                        summary = summary.contents[0]
                    except:
                        break
        except:
            pass
    ingredient['substring'] = substitutes
    ingredient['summary'] = summary.lower()

    # do stuff with summary

    nutrients = {}
    macros = ingredient_soup.find_all(class_='left_strong_label')
    for macro in macros:
        nutrient = macro.contents[0].strip()
        amount = [macro.contents[1].contents[0].strip()]
        if macro != macros[0]:
            amount.append(macro.find_next(class_='right_light_label').contents[1].contents[0].strip())
        nutrients[nutrient.lower()] = amount

    others = ingredient_soup.find_all(class_='left_light_label')
    for other in others:
        if other != others[0]:
            nutrient = other.contents[0].strip()
            amount = [other.contents[1].contents[0].strip()]
            amount.append(other.find_next(class_='right_light_label').contents[1].contents[0].strip())
        nutrients[nutrient.lower()] = amount

    minerals = ingredient_soup.find_all(class_='left_col') + ingredient_soup.find_all(class_='right_col')
    for mineral in minerals:
        data = mineral.contents[0].strip().split(u'\xa0')
        nutrients[data[0].lower()] = data[1]

    if nutrients:
        ingredient['nutrients'] = nutrients

    # print ingredient

    kb.insert(ingredient) # good spot?
    return ingredient

def get_soup(url):
    page = urllib2.urlopen(url)
    return bs4.BeautifulSoup(page.read())

#### KB REFINEMENT ####

def refine_kb_entries():
    for ingredient in kb.find():
        ingredient['type'] = get_type(ingredient)
        ingredient['composition'] = get_composition(ingredient)
        ingredient['diet_descriptor'] = get_diet_descriptors(ingredient)
        ingredient['healthy_descriptor'] = get_healthy_descriptors(ingredient)

        ingredient['substitutes'] = fix_substitutes(ingredient['substring'])
        kb.save(ingredient)

def get_type(ingredient):
    potential_groups = []
    if 'web_taxonomy' in ingredient:
        for group, examples in type_converters.iteritems():
            for example in examples:
                if example in ingredient['web_taxonomy']:
                    potential_groups.append(group)
                    break
    if len(potential_groups) > 0:
        return potential_groups[0]
    else:
        tally = {}
        for group, examples in type_converters.iteritems():
            tally[group] = 0
            for example in examples:
                if example in ingredient['summary'] or ingredient['name']:
                    tally[group] += 1
        best = max(tally.iteritems(), key=operator.itemgetter(1))
        if best[1] != 0:
            return best[0]
        else:
            print best
            return 'uncertain'

def get_composition(ingredient):
    if 'web_taxonomy' in ingredient:
        for group, examples in composition_converters.iteritems():
            for example in examples:
                if example in ingredient['web_taxonomy'] or example in ingredient['name']:
                    return group
    return 'solid'

def get_diet_descriptors(ingredient):
    descriptors = []
    if ingredient['type'] in ['fruit', 'vegetable', 'carb']:
        return ['vegan', 'vegetarian', 'pescatarian', 'lactose-free']
    elif ingredient['type'] == 'dairy':
        if 'non-dairy' in ingredient['web_taxonomy']:
            return ['vegan', 'vegetarian', 'pescatarian', 'lactose-free']
        else:
            return ['vegetarian', 'pescatarian']
    elif ingredient['type'] in ['protein', 'other']:
        diets = []
        if 'meat substitute' in ingredient['summary']:
            return ['vegan', 'vegetarian', 'pescatarian', 'lactose-free']
        for diet, examples in diet_converter.iteritems():
            append = True
            for example in examples:
                if 'web_taxonomy' in ingredient and example in ingredient['web_taxonomy'] \
                or example in ingredient['name'] or example in ingredient['summary']:
                    append = False
                    break
                elif example in ingredient['name'] or example in ingredient['summary']:
                    append = False
                    break
            if append:
                diets.append(diet)
        return diets
    return

def get_healthy_descriptors(ingredient):
    if 'nutrients' in ingredient:
        descriptors = []
        for descriptor, check in healthy_converter.iteritems():
            if check(ingredient['nutrients']):
                descriptors.append(descriptor)
        return descriptors
    else:
        return ['low-sodium', 'low-fat', 'low-calorie']

def fix_substitutes(sub_string):
    new_string = re.sub('\(.*\)', '', sub_string)
    sub_array = re.split(',| or | and ', new_string)

    ret_res = []
    for i in sub_array:
        if i.strip() != '' and \
        'cooking' not in i:
            ret_res.append(i)

    return ret_res

#### Converters ####

type_converters = {
    'carb': [
        'pasta',
        'bread',
        'flour',
        'cereal',
        'wheat',
        'oat',
        'rice',
        'grain',
        'potato',
        'dough',
        'tuber',
        'starch',
        'cracker',
        'toast',
        'corn'
    ],
    'protein': [
        'protein',
        'fish',
        'chicken',
        'soy',
        'nut',
        'bean',
        'pork',
        'beef',
        'ham',
        'egg',
        'legume',
        'steak',
        'meat',
        'poultry',
        'tofu',
        'sausage'
    ],
    'dairy': [
        'dairy',
        'milk',
        'cheese',
        'cream',
        'yogurt',
    ],
    'other': [
        'chocolate',
        'liquer',
        'liqueur',
        'liquor',
        'wine',
        'alcohol',
        'beer',
        'condiment',
        'spice',
        'herb',
        'seed',
        'salt',
        'additive',
        'oil',
        'garlic',
        'powder',
        'cookie',
        'sugar',
        'candy',
        'vinegar',
        'yeast',
        'cooking fat',
        'crumb',
        'water',
        'brandy',
        'sweetener',
        'coffee',
    ],
    'fruit': [
        'fruit',
        'berry',
        'berries',
        'avocado',
        'apple',
        'orange',
        'peach',
        'pear',
        'cherry',
        'kiwi',
        'grape',
        'melon',
        'honeydew',
    ],
    'vegetable': [
        'vegetable',
        'veggie',
        'root',
        'leaf',
        'eggplant',
        'sprout',
        'greens',
        'broccoli',
        'kale',
        'bok choy',
        'squash',
        'carrot',
        'onion',
        'mushroom',
        'pepper',
        'flower',
        'chile',
        'olive',
        'pea',
        'leave',
        'bamboo',
        'cabbage',
        'tomato',
        'lentil',
        'pickle'
    ],
    'ignore': [
        'recipe terms',
        'miscellaneous',
        'technique',
        'equipment',
        'cooking terms',
        'glossary',
        'serving tool',
        'reference',

    ]
}

composition_converters = {
    'liquid': [
        'oil',
        'liquid',
        'juice',
        'nectar',
        'soup',
        'drink',
        'sauce',
        'broth',
        'wine',
        'beer',
        'liquer',
        'liquor',
        'coffee',
        'liquid'
    ],
    'powder': [
        'sugar',
        'spice',
        'salt', 
    ]
}

# eliminate if these are here
diet_converter = {
    'pescatarian': [
        'chicken',
        'poultry',
        'red meat'
        'pork',
        'beef',
        'ham',
        'steak'
    ],
    'vegetarian': [
        'fish',
        'chicken',
        'pork',
        'beef',
        'ham',
        'steak',
        'meat',
        'poultry',
        'animal fat',
    ],
    'vegan': [
        'fish',
        'chicken',
        'pork',
        'beef',
        'ham',
        'egg',
        'steak',
        'meat',
        'poultry',
        'animal fat',
        'butter',
    ],
    'lactose-free': [
        'generic-place-holder-here'
    ]
}

healthy_converter = {
    'low-sodium': lambda x: (float(x['sodium'][1].strip('%')) < 10),
    'low-fat': lambda x: (float(x['saturated fat'][1].strip('%')) < 5 and \
        float(x['total fat'][1].strip('%')) < 10),
    'low-calorie': lambda x:(float(x['calories'][0]) < 400)
}