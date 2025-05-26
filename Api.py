import requests
from Config import API_KEY
from Pantry import get

def get_recipes():
    items = get()
    query = ",".join(k.split(" (")[0] for k in items.keys())

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": query,
        "number": 15,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": API_KEY
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


