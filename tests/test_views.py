from unittest import TestCase
from flask import session, request
from app import app, KEY
from models import db, bcrypt, User, Drink, Ingredients, Drinks_Ingredients, Favorite, Rating, Recommendation
from forms import RegisterForm, LoginForm, RecommendForm
import random

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktails_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

class CocktailsViewsTestCase(TestCase):
    """Testing view functions"""

    def setUp(self):
        User.query.delete()
        self.client = app.test_client()
        user = User(
            username='testuser1',
            first_name='test',
            last_name='user',
            password='test1',
            email='test1@test.com',)        
        user_id = 999
        user.id = user_id
        db.session.add(user)

    def tearDown(self):
        db.session.rollback()

    def test_home(self):
        with self.client as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h3>Check out", str(resp.data))
            self.assertIn('<div class="column', str(resp.data))
            self.assertIn('<div class="card', str(resp.data))
            self.assertIn("More Info</a>", str(resp.data))
            self.assertIn('id="search_input"', str(resp.data))
            self.assertIn('id="search_btn"', str(resp.data))

    def test_logged_out_home(self):
        with self.client as client:
            resp = client.get('/')
            self.assertIn('id="nav_login"', str(resp.data))
            self.assertIn('id="nav_register"', str(resp.data))
    
    def test_logged_in_home(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999        
        resp = client.get('/')
        self.assertIn('id="nav_avatar"', str(resp.data))
        self.assertIn('id="nav_fav"', str(resp.data))
        self.assertIn('id="nav_recommends"', str(resp.data))
        self.assertIn('id="nav_logout"', str(resp.data))

    def test_get_signup(self):
        with self.client as client:
            resp = client.get('/user/signup')
            self.assertIn('<h2>Enter your information</h2>', str(resp.data))
            self.assertIn('id="signup_form"', str(resp.data))
            self.assertIn('id="username"', str(resp.data))
            self.assertIn('id="first_name"', str(resp.data))
            self.assertIn('id="last_name"', str(resp.data))
            self.assertIn('id="email"', str(resp.data))
            self.assertIn('id="password"', str(resp.data))
            self.assertIn('Sign up</button>', str(resp.data))

    def test_sign_up_invalid_user(self):
        with app.app_context():
            with self.client as client:
                with client.session_transaction() as sess:
                    sess[KEY]=1000
                form = RegisterForm()
                form.username.data = 'testuser1'
                form.first_name.data = 'test1'
                form.last_name.data = 'test'
                form.email.data = 'test_invalid@test.com'
                form.password.data = 'testinv'
                form.validate_on_submit()
                resp = client.post('/user/signup', data=form.data, follow_redirects=True)                
                self.assertIn('<h2>Enter your information</h2>', str(resp.data))
                self.assertIn('id="signup_form"', str(resp.data))

    def test_get_login_page(self):
        with self.client as client:
            resp = client.get('/user/login')
            self.assertIn('<h2>Enter your information</h2>', str(resp.data))
            self.assertIn('id="login_form"', str(resp.data))
            self.assertIn('name="username" placeholder="Username"', str(resp.data))
            self.assertIn('name="password" placeholder="Password"', str(resp.data))
            self.assertIn('Log In</button>', str(resp.data))

    def test_logout_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            resp = client.get('/user/logout', follow_redirects=True)
            self.assertIn('Logout successful</div>', str(resp.data))
            self.assertIn('<h3>Check out some of', str(resp.data))

    def test_not_logged_in_user_page(self):
        with self.client as client:
            resp = client.get('/user', follow_redirects=True)
            self.assertIn('<h3>Check out some of', str(resp.data))

    def test_logged_in_user_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999
            resp = client.get('/user')
            self.assertIn('<div class="column', str(resp.data))
            self.assertIn('<div class="card', str(resp.data))
            self.assertIn("More Info</a>", str(resp.data))

    def test_empty_search(self):
        with self.client as client:
            resp = client.get('/search', query_string={"search":""}, follow_redirects=True)            
            self.assertIn('Please enter a drink in the search bar</div>', str(resp.data))
            self.assertIn('<h3>Check out some of', str(resp.data))
            self.assertIn('<div class="column', str(resp.data))
            self.assertIn('<div class="card', str(resp.data))
            self.assertIn("More Info</a>", str(resp.data))
    
    def test_search(self):
        with self.client as client:
            resp = client.get('/search', query_string={"search":"mojito"}, follow_redirects=True)  
            self.assertIn('<div class="column', str(resp.data))
            self.assertIn('<div class="card', str(resp.data))
            self.assertIn("More Info</a>", str(resp.data))   
            self.assertIn("Mojito</h5>", str(resp.data))   
            self.assertIn("<li>Light rum</li>", str(resp.data))   
            self.assertIn("<li>Lime juice</li>", str(resp.data))   
            self.assertIn("<li>Sugar</li>", str(resp.data))   
            self.assertIn("<li>Mint</li>", str(resp.data))   
            self.assertIn("<li>Soda water</li>", str(resp.data))
            self.assertIn("Mojito #3</h5>", str(resp.data))  

    def test_drinks_first_page(self):
        with self.client as client:
            resp = client.get('/drinks/page1')
            self.assertIn('<table ', str(resp.data))
            self.assertIn('<thead>', str(resp.data))
            self.assertIn('<tr ', str(resp.data))
            self.assertIn('id</th>', str(resp.data))
            self.assertIn('Ingredients</th>', str(resp.data))
            self.assertIn('1</th>', str(resp.data))
            self.assertIn('25</th>', str(resp.data))
            self.assertIn('"/drinks/1">A1</a></td>', str(resp.data))
            self.assertIn('<li class="page-item">', str(resp.data))
            self.assertIn('1</a>', str(resp.data))
    
    def test_drinks_rand_page(self):
        rand_num = random.choice(range(2,16))        
        with self.client as client:
            resp = client.get(f'/drinks/page{rand_num}')
            self.assertIn(f'{rand_num}</a>', str(resp.data))
            self.assertIn(f'{((rand_num-1)*25)+1}</th>', str(resp.data))
            self.assertIn(f'{rand_num*25}</th>', str(resp.data))


    def test_drinks_last_page(self):
        with self.client as client:
            resp = client.get('/drinks/page17')
            self.assertIn('17</a>', str(resp.data))
            self.assertIn('401</th>', str(resp.data))
    
    def test_past_last_drinks_page(self):
        with self.client as client:
            resp = client.get('/drinks/page18', follow_redirects=True)
            self.assertIn("We&#39;re out of drinks!</div>", str(resp.data))
            self.assertIn('17</a>', str(resp.data))
            self.assertIn('401</th>', str(resp.data))

    def test_not_logged_in_favorite_page(self):
        with self.client as client:
            resp = client.get('/user/favorites', follow_redirects=True)
            self.assertIn("Log in to rate/favorite drinks</div>", str(resp.data))
            self.assertIn('<h3>Check out some of', str(resp.data))
            self.assertIn('<div class="column', str(resp.data))
            self.assertIn('<div class="card', str(resp.data))
            self.assertIn("More Info</a>", str(resp.data))

    def test_no_favorites_favorite_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            resp = client.get('/user/favorites')
            self.assertIn("<h4>Sorry you don", str(resp.data))
            self.assertIn("<footer>(Add to favorites ", str(resp.data))

    def test_favorite_page_with_favorite(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999
            new_fav = Favorite(id=1, user_id=999, drink_id=1)
            db.session.add(new_fav)
            resp = client.get('/user/favorites')
            self.assertIn('<div class="carousel-inner">', str(resp.data))       
            self.assertIn('<div class="card ', str(resp.data))       
            self.assertIn('<h5 class="card-title">A1</h5>', str(resp.data))       
            self.assertIn('<a href="/drinks/1"', str(resp.data))
            self.assertIn('<table ', str(resp.data))  
            self.assertIn('<thead>', str(resp.data))  
            self.assertIn('<tr ', str(resp.data))  
            self.assertIn('id</th>', str(resp.data))  
            self.assertIn('Name</th>', str(resp.data))  
            self.assertIn('Ingredients</th>', str(resp.data))  
            self.assertIn('<tbody>', str(resp.data))  
            self.assertIn('<tr>', str(resp.data))  
            self.assertIn('1</th>', str(resp.data))  
            self.assertIn('<td>', str(resp.data))  
            self.assertIn('<a href="/drinks/1">A1</a>', str(resp.data))  
            self.assertIn('Recommend</button>', str(resp.data))  
            self.assertIn('Remove</button>', str(resp.data))

    def test_add_fav_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999                
            resp = client.post('/user/favorites', json={'drinkId': '2'})                
            self.assertIn('<h5 class="card-title">ABC</h5>', str(resp.data))       
            self.assertIn('<a href="/drinks/2"', str(resp.data))
            self.assertIn('id</th>', str(resp.data))  
            self.assertIn('Name</th>', str(resp.data))  
            self.assertIn('Ingredients</th>', str(resp.data))   
            self.assertIn('2</th>', str(resp.data))    
            self.assertIn('<a href="/drinks/2">ABC</a>', str(resp.data))
            fav = Favorite.query.filter(Favorite.drink_id==2).first()
            db.session.delete(fav)
            db.session.commit()

    def test_delete_fav_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999           
            fav = Favorite(id=10000, user_id=999, drink_id=3)
            db.session.add(fav)    
            resp = client.post('/user/favorites', json={'drinkId': '3'})
            self.assertIn("<h4>Sorry you don", str(resp.data))
            self.assertIn("<footer>(Add to favorites ", str(resp.data))
    
    def test_logged_out_drink_info_page(self):
        with self.client as client:            
            resp = client.get('/drinks/1')
            self.assertIn('Log in to rate/favorite drinks</div>', str(resp.data))
            self.assertIn('<div class="jumbotron ', str(resp.data))
            self.assertIn('A1', str(resp.data))
            self.assertIn('<li>Gin - 1 3/4 shot', str(resp.data))
            self.assertIn('Back</button>', str(resp.data))

    def test_logged_in_drink_info_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999
            resp =client.get('/drinks/1')            
            self.assertIn('<div class="jumbotron ', str(resp.data))
            self.assertIn('A1', str(resp.data))
            self.assertIn('<i id="fav" class="fas fa-cocktail', str(resp.data))
            self.assertIn('<form id="1form"', str(resp.data))
            self.assertIn('<input id="slider"', str(resp.data))
            self.assertIn('Update Rating</button>', str(resp.data))
            self.assertIn('/5</h5>', str(resp.data))
            self.assertIn('<li>Gin - 1 3/4 shot', str(resp.data))
            self.assertIn('Back</button>', str(resp.data))

    def test_rate_drink_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            resp = client.post('/drinks/1', json={'rating': '3'}, follow_redirects=True)
            self.assertIn('3.0/5</h5>', str(resp.data))
            rating = Rating.query.filter(Rating.user_id==999).first()
            db.session.delete(rating)
            db.session.commit()

    def test_rate_drink_update_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            resp = client.post('/drinks/1', json={'rating': '4.5'}, follow_redirects=True)
            self.assertIn('4.5/5</h5>', str(resp.data))
            rating = Rating.query.filter(Rating.user_id==999).first()
            db.session.delete(rating)
            db.session.commit()


    def test_logged_out_recommend_page(self):
        with self.client as client:
            resp = client.get('/user/recommendations', follow_redirects=True)
            self.assertIn('Please log in or sign up to get recommendations</div>', str(resp.data))
            self.assertIn('<h3>Check out some of', str(resp.data))

    def test_no_recommends_recommend_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            resp = client.get('/user/recommendations')
            self.assertIn("You don\\\'t have any recommendations yet", str(resp.data))

    def test_one_recommend_recommends_page(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999            
            new_user = User(username='test2', first_name='test2', last_name='user', email='test2@test.com', password='test2')
            new_id = 1001
            new_user.id = new_id
            db.session.add(new_user)
            new_recommend = Recommendation(recommender_id=new_user.id, recommend_to_user_id=999, drink_id='1')
            db.session.add(new_recommend)
            resp = client.get('/user/recommendations')            
            self.assertIn('<table ', str(resp.data))
            self.assertIn('<thead>', str(resp.data))
            self.assertIn('Name</th>', str(resp.data))
            self.assertIn('Recommended by</th>', str(resp.data))
            self.assertIn('<tbody>', str(resp.data))
            self.assertIn('1</td>', str(resp.data))
            self.assertIn('<a href="/drinks/1">A1</a>', str(resp.data))
            self.assertIn('test2</td>', str(resp.data))
            self.assertIn('Remove</button>', str(resp.data))

    def test_delete_recommend_post(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999
            new_user = User(
                id=1002,
                username='testuser3',
                first_name='test',
                last_name='user3',
                password='test3',
                email='test3@test.com',)
            db.session.add(new_user)
            new_recommend = Recommendation(recommender_id=1002, recommend_to_user_id=999, drink_id='1')
            rec_id = 9999
            new_recommend.id = rec_id
            db.session.add(new_recommend)
            resp = client.post('/user/recommendations', json={'recId': 9999}, follow_redirects=True)
            self.assertIn("You don\\\'t have any recommendations yet", str(resp.data))           
            del_new_user = User.query.get(1002)
            db.session.delete(del_new_user)         

    def test_logged_out_rec_form(self):
        with self.client as client:
            resp = client.get('/user/recommend/form1', follow_redirects=True)
            self.assertIn('Please log in or sign up to send recommendations</div>', str(resp.data))
            self.assertIn('<h3>Check out some of', str(resp.data))

    def test_logged_in_rec_form(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[KEY]=999
            resp = client.get('/user/recommend/form1')
            self.assertIn('Select a user to send recommendation to</h3>', str(resp.data))
            self.assertIn('<form action="/user/recommend/form1"', str(resp.data))
            self.assertIn('disabled id="username" name="username" placeholder="User Name"', str(resp.data))
            self.assertIn('<select ', str(resp.data))
            self.assertIn('name="recommend_to_name" placeholder="Recommend To"', str(resp.data))
            self.assertIn('disabled id="drink" name="drink" placeholder="Drink Name"', str(resp.data))