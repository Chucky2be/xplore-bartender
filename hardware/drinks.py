import uuid
import base64

drink_list = [
    {
        "name": "Rum & Coke",
        "ingredients": {
            "rum": 50,
            "coke": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/rumcoke.jpg",
        "description_short": "Highball cocktail",
        "description": "Rum and Coke or Cuba Libre is a highball cocktail consisting of cola and rum. The cocktail originated in the early 20th century in Cuba after the country won independence in the Spanish-American War.",
        "id": "e9fa34eb-6530-4bb4-9719-ed167575b850"
    }, {
        "name": "Gin & Tonic",
        "ingredients": {
            "gin": 50,
            "tonic": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/gintonic.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "ee6a4efd-afe2-49a3-9e96-e37da19c9948"
    }, {
        "name": "Long Island",
        "ingredients": {
            "gin": 15,
            "rum": 15,
            "vodka": 15,
            "tequila": 15,
            "coke": 100,
            "oj": 30
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/longislandicetea.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "14434d4e-ab93-4cbb-9399-6e55a0d75f24"
    }, {
        "name": "Screwdriver",
        "ingredients": {
            "vodka": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/noimage.png",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "1d25d4c6-0de3-4f91-9cbb-a0c2cefdde34"
    }, {
        "name": "Margarita",
        "ingredients": {
            "tequila": 50,
            "mmix": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/margarita.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "6367a5a5-86a1-4762-ad2d-18851835b029"
    }, {
        "name": "Gin & Juice",
        "ingredients": {
            "gin": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/ginjuce.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "366802db-b5fd-4c41-9df3-9c4aa4da5056"
    }, {
        "name": "Tequila Sunrise",
        "ingredients": {
            "tequila": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/tequilasunrise.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "d20e446b-9863-47eb-991d-a0ca62087819"
    }, {
        "name": "Cola",
        "ingredients": {
            "coke": 200
        },
        "alcoholic": False,
        "img": "../static/img/cocktails/cola.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "5b6a7177-1bc7-4d01-9338-c5d46916ce30"
    }, {
        "name": "Orange Juce",
        "ingredients": {
            "oj": 200
        },
        "alcoholic": False,
        "img": "../static/img/cocktails/orangejuice.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok cooking",
        "id": "55cd19cd-922b-4337-8ddd-87da57f9cc68"
    }
]

drink_options = [
    {"name": "Gin", "value": "gin"},
    {"name": "Rum", "value": "rum"},
    {"name": "Vodka", "value": "vodka"},
    {"name": "Tequila", "value": "tequila"},
    {"name": "Tonic Water", "value": "tonic"},
    {"name": "Coke", "value": "coke"},
    {"name": "Orange Juice", "value": "oj"},
    {"name": "Margarita Mix", "value": "mmix"}
]

drink_dict = {}

# converts the above list into dict so it becomes searchable
def list_to_dict():
    for drink in drink_list:
        drink_dict[refactor_name(drink["name"])] = drink

# refactors the name so it is an allowed name (url)
def refactor_name(name):
    try:
        return base64.encodestring(name).replace("\n", "")

    except:
        raise Exception("Not a supported format")

# gets the drink by name
def get_drink_from_name(base64name):

    try:
        # if dict is still empty or key not found update
        if drink_dict == {} or base64name not in drink_dict.keys():
            list_to_dict()

        return drink_dict[base64name]

    except Exception as ex:
        #throw ex if not found
        raise Exception("Id not found, probaly not in dict")



