from unittest import TestCase
from flask import session, request
from app import app, KEY
from models import db, bcrypt, User, Drink, Ingredients, Drinks_Ingredients, Favorite, Rating, Recommendation
from psycopg2 import errorcodes
from sqlalchemy import exc

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktails_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

class CocktailModelsTestCase(TestCase):
    """Testing models"""

    def setUp(self):       
        User.query.delete()
        self.client = app.test_client()
        self.user = User(
            username='testuser1',
            first_name='test',
            last_name='user',
            password='test1',
            email='test1@test.com',
        )     
        self.user_id = 11111
        self.user.id = self.user_id
        db.session.add(self.user)

    def tearDown(self):
        db.session.rollback()
    
    def test_user(self):       
        users = User.query.all()
        self.assertEqual(len(users),1)

    def test_add_remove_user(self):        
        new_user = User(
            username='testuser2',
            first_name='test2',
            last_name='user2',
            password='test2',
            email='test2@test.com',)
        new_user.id=11113
        db.session.add(new_user)
        users = User.query.all()
        new = User.query.filter(User.id==11113).first()
        self.assertEqual(len(users), 2)
        self.assertEqual(new.id, 11113)
        self.assertEqual(new.username, 'testuser2')
        self.assertEqual(new.first_name, 'test2')
        self.assertEqual(new.last_name, 'user2')
        self.assertEqual(new.password, 'test2')
        self.assertEqual(new.email, 'test2@test.com')
        db.session.delete(new)
        db.session.commit()
        check_user = User.query.get(11113)
        self.assertEqual(check_user, None)

    def test_user_signup(self):
        sign_user = User.signup(
            username='signuser',
            first_name='sign',
            last_name='user',
            password='signuser',
            email='sign@test.com',)
        users = User.query.all()
        sign = User.query.filter(User.username=='signuser').first()
        self.assertEqual(len(users),2)
        self.assertEqual(sign.username, 'signuser')
        self.assertEqual(sign.first_name, 'sign')
        self.assertEqual(sign.last_name, 'user')
        self.assertEqual(sign.email, 'sign@test.com')

    def test_drink(self):        
        drink1 = Drink.query.get(1)
        self.assertEqual(drink1.id,1)
        self.assertEqual(drink1.name,'A1')
        self.assertEqual(drink1.content,'Alcoholic')
        self.assertIn('serve over ice into a chilled glass',drink1.instructions)
        self.assertIn('2x8thr1504816928.jpg', drink1.image)
        self.assertEqual(drink1.glass,'Cocktail glass')
        self.assertEqual(drink1.drink_type,'Cocktail')

    def test_drink_add(self):
        new_drink = Drink(name='Test Drink', content="Alcoholic", instructions='Test instructions')
        new_drink.id = 10000
        db.session.add(new_drink)
        new = Drink.query.get(10000)
        self.assertEqual(new.id,10000)
        self.assertEqual(new.name,'Test Drink')
        self.assertEqual(new.content,'Alcoholic')
        self.assertEqual(new.instructions,'Test instructions')

    def test_drink_remove(self):
        new_drink = Drink(name='Delete Drink', content="Alcoholic", instructions='Delete instructions')
        new_drink.id = 10001
        db.session.add(new_drink)
        new = Drink.query.get(10001)
        db.session.delete(new)
        check_delete = Drink.query.filter(Drink.name=='Delete Drink').first()
        self.assertEqual(check_delete, None)

    def test_change_drink_info(self):
        change_drink = Drink(name='Change Drink', content="Alcoholic", instructions='Change instructions')
        change_drink.id = 10002
        db.session.add(change_drink)
        db.session.commit()
        change = Drink.query.get(10002)
        change.content = 'Non-alcoholic'
        db.session.commit()
        change_check = Drink.query.get(10002)
        self.assertEqual(change_check.content,'Non-alcoholic')
        db.session.delete(change_check)
        db.session.commit()

    def test_add_remove_change_ingred(self):
        new_ingredient = Ingredients(name='Test Ingred')
        new_ingredient.id = 10000
        db.session.add(new_ingredient)
        ingred = Ingredients.query.get(10000)
        self.assertEqual(ingred.id, 10000)
        self.assertEqual(ingred.name, 'Test Ingred')
        ingred.name = 'Change Ingred'
        db.session.commit() 
        self.assertEqual(ingred.name,'Change Ingred')
        db.session.delete(ingred)
        db.session.commit()
        delete_ingred = Ingredients.query.filter(Ingredients.name == 'Test2 Ingred').first()
        self.assertEqual(delete_ingred, None)

    def test_drink_ingred_add_remove_change(self):
        new_drink_ingred = Drinks_Ingredients(drink_id=1, ingredient_id=1, amount='5 mL')
        new_drink_ingred.id = 10000
        db.session.add(new_drink_ingred)
        drink_ingred = Drinks_Ingredients.query.get(10000)
        self.assertEqual(drink_ingred.drink_id, 1)
        self.assertEqual(drink_ingred.ingredient_id, 1)
        self.assertEqual(drink_ingred.amount, '5 mL')
        drink_ingred.amount = '10 oz'
        db.session.commit()
        self.assertEqual(drink_ingred.amount, '10 oz')
        db.session.delete(drink_ingred)
        db.session.commit()
        delete_drink_ingred = Drinks_Ingredients.query.get(10000)
        self.assertEqual(delete_drink_ingred, None)

    def test_recommend_add_remove(self):
        new_user = User(
            username='recuser',
            first_name='rec',
            last_name='user',
            password='recuser',
            email='recuser@test.com',)
        new_user.id = 11114
        db.session.add(new_user)
        new_rec = Recommendation(recommender_id=11114, recommend_to_user_id=11111, drink_id=1)
        new_rec.id = 10000
        db.session.add(new_rec)
        rec= Recommendation.query.get(10000)
        self.assertEqual(rec.id, 10000)
        self.assertEqual(rec.recommender_id, 11114)
        self.assertEqual(rec.recommend_to_user_id, 11111)
        self.assertEqual(rec.drink_id, 1)
        db.session.delete(rec)
        db.session.commit()
        check_rec = Recommendation.query.get(10000)
        self.assertEqual(check_rec, None)

    def test_add_remove_fav(self):
        new_fav = Favorite(user_id=11111, drink_id=1)
        new_fav.id = 10000
        db.session.add(new_fav)
        fav = Favorite.query.get(10000)
        self.assertEqual(fav.id, 10000)
        self.assertEqual(fav.user_id, 11111)
        self.assertEqual(fav.drink_id, 1)
        db.session.delete(fav)
        db.session.commit()
        check_fav = Favorite.query.get(10000)
        self.assertEqual(check_fav, None)

    def test_add_remove_change_rating(self):
        new_rating = Rating(rating=2.5, user_id=11111, drink_id=1)
        new_rating.id = 10000
        db.session.add(new_rating)
        rating = Rating.query.get(10000)
        self.assertEqual(rating.id, 10000)
        self.assertEqual(rating.rating, 2.5)
        self.assertEqual(rating.user_id, 11111)
        self.assertEqual(rating.drink_id, 1)
        rating.rating = 1.0
        db.session.commit()
        self.assertEqual(rating.rating, 1.0)
        db.session.delete(rating)
        db.session.commit()
        check_rating = Rating.query.get(10000)
        self.assertEqual(check_rating, None)