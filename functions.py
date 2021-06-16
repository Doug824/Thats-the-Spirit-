from flask import session, g
from models import User, Drink, Ingredients, Drinks_Ingredients, Recommendation, Favorite, Rating
KEY = 'user'

#Seed file functions for db: cocktails
drinks_dict = {}