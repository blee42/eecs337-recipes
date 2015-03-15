import sys
import string
import bs4
import urllib2

BASE_URL = 'http://www.gourmetsleuth.com/'
# BASE_URL = 'http://www.gourmetsleuth.com/ingredients/'

def get_ingredients():
    ingredients = []

    i = 0
    for letter in string.lowercase:
        letter_soup = get_soup(BASE_URL + 'ingredients/' + letter)
        ingredients += get_ingredients_from_letter(letter_soup)
        print '\rLetters done: ' + i
        sys.stdout.flush()
        i += 1

    return ingredients

def get_ingredients_from_letter(letter_soup):
    all_ingredients = []
    all_ingredients += get_ingredients_from_letter_page(letter_soup)

    pages = letter_soup.find_all(class_='sf_pagerNumeric')[0].find_all('a')
    for i in pages[1:]: # first item is duplicate
        ext = i.attrs['href'][1:] # skip first /
        page_soup = get_soup(BASE_URL + ext)
        all_ingredients += get_ingredients_from_letter_page(page_soup)

    return all_ingredients

def get_ingredients_from_letter_page(letter_soup):
    ingredients = []
    for sec in letter_soup.find_all(class_='portfolio_dscr'):
        ext = sec.a.attrs['href'][1:]
        ingredient_soup = get_soup(BASE_URL + ext)
        ingredients.append(get_ingredient_details(ingredient_soup))

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
        print taxonomy
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

    # do stuff with summary
    return ingredient

def get_soup(url):
    page = urllib2.urlopen(url)
    return bs4.BeautifulSoup(page.read())