from scripts import recipe

def main(url):
    recipe = recipe.fetch_recipe(url)
    result = {}
    result['url'] = url
    result['ingredients'] = []
    for ingr in recipe['ingredients']:
        ingredient = {}
        ingredient['name'] = [ingr['name']]
        ingredient['quantity'] = [ingr['quantity']]
        ingredient['measurement'] = [ingr['measurement']]
        ingredient['descriptor'] = [ingr['descriptor']]
        ingredient['preparation'] = [ingr['preparation']]
        ingredient['prep_descriptor'] = [ingr['prep_descriptor']]
        result['ingredients'].append(ingredient)
    result['primary cooking method'] = recipe['primary_method']
    result['cooking methods'] = recipe['recipe_methods']
    result['cooking tools'] = recipe['recipe_tools']

    return result