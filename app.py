#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo
from logging import Formatter, FileHandler
from forms import *
from scripts import transforms, populate_kb, recipe

import logging
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
mongo = PyMongo(app)

def kb_ready():
    if mongo.db.kb.count() >= 2043:
        return True
    else:
        return False

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    if kb_ready():
        return render_template('pages/placeholder.home.html')
    else:
        context = {}
        context['loaded'] = mongo.db.kb.count()
        return render_template('pages/loading.html', context=context)

@app.route('/', methods=['POST'])
def home_post():
    recipe_url = request.form['recipe_url']
    transforms = request.form['transform']
    # health_transform = request.form['health_transform']
    # cuisine_transform = request.form['cuisine_transform']
    if transforms == '0':
        # pescatarian
        return recipe_submitted(recipe_url, 'pescatarian', '', '')
    elif transforms == '1':
        # vegetarian
        return recipe_submitted(recipe_url, 'vegetarian', '', '')
    elif transforms == '2':
        # vegan
        return recipe_submitted(recipe_url, 'vegan', '', '')
    elif transforms == '3':
        # lactose-free
        return recipe_submitted(recipe_url, 'lactose-free', '', '')
    elif transforms == '4':
        # low calorie
        return recipe_submitted(recipe_url, '', 'low-calorie', '')
    elif transforms == '5':
        # low fat
        return recipe_submitted(recipe_url, '', 'low-fat', '')
    elif transforms == '6':
        # low sodium
        return recipe_submitted(recipe_url, '', 'low-sodium', '')
    elif transforms == '7':
        # low carb
        return recipe_submitted(recipe_url, '', 'low-carb', '')
    elif transforms == '8':
        # asian
        return recipe_submitted(recipe_url, '', '', 'asian')
    elif transforms == '9':
        # western
        return recipe_submitted(recipe_url, '', '', 'western')
    elif transforms == '10':
        return recipe_submitted(recipe_url, '', '', 'italian')
    elif transforms == '11':
        return recipe_submitted(recipe_url, '', '', 'latin')
    elif transforms == '12':
        return recipe_submitted(recipe_url, '', '', 'indian')

@app.route('/recipe_submitted', methods=['POST'])
def recipe_submitted(url, diet, health, cuisine):
    context = {}
    parsed_recipe = recipe.fetch_recipe(url)
    context['recipe_name'] = parsed_recipe['recipe_name']
    context['recipe_url'] = url
    context['prep_time'] = parsed_recipe['prep_time']
    context['cook_time'] = parsed_recipe['cook_time']
    context['total_time'] = parsed_recipe['total_time']
    context['ingredients'] = parsed_recipe['ingredients']
    context['instructions'] = parsed_recipe['instructions']
    context['tools'] = parsed_recipe['recipe_tools']
    context['methods'] = parsed_recipe['recipe_methods']
    context['primary_method'] = parsed_recipe['primary_method']

    if diet != '':
        transformed_recipe = transforms.transform_to_diet(parsed_recipe, diet)
        context['transformed_recipe'] = transformed_recipe
        context['transformation'] = diet
    if health != '':
        context['transformed_recipe'] = transforms.transform_healthiness(parsed_recipe, diet)
        context['transformation'] = health
    if cuisine != '':
        context['transformed_recipe'] = transforms.transform_cuisine(parsed_recipe, cuisine)
        context['transformation'] = cuisine
    # else:
    #     context['transformed_recipe'] = 'Not available'
    #     context['transformation'] = ''
    return render_template('pages/recipe_submitted.html', context=context)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.before_first_request
def before_first_request():
    populate_kb.run_async()

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
