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

	# get times
	prep_time = soup.find(id='prepMinsSpan').string
	cook_time = soup.find(id='cookMinsSpan').string
	total_time = soup.find(id='totalMinsSpan').string

	# get ingredients
	ingredient_list = soup.find_all(id='liIngredient')
	for ingredient in ingredient_list:
		amount_string = ingredient.find(id='lblIngAmount').string
		name_string = ingredient.find(id='lblIngName').string

		print name_string
		print amount_string

		amount_string = amount_string.split()
		if len(amount_string) > 1:
			quantity = amount_string[0]
			measurement = amount_string[1]
		else:
			quantity = amount_string[0]

		name_string = name_string.split(',')
		ingredient_name = name_string[0]
		del name_string[0]

		name_string = name_string.split()
		tagged_name = nltk.pos_tag(name_string)

		print
		print tagged_name
		print

		preparation = []
		if len(name_string) > 0:
			for phrase in name_string:
				preparation.append(phrase)
			
		print
		print ingredient_name
		print quantity
		print measurement
		print preparation
		print

fetch_recipe(url)   