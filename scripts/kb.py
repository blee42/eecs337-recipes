from pymongo import MongoClient
from enum import Enum


db = MongoClient().app
kb = db.kb

def insert_fixtures():
    if kb.count() == 0:
        examples = [
            {
                'name': 'chicken',
                'type': 'protein',
                'diet_descriptor': [],
                'healthy_descriptor': [],
                'cuisine': [], # some long list of cuisine types
            }
        ]
        kb.insert_many(examples)
