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
        "description": "Rum and Coke or Cuba Libre is a highball cocktail consisting of cola and rum. The cocktail originated in the early 20th century in Cuba after the country won independence in the Spanish-American War."
    }, {
        "name": "Gin & Tonic",
        "ingredients": {
            "gin": 50,
            "tonic": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/gintonic.jpg",
        "description_short": "Highball cocktail",
        "description": "A gin and tonic is a highball cocktail made with gin and tonic water poured over ice. It is usually garnished with a slice or wedge of lime. The amount of gin varies according to taste. Suggested ratios of gin to tonic are between 1:1 and 1:3."
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
        "description_short": "Highball cocktail",
        "description": "A Long Island Iced Tea is a type of alcoholic mixed drink typically made with vodka, tequila, light rum, triple sec, gin, and a splash of cola, which gives the drink the same amber hue as its namesake. A popular version mixes equal parts vodka, gin, rum, triple sec, with 1 1/2 parts sour mix and a splash of cola. Lastly, it is decorated with the lemon and straw, after stirring with bar spoon smoothly."
    }, {
        "name": "Screwdriver",
        "ingredients": {
            "vodka": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/noimage.png",
        "description_short": "Highball cocktail",
        "description": "A screwdriver is a popular alcoholic highball drink made with orange juice and vodka. While the basic drink is simply the two ingredients, there are many variations; the most common one is made with one part vodka, one part of any kind of orange soda, and one part of orange juice. Many of the variations have different names in different parts of the world."
    }, {
        "name": "Margarita",
        "ingredients": {
            "tequila": 50,
            "mmix": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/margarita.jpg",
        "description_short": "Alcoholic",
        "description": "A margarita is a cocktail consisting of tequila, orange liqueur, and lime juice often served with salt on the rim of the glass. The drink is served shaken with ice (on the rocks), blended with ice (frozen margarita), or without ice (straight up). Although it has become acceptable to serve a margarita in a wide variety of glass types, ranging from cocktail and wine glasses to pint glasses and even large schooners, the drink is traditionally served in the eponymous margarita glass, a stepped-diameter variant of a cocktail glass or champagne coupe."
    }, {
        "name": "Gin & Juice",
        "ingredients": {
            "gin": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/ginjuce.jpg",
        "description_short": "Alcoholic",
        "description": "Gin & Juice is a cocktail consisting of 1/4 gin and 3/ orange juice."
    }, {
        "name": "Tequila Sunrise",
        "ingredients": {
            "tequila": 50,
            "oj": 150
        },
        "alcoholic": True,
        "img": "../static/img/cocktails/tequilasunrise.jpg",
        "description_short": "Alcoholic",
        "description": "The Tequila Sunrise is a cocktail made of tequila, orange juice, and grenadine syrup and served unmixed in a tall glass. The modern drink originates from Sausalito in the early 1970s, after an earlier one created in the 1930s in Phoenix, near Scottsdale. The cocktail is named for its appearance when served, with gradations of colour resembling a sunrise."
    }, {
        "name": "Cola",
        "ingredients": {
            "coke": 200
        },
        "alcoholic": False,
        "img": "../static/img/cocktails/cola.jpg",
        "description_short": "Non-Alcoholic",
        "description": "Cola is a sweetened, carbonated soft drink, made from ingredients that contain caffeine from the kola nut and non-cocaine derivatives from coca leaves, flavoured with vanilla and other ingredients. With the primary exception of Coca-Cola, most colas now use other flavouring (and caffeinating) ingredients than kola nuts and coca leaves with a similar taste."
    }, {
        "name": "Orange Juce",
        "ingredients": {
            "oj": 200
        },
        "alcoholic": False,
        "img": "../static/img/cocktails/orangejuice.jpg",
        "description_short": "Non-Alcoholic",
        "description": "Orange juice is the liquid extract of the orange tree fruit, produced by squeezing oranges. It comes in several different varieties, including blood orange, navel oranges, valencia orange, clementine, and tangerine. ",
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



