import json, os

PANTRY_FILE = "pantry.json"
pantry = {}

def load():
    global pantry
    if os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "r") as f:
            pantry = json.load(f)
    else:
        pantry = {}

def save():
    if pantry:
        with open(PANTRY_FILE, "w") as f:
            json.dump(pantry, f)

def add(name, amount):
    name = name.lower().strip()
    pantry[name] = pantry.get(name, 0) + amount
    save()

def remove(name):
    name = name.lower().strip()
    if name in pantry:
        del pantry[name]
        save()

def update(name, delta):
    name = name.lower().strip()
    if name in pantry:
        pantry[name] += delta
        if pantry[name] <= 0:
            remove(name)
        else:
            save()

def get():
    return pantry.copy()

