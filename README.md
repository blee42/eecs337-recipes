# Recipe Transformer

Project by Kevin Chen, Brittany Lee, Kevin Broh-Kahn, and Bhavita Jaiswal!

This project is built off of a Flask boilerplate - [https://github.com/mjhea0/flask-boilerplate/](https://github.com/mjhea0/flask-boilerplate)

## Quick Start
1. Clone the repo
  ```shell
  $ git clone git@github.com:blee42/eecs337.git
  $ cd flask-boilerplate
  ```

2. Make a virtual environment.  We are using the virtualenvwrapper; if you have not used it before the installation docs can be seen [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](here).
  ```shell
  $ mkvirtualenv env
  $ workon env
  ```

3. Install the dependencies:
  ```shell
  $ pip install -r requirements.txt
  ```

4. Install MongoDB

4. Run the development server:
  ```shell
  $ python app.py
  ```

5. Navigate to [http://localhost:5000](http://localhost:5000)

## Starting MongoDB
1. Have MongoDB installed and Flask PyMongo installed via PIP (TODO: add to README).
2. Make the `data/db` folder.
  ```shell
  $ mkdir data/db
  ```

3. Start MongoDB in a separate shell window.
  ```shell
  $ mongo --dbpath data/db/
  ```

4. Do whatever else you want to.

## Populating the DB initially

`populate_kb.py` contains code for generating our knowledge base by populating the database with some 2043 entries.
Just run `run()` and it should do the right thing. This will take ~10 mins. Running the Flask server itself will have a similar effect, in addition to checks that rerun specific bits as necessary.

example data:
```JSON
{
  "_id" : ObjectId("5507cca29547e66a6a1bb445"),
  "name" : "abiu",
  "substitutes" : [
    "cherimoya",
    "any fresh tropical fruit"
  ],
  "diet_descriptor" : [
    "vegan",
    "vegetarian",
    "pescatarian",
    "lactose-free"
  ],
  "healthy_descriptor" : null,
  "summary" : "(pouteria caimito) a tropical fruit with caramel flavored flesh. the fruit is typically eaten fresh and slightly chilled. eat only the soft \"jelly like\" fruit and don't scrape too close to the skin which exudes an unpleasant milk substance. the fruit can also be scooped out and tossed lightly with lemon juice to retard browning then used in a fresh fruit salad.",
  "web_taxonomy" : "tropical fruits",
  "type" : "fruit",
  "composition" : "solid"
}
{
  "_id" : ObjectId("5507cca29547e66a6a1bb447"),
  "substitutes" : [
    "champagne grapes",
    "other small grapes"
  ],
  "name" : "baby kiwi",
  "nutrients" : {
    "total fat" : [
      "1g",
      "0%"
    ],
    "sodium" : [
      "5mg",
      "0%"
    ],
    "saturated fat" : [
      "0g",
      "0%"
    ],
    "potassium" : [
      "552g",
      "20%"
    ],
    "sugars" : [
      "16g",
      "0%"
    ],
    "calories" : [
      "108"
    ],
    "vitamin c" : " 0%",
    "calcium" : " 0%",
    "vitamin a" : " 0%",
    "iron" : " 0%",
    "dietary fiber" : [
      "5g",
      "20%"
    ],
    "total carbohydrate" : [
      "26g",
      "10%"
    ],
    "protein" : [
      "2g",
      "0%"
    ],
    "cholesterol" : [
      "0mg",
      "0%"
    ]
  },
  "healthy_descriptor" : null,
  "summary" : "a vine (actinidia ",
  "web_taxonomy" : "berries",
  "diet_descriptor" : [
    "vegan",
    "vegetarian",
    "pescatarian",
    "lactose-free"
  ],
  "type" : "fruit",
  "composition" : "solid"
}
```

## Inserting / Finding / etc. with MongoDB.
Just do everything in `kb.py`. Standard Mongo stuff -- `kb.insert()`, `kb.find()`, etc. Read the docs.

