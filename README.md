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
1. Have MongoDB installed.
2. Make the `data/db` folder.
  ```
  $ mkdir data/db
  ```
3. Start MongoDB in a separate shell window.
  ```
  $ mongo --dbpath data/db/
  ```
4. Do whatever else you want to.

## Inserting / Finding / etc. with MongoDB.
Just do everything in `kb.py`. Standard Mongo stuff -- `kb.insert_one`, `kb.insert_many`, `kb.find()`, etc. Read the docs.

