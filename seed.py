from app import db
from models import User, Drink, Recommendation, Favorite, Ingredients, Drinks_Ingredients
import requests
import json
from functions import drinks_dict, get_name, get_alc_content, get_instructions, get_image, get_ingredients, get_measurements, get_glass, get_type

####################### Get data from API and manipulate it to fill out DB as needed ##################

db.drop_all()
db.create_all()
i = 0
j = 0
k = 1
alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
api_dict = {}

for letter in alph:
    api_dict[f'{j+1}'] = {}
    drinks = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}')
    api_dict[f'{j+1}'] = json.loads(drinks.text)
    j = j + 1


for key in api_dict:
    drinks_dict[f'{key}'] = {}
    if api_dict[key]['drinks'] is None:
        continue
    for drink in api_dict[key]['drinks']:
        drinks_dict[key][f'{i+1}'] = {}
        get_name(api_dict, i, key)
        get_alc_content(api_dict, i, key)
        get_instructions(api_dict, i, key)
        get_image(api_dict, i, key)
        get_ingredients(api_dict, i, key)
        get_measurements(api_dict, i, key)
        get_glass(api_dict, i, key)
        get_type(api_dict, i, key)
        i = i + 1
    i = 0


for key in drinks_dict:
    for drink in drinks_dict[key]:
        name = drinks_dict[key][drink]['name']
        content = drinks_dict[key][drink]['content']
        instructions = drinks_dict[key][drink]['instructions']
        image = drinks_dict[key][drink]['image']
        ingredients = drinks_dict[key][drink]['ingredients']
        measurements = drinks_dict[key][drink]['measurements']
        glass = drinks_dict[key][drink]['glass']
        drink_type = drinks_dict[key][drink]['drink_type']
        new_drink = Drink(name=name, content=content, instructions=instructions, image=image, glass=glass, drink_type=drink_type)
        db.session.add(new_drink)
        db.session.commit()
        q_drink = Drink.query.filter(Drink.name==name).first()
        
        for ingredient in ingredients:          
            ingredient_check = Ingredients.query.filter(Ingredients.name.ilike(f'%{ingredients[ingredient]}%')).first()
            if ingredient_check == None:
                new_ingredient = Ingredients(name=ingredients[ingredient])
                db.session.add(new_ingredient)
                db.session.commit()
            else:
                continue   
        for ingredient in ingredients:
            try:
                measurements[ingredient]
            except KeyError:
                measurements[ingredient] = 'desired amount'
            find_ingredient = Ingredients.query.filter(Ingredients.name.ilike(f'%{ingredients[ingredient]}%')).first()
            new_drink_ingredient = Drinks_Ingredients(drink_id=q_drink.id, ingredient_id=find_ingredient.id, amount=measurements[ingredient])
            db.session.add(new_drink_ingredient)
            db.session.commit()