import urllib2
import nltk
from nltk import pos_tag
from bs4 import BeautifulSoup

url = 'http://allrecipes.com/Recipe/Chef-Johns-Pasta-Primavera/Detail.aspx?evt19=1&referringHubId=95'

def fetch_recipe(url):
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)

	# get name of recipe
	name = soup.find(id='itemTitle').string
	print 'RECIPE: ' + name

	# get times
	# prep_time = soup.find(id='prepMinsSpan').string
	# cook_time = soup.find(id='cookMinsSpan').string
	# total_time = soup.find(id='totalMinsSpan').string

	# print 'PREP TIME: ' + prep_time
	# print 'COOK TIME: ' + cook_time
	# print 'TOTAL TIME: ' + total_time

	# get ingredients
	ingredients = []
	ingredient_list = soup.find_all(id='liIngredient')
	for ingredient in ingredient_list:
		amount_string = ingredient.find(id='lblIngAmount').string
		name_string = ingredient.find(id='lblIngName').string

		amount_string = amount_string.split()
		if len(amount_string) > 1:
			quantity = amount_string[0]
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
		if len(tagged_name) > 1:
			if tagged_name[0][1] == 'VBD':
				descriptor = ingredient_name[0]
				del ingredient_name[0]
				name_ingr = ' '.join(ingredient_name)
			else:
				name_ingr = ' '.join(ingredient_name)
		else:
			name_ingr = ingredient_name[0]

		preparation = []
		if len(name_string) > 0:
			for phrase in name_string:
				preparation.append(phrase)
		preparation = ''.join(preparation)
			
		ingredient_obj = {}
		ingredient_obj['name'] = name_ingr
		ingredient_obj['descriptor'] = descriptor
		ingredient_obj['quantity'] = quantity
		ingredient_obj['measurement'] = measurement
		ingredient_obj['preparation'] = preparation

		ingredients.append(ingredient_obj)
		# print
		# print 'ingredient: ' + name_ingr
		# print 'descriptor: ' + descriptor
		# print 'quantity: ' + quantity
		# print 'measurement: ' + measurement
		# print 'preparation: ' + preparation
		# print

	# get steps
	instruction_div = soup.find('div', {'class': 'directions'})
	instructions = instruction_div.find_all('li')
	instruction_list = []
	for step in instructions:
		step_obj = {}
		step_obj['text'] = step.span.text

		instruction_list.append(step_obj)
		# print step.span.text
		# print










fetch_recipe(url)   