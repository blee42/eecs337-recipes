from pymongo import MongoClient
from threading import Thread

import sys
import string
import bs4
import urllib2

BASE_URL = 'http://www.gourmetsleuth.com/'

db = MongoClient().app
kb = db.kb

def get_ingredients():
    ingredients = []
    threads = []

    i = 0
    for letter in string.lowercase:
        letter_soup = get_soup(BASE_URL + 'ingredients/' + letter)
        thread = Thread(target=get_ingredients_from_letter, args=(letter_soup, letter))
        thread.daemon = True
        thread.start()
        print 'Thread {0} started.'.format(letter)
        threads.append(thread)
        # ingredients += get_ingredients_from_letter(letter_soup)

    for thread in threads:
        thread.join()

    return ingredients

def get_ingredients_from_letter(letter_soup, letter):
    all_ingredients = []
    all_ingredients += get_ingredients_from_letter_page(letter_soup)

    pages = letter_soup.find_all(class_='sf_pagerNumeric')[0].find_all('a')
    print 'Page 1 from Thread {0} completed.'.format(letter)
    sys.stdout.flush()
    count = 1
    for i in pages[1:]: # first item is duplicate
        ext = i.attrs['href'][1:] # skip first /
        page_soup = get_soup(BASE_URL + ext)
        all_ingredients += get_ingredients_from_letter_page(page_soup)

        count += 1
        print 'Page {0} from Thread {1} completed.'.format(count, letter)
        sys.stdout.flush()

    return all_ingredients

def get_ingredients_from_letter_page(letter_soup):
    ingredients = []
    for sec in letter_soup.find_all(class_='portfolio_dscr'):
        ext = sec.a.attrs['href'][1:]
        ingredient_soup = get_soup(BASE_URL + ext)
        ingredients.append(get_ingredient_details(ingredient_soup))

    kb.insert_many(ingredients) # good spot?

    return ingredients


converters = {
    'carbs': [
        'pasta',
        'bread',
        'flour',
        'cereal',
        'wheat',
        'oats',
        'rice'
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
        'ham'
    ],
    'dairy': [
        'dairy',
        'milk',
        'cheese',
        'cream',
    ],
    'other': [
        'liquer',
        'liquor',
        'alcohol',
        'beer',
        'condiment',
        'spice',
        'herb',
        'seed',
        'salt',
        'additive',
        'oil',
    ],
    'fruit': [
        'fruit',
        'berry',
        'berries',
        'avocado',

    ],
    'vegetable': [
        'vegetable',
        'root',
        'leaf',
        'eggplant',
        'sprout',
        'greens'

    ],
    'ignore': [
        'recipe terms',
        'miscellaneous',
        'technique',
    ]
}


def get_ingredient_details():
    ingredient = {}
    ingredient_soup=get_soup('http://www.gourmetsleuth.com/' + ext)
    ingredient['name'] = ingredient_soup.find('h1').contents[0].contents[0]
    try:
        taxonomy = ingredient_soup.find(class_='taxa').contents[0].strip('\r\n ').lower()
        ingredient['web_taxonomy'] = taxonomy
    except:
        # print ingredient
        pass

    details = ingredient_soup.find_all(class_='ingredient-summary')
    substitutes = []
    summary = ''
    for i in details:
        try:
            if 'Substitute' in i.contents[0].contents[0]:
                subs = i.contents[1].contents[0].lower()
                if (',' in subs) and (' or' in subs):
                    subs.strip(',')
                    subs = subs.split(' or')
                elif (',') in subs:
                    subs = subs.split(',')
                elif ' or' in subs:
                    subs = subs.split(' or')
                else:
                    subs = [subs]

                for j in subs:
                    substitutes.append(j.strip())

            elif 'About' in i.contents[0].contents[0]:
                summary = i.contents[1].contents[0]
        except:
            pass
    ingredient['substitutes'] = substitutes
    ingredient['summary'] = summary

    # do stuff with summary

    nutrients = {}
    macros = ingredient_soup.find_all(class_='left_strong_label')
    for macro in macros:
        nutrient = macro.contents[0].strip()
        amount = [macro.contents[1].contents[0].strip()]
        if macro != macros[0]:
            amount.append(macro.find_next(class_='right_light_label').contents[1].contents[0].strip())
        nutrients[nutrient] = amount

    others = ingredient_soup.find_all(class_='left_light_label')
    for other in others:
        if other != others[0]:
            nutrient = other.contents[0].strip()
            amount = [other.contents[1].contents[0].strip()]
            amount.append(other.find_next(class_='right_light_label').contents[1].contents[0].strip())
        nutrients[nutrient] = amount

    minerals = ingredient_soup.find_all(class_='left_col') + ingredient_soup.find_all(class_='right_col')
    for mineral in minerals:
        data = mineral.contents[0].strip().split(u'\xa0')
        nutrients[data[0]] = data[1]

    if nutrients:
        ingredient['nutrients'] = nutrients



    return ingredient

def get_soup(url):
    page = urllib2.urlopen(url)
    return bs4.BeautifulSoup(page.read())