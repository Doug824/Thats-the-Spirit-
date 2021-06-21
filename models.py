from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    @classmethod
    def register(cls, username, first_name, last_name, email, password):
        """register user. Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class Drink(db.Model):
    """Drinks"""
    __tablename__ = 'drinks'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    name = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False) #alcoholic vs non-alcoholic
    instructions = db.Column(db.Text, nullable = False)
    image = db.Column(db.String)
    glass = db.Column(db.String)
    drink_type = db.Column(db.String)


class Ingredients(db.Model):
    """Drink ingredients"""
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    name = db.Column(db.String, nullable = False)


class Drinks_Ingredients(db.Model):
    """Holds drink id and ingredient id and amount"""
    __tablename__ = 'drinks_ingredients'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete = 'cascade'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete = 'cascade'))
    amount = db.Column(db.String, nullable = False)


class Recommendation(db.Model):
    """Recommendations"""
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    recommender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))
    recommend_to_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete = 'cascade'))


class Favorite(db.Model):
    """Favorites"""
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete = 'cascade'))


class Rating(db.Model):
    """Ratings for drinks"""
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
    rating = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete = 'cascade'))