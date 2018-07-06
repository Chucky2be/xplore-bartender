import uuid

drink_list = [
    {
        "name": "Rum & Coke",
        "ingredients": {
            "rum": 50,
            "coke": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/rumcoke.jpg",
        "description_short": "Bangkok",
        "description": "Bangkok bangerang",
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


def list_to_dict():
    for cocktail in drink_list:
        drink_dict[cocktail["name"].replace(" ","")] = cocktail


def get_drink_from_id(name):
    try:
        if drink_dict == {}:
            list_to_dict()

        return drink_dict[name.replace(" ","")]

    except Exception as ex:
        raise Exception("Id not found, probaly not in dict")



