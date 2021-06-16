from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Drink, Recommendation, Ingredients, Favorite, Rating, Drinks_Ingredients
from functions import login, logout, get_fav_drink_dict, get_fav_drink_ingredients, get_drink_ingredients, get_count_dict, get_fav_ingredient
from forms import RegisterForm, LoginForm, RecommendForm
from sqlalchemy.sql import func
import random
KEY = "user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "raise_a_spirit"
# toolbar = DebugToolbarExtension(app)

connect_db(app)