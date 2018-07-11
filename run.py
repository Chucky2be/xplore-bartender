import os
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from hardware.bartender import Bartender
from hardware.drinks import *   #this provides the drink list mentioned
from threading import Thread
app = Flask(__name__)


# index (same as cocktail overvieuw)
@app.route('/')
def index():
    return render_template("drinks.html", drink_list=drink_list)


# detail cocktail
@app.route('/drinks')
def drinks():
    return render_template("drinks.html", drink_list=drink_list)


# path for one drink
@app.route("/drink")
def drink():
    # request if cocktail was given
    drink_name = request.args.get("drink")

    # if coctail does not exist throw 404
    try:
        drink = get_drink_from_name(drink_name)
        return render_template("drink.html", drink=drink)
    except Exception as ex:
        print(ex)
        abort(404)


# path for config
@app.route('/configure')
def configure():
    # basic configure page
    return render_template("configure.html")


# pump selection
@app.route('/pumps')
def pumps():
    # request pump
    pump = request.args.get("pump")
    pump = base64.decodestring(pump)
    # resuest list af available liquids
    return render_template("pumps.html", pump=pump)


# pump drink selection
@app.route('/pump')
def pump():
    # request the drink from the menu
    drink_in_menu = request.args.get("drink_in_menu")
    # resuest list af available liquids
    return render_template("pump.html", drink_in_menu=drink_in_menu)


# clean machine
@app.route('/clean')
def clean():
    return render_template("clean.html")

#simple page to show back
@app.route('/back')
def back():
    return render_template("back.html")

# admin (alcohol, toggle, ...)
@app.route('/admin')
def admin():
    return render_template("admin.html")


# starts the hw
def start_hardware():
    print("turning on hw")

    # adds a base64 field from the name in order tot transfer
    # not the best way but no classes
    for drink in drink_list:
        drink["base64name"] = base64.encodestring(drink["name"])

    # set gpio
    Bartender.set_gpio()

    # make obj (make it global available)
    global bartender
    bartender = Bartender()

    #start as thread
    # thread = Thread(target=bartender.start_operation)
    # thread.start()

    bartender.start_operation()



if __name__ == '__main__':
    try:
        # turn on hw
        start_hardware()

        # set server vars
        # set port 8080
        port = int(os.environ.get("PORT", 8080))
        # set ip
        host = "169.254.55.5"
        # pas parms and set debug
        app.run(host=host, port=port, debug=False, threaded=True)
        #app.run(port=8080, debug=True, threaded=True)


    except Exception as ex:
        print(ex)
        print("Interupted")

    finally:
        bartender.clean_gpio()
        print("Cleaned GPIO")
