# Recipe Transformer

Project by Kevin Chen, Brittany Lee, Kevin Broh-Kahn, and Bhavita Jaiswal!

This project is built off of a Flask boilerplate - [https://github.com/mjhea0/flask-boilerplate/](https://github.com/mjhea0/flask-boilerplate). Built and tested with Mongo 2.6.4 and Python 2.7.6.

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

4. Install & start MongoDB (see below)

4. Run the development server:
  ```shell
  $ python app.py
  ```

5. Navigate to [http://localhost:5000](http://localhost:5000)

## Starting MongoDB
1. Have MongoDB and Flask PyMongo installed (the latter should be installed if you did `pip install` above.
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

The first you start the server will require populate the knowledge base with a couple thousand entries, so sit tight.

`populate_kb.py` contains this code feel free to also just run `run()` -- this'll also clear the KB, so if it glitches out or something, just rerun it here.

example data:
```JSON
{
  "_id" : "5507cca29547e66a6a1bb447",
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

