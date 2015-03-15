# Recipe Transformer

Project by Kevin Chen, Brittany Lee, Kevin Broh-Kahn, and Bhavita Jaiswal!

This project is built off of a Flask boilerplate - [https://github.com/mjhea0/flask-boilerplate/](https://github.com/mjhea0/flask-boilerplate)

## Quick Start
1. Clone the repo
  ```
  $ git clone git@github.com:blee42/eecs337.git
  $ cd flask-boilerplate
  ```

2. Make a virtual environment.  We are using the virtualenvwrapper; if you have not used it before the installation docs can be seen [http://virtualenvwrapper.readthedocs.org/en/latest/install.html](here).
  ```
  $ mkvirtualenv env
  $ workon env
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Run the development server:
  ```
  $ python app.py
  ```

5. Navigate to [http://localhost:5000](http://localhost:5000)

## Starting MongoDB
1. Have MongoDB installed and Flask PyMongo installed via PIP (TODO: add to README).
2. Make the `data/db` folder.
  ```
  $ mkdir data/db
  ```

3. Start MongoDB in a separate shell window.
  ```
  $ mongo --dbpath data/db/
  ```

4. Do whatever else you want to.

## Populating the DB initially

`populate_kb.py` contains code for quickly populating the database with some 2000 or so ingredients. The data still needs to be refined, but everyone should scrape the data first and wait for a later script to modify all database entries.

Just run `get_ingredients()` and it should do the right thing. This will take ~20 mins.

## Inserting / Finding / etc. with MongoDB.
Just do everything in `kb.py`. Standard Mongo stuff -- `kb.insert()`, `kb.find()`, etc. Read the docs.

