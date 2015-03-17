import urllib2
import nltk
from nltk import pos_tag
from bs4 import BeautifulSoup

url = 'http://allrecipes.com/Recipe/Chef-Johns-Pasta-Primavera/Detail.aspx?evt19=1&referringHubId=95'
url_2 = 'http://allrecipes.com/Recipe/Pork-Roast-with-Sauerkraut-and-Kielbasa/Detail.aspx?evt19=1&referringHubId=1202'
url_3 = ''

cooking_tools = ['spoon', 'cup', 'bowl', 'cutting board', 'knife', 'peeler', 'colander', 'strainer', 'grater', 'can opener', 'saucepan', 'frying pan', 'pan', 'baking dish', 'blender', 'spatula', 'tongs', 'garlic press', 'ladle', 'ricer', 'pot holder', 'rolling pin', 'scissors', 'whisk', 'skillet', 'wok', 'baking sheet', 'casserole dish', 'pot']
cooking_methods = ['peel', 'grate', 'cut', 'slice', 'sieve', 'knead', 'break', 'boil', 'crack', 'fry', 'scramble', 'stir', 'add', 'bake', 'saute', 'simmer', 'pour', 'chop', 'blend', 'brown', 'carmelise', 'beat', 'dice', 'melt', 'poach', 'toss', 'roast']

def fetch_recipe(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    # get name of recipe
    recipe_name = soup.find(id='itemTitle').string

    recipe_tools = []
    recipe_methods = []

    # get times
    prep_time = soup.find(id='prepMinsSpan').next.string
    cook_time = soup.find(id='cookMinsSpan').next.string
    total_time = soup.find(id='totalMinsSpan').next.string

    # get ingredients
    ingredients = []
    ingredient_list = soup.find_all(id='liIngredient')
    for ingredient in ingredient_list:
        if ingredient.find(id='lblIngAmount'):
            amount_string = ingredient.find(id='lblIngAmount').string
        else:
            amount_string = ''
        if ingredient.find(id='lblIngName'):
            name_string = ingredient.find(id='lblIngName').string
        else:
            name_string = ''

        if amount_string:
            # TODO: sometimes something in parentheses messes this up
            amount_string = amount_string.split()
            if len(amount_string) > 1:
                quantity = amount_string[0]
                if amount_string[1].startswith('('):
                    measurement = ''
                else:
                    measurement = amount_string[1]
            else:
                quantity = amount_string[0]
                measurement = ''

        name_string = name_string.split(',')
        ingredient_name = name_string[0]
        del name_string[0]

        ingredient_name = ''.join(ingredient_name)
        ingredient_name = ingredient_name.split()
        tagged_name = nltk.pos_tag(ingredient_name)

        descriptor = ''
        preparation = ''
        prep_descriptor = ''
        if len(tagged_name) > 1:
            if tagged_name[0][1] == 'VBD' or tagged_name[0][1] == 'JJ':
                descriptor = ingredient_name[0]
                del ingredient_name[0]
                name_ingr = ' '.join(ingredient_name)
            else:
                name_ingr = ' '.join(ingredient_name)
        else:
            name_ingr = ingredient_name[0]

        if descriptor.endswith('ed'):
            preparation = descriptor
            descriptor = ''

        name_string = ''.join(name_string)
        name_string = name_string.split()
        if len(name_string) > 0:
            for phrase in name_string:
                if phrase.endswith('ly'):
                    prep_descriptor = phrase
                if phrase.endswith('ed') and preparation == '':
                    preparation = phrase

            
        ingredient_obj = {}
        ingredient_obj['name'] = name_ingr
        ingredient_obj['descriptor'] = descriptor
        ingredient_obj['quantity'] = quantity
        ingredient_obj['measurement'] = measurement
        ingredient_obj['preparation'] = preparation
        ingredient_obj['prep_descriptor'] = prep_descriptor

        ingredients.append(ingredient_obj)

    # get steps
    instruction_div = soup.find('div', {'class': 'directions'})
    instructions = instruction_div.find_all('li')
    instruction_list = []
    for step in instructions:
        step_obj = {}
        step_obj['text'] = step.span.text

        # get cooking tools
        step_obj['tools'] = []
        for tool in cooking_tools:
            if tool in step_obj['text']:
                step_obj['tools'].append(tool)
                if tool not in recipe_tools:
                    recipe_tools.append(tool)

        # get cooking methods
        step_obj['methods'] = []
        for method in cooking_methods:
            if method in step_obj['text']:
                step_obj['methods']. append(method)
                if method not in recipe_methods:
                    recipe_methods.append(method)

        # get cooking time
        step_obj['time'] = 0
        instruction_tokens = step_obj['text'].split()
        for i in range(0, len(instruction_tokens)):
            if 'minute' in instruction_tokens[i]:
                word = time_phrase(instruction_tokens[i-1])
                if word:
                    step_obj['time'] += word
                elif instruction_tokens[i-1].isnumeric():
                    step_obj['time'] += int(instruction_tokens[i-1])
            if 'hour' in instruction_tokens[i]:
                word = time_phrase(instruction_tokens[i-1])
                if word:
                    step_obj['time'] += word
                elif instruction_tokens[i-1].isnumeric():
                    step_obj['time'] += int(instruction_tokens[i-1])*60


        instruction_list.append(step_obj)

    # print debug
    # print 'RECIPE: ' + recipe_name
    # print
    # print 'PREP TIME: ' + prep_time
    # print 'COOK TIME: ' + cook_time
    # print 'TOTAL TIME: ' + total_time
    # print
    # print 'INGREDIENTS'
    # for ingr in ingredients:
    #     print ingr['name']
    #     print ingr['descriptor']
    #     print ingr['quantity']
    #     print ingr['measurement']
    #     print ingr['preparation']
    #     print ingr['prep_descriptor']
    #     print
    # print 'INSTRUCTIONS'
    # for instruct in instruction_list:
    #     print instruct['text']
    #     print instruct['tools']
    #     print instruct['methods']
    #     print str(instruct['time']) + ' minutes'
    #     print

    # print 'RECIPE TOOLS: '
    # print recipe_tools
    # print 'RECIPE METHODS: '
    # print recipe_methods

    return {
        'recipe_name' : recipe_name,
        'prep_time' : prep_time,
        'cook_time' : cook_time,
        'total_time' : total_time,
        'ingredients' : ingredients,
        'instructions' : instruction_list,
        'recipe_tools' : recipe_tools,
        'receipe_methods' : recipe_methods
    }

def time_phrase(phrase):
    if 'couple' in phrase:
        return 2
    elif 'few' in phrase:
        return 5
    elif 'several' in phrase:
        return 8
    else:
        return False   