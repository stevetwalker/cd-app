"""
Topic and problem database ('topics').
Non-relational db with one document per topic.

Document structure:
    {**'topic_id': 't44',        #unique
     **'topic': 'Two-Step Equations with Division (integer answers)', #unique
     **'instructions': 'Solve each equation.'
     **'category': 'Solving Equations and Inequalities',
     **'sub_categories': {
        1: 'Two-Step Equations',
        2: 'Division Required'},
     **'integers_only': 'y',    #y for yes, n for no (re: answers allowed)
     'positive_only': 'n',      #y for yes, n for no (re: answers allowed)
     'equation': 'a+b=c',
     'variables': {
        'a': {
            'min': -20,
            'max': 20,
            'zero_ok': 'n',     #y for yes, n for no, None for not applicable
            'num_type': 'i'}    #i for integer, d for decimal
         ...}
     'problems': [
        {**'problem_id': 'p4245'            #unique
         'values': {'a': 10, 'b': 7, 'c': 27, 'x': [2]},
         'problem': '10x+7=27', #LaTeX string
         'answer': 'x=2'},      #LaTeX string
        ...]
    }

**Not yet implemented
"""

# pylint: disable=W1202

import logging
from pymongo import MongoClient


class MongoDBConnection():
    """Establish MongoDB connection."""

    def __init__(self, host='127.0.0.1', port=27017): # Set to localhost
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def write_to_topics_db(equation_dict):
    """Import equation details and problem combos to MongoDB."""

    logging.info("Initializing MongoDB.")
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        logging.info("Accessing topics database.")
        topics = database['topics'] # Creates equations db if it doesn't exist yet
        logging.info(f"Currently {topics.count_documents({})} in db.")

        try:
            topics.insert_one(equation_dict)
            logging.info(f"Data from {equation_dict['equation']} added to database.")
            logging.info(f"Now {topics.count_documents({})} in db.")

        except Exception as err:
            logging.error(err)


def display_topics_db():
    """Display the contents of the equations database."""

    logging.info("Initializing MongoDB.")
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.media

        logging.info("Accessing topics database.")
        docs = database['topics'].find()

        for doc in docs:
            print(doc)
