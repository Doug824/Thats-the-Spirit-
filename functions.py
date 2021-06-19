from flask import session, g
from models import User, Drink, Ingredients, Drinks_Ingredients, Recommendation, Favorite, Rating
KEY = 'user'

#Seed file functions for db: cocktails
drinks_dict = {}

def get_name(dictionary, i, key):
    try:
        name = dictionary[key]['drinks'][i]['strDrink']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['name'] = name
    return drinks_dict


def get_alc_content(dictionary, i, key):
    try:
        content = dictionary[key]['drinks'][i]['strAlcoholic']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['content'] = content
    return drinks_dict


def get_instructions(dictionary, i, key):
    try:
        instructions = dictionary[key]['drinks'][i]['strInstructions']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['instructions'] = instructions
    return drinks_dict


def get_image(dictionary, i, key):
    try:
        image = dictionary[key]['drinks'][i]['strDrinkThumb']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['image'] = image
    return drinks_dict


def get_ingredients(dictionary, i, key):
    ingredients = {}
    for num in range(1,15):
        try:
            ingredients[f'{num}'] = dictionary[key]['drinks'][i][f'strIngredient{num}']
        except KeyError:
            return
        if ingredients[f'{num}'] == None:
            ingredients.pop(f'{num}', 'Key not in dictionary')
            break
    drinks_dict[key][f'{str(i+1)}']['ingredients'] = ingredients
    return drinks_dict


def get_measurements(dictionary, i, key):
    measurements = {}
    for num in range(1,15):
        try:
            measurements[f'{num}'] = dictionary[key]['drinks'][i][f'strMeasure{num}']
        except KeyError:
            return
        if measurements[f'{num}'] == None:
            measurements.pop(f'{num}', 'Key not in dictionary')
            break
    drinks_dict[key][f'{str(i+1)}']['measurements'] = measurements
    return drinks_dict


def get_glass(dictionary, i, key):
    try:
        glass = dictionary[key]['drinks'][i]['strGlass']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['glass'] = glass
    return drinks_dict


def get_type(dictionary, i, key):
    try:
        drink_type = dictionary[key]['drinks'][i]['strCategory']
    except KeyError:
        return
    drinks_dict[key][f'{str(i+1)}']['drink_type'] = drink_type
    return drinks_dict


#################### Functions used in app file #################################


def login(user):
    """Log in user."""
    session[KEY] = user.id


def logout():
    """Logout user."""
    if KEY in session:
        del session[KEY]


def get_fav_drink_dict(favs):
    """Set up favorite drinks dict"""
    drinks = {}   
    for fav in favs:
        drink = Drink.query.get(fav.drink_id)
        drinks[fav.id]= drink            
    return drinks


def get_fav_drink_ingredients(drinks):
    """Get ingredients from favorite drinks dict for favorites page"""
    drink_ingreds = {}
    for drink in drinks:
        ingredients_list = []
        ingredients = Drinks_Ingredients.query.filter(Drinks_Ingredients.drink_id==drinks[drink].id).all()
        for ingredient in ingredients:
            find_ingredient = Ingredients.query.filter(Ingredients.id==ingredient.ingredient_id).first()
            ingredients_list.append(find_ingredient.name)
        drink_ingreds[drinks[drink].id] = ingredients_list
    return drink_ingreds


def get_drink_ingredients(drinks):
    """Get ingredients to list on all drinks page and for search"""
    drink_ingreds = {}
    for drink in drinks:
        ingredients_list = []
        ingredients = Drinks_Ingredients.query.filter(Drinks_Ingredients.drink_id==drink.id).all()
        for ingredient in ingredients:
            find_ingredient = Ingredients.query.filter(Ingredients.id==ingredient.ingredient_id).first()
            ingredients_list.append(find_ingredient.name)
        drink_ingreds[drink.id] = ingredients_list    
    return drink_ingreds


def get_count_dict(drink_ingreds):
    """Creates a dictionary containing the ingredients of the users favorite drinks and how many times
    each ingredient is used"""
    ingredients_list=[]
    count_dict = {}
    count = 0
    for drink_id in drink_ingreds:
        for ingredient in drink_ingreds[drink_id]:
            if ingredient in ingredients_list:
                count += 1
                count_dict[ingredient] = count
            else:
                ingredients_list.append(ingredient)
                count_dict[ingredient] = 1
    return count_dict


def get_fav_ingredient(count_dict):
    """Creates dictionary with favorite ingredient and how many times that ingredient
    is used in all of the users favorite drinks"""
    fav_ingredient_dict = {}
    highest = 0
    for count_name in count_dict:
        if count_dict[count_name] > highest:
            fav_ingredient_dict = {}
            highest = count_dict[count_name]
            fav_ingredient_dict[count_name] = highest    
    return fav_ingredient_dict