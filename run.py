import os
import threading
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from hardware.bartender import Bartender
from hardware.drinks import *   #this provides the drink list mentioned
from threading import Thread
app = Flask(__name__)


# index
@app.route('/')
def index():
    return render_template("drinks.html", drink_list=drink_list)


# detail cocktail
@app.route('/drinks')
def drinks():
    return render_template("drinks.html", drink_list=drink_list)


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


# configure pump
@app.route('/pumps')
def detail():
    # request pump
    pump = request.args.get("pump")
    # resuest list af available liquids
    return render_template("pumps.html", pump=pump)


# admin (alcohol, toggle, ...)
@app.route('/admin')
def admin():
    return render_template("admin.html")


# starts the hw
def start_hardware():
    # adds a base64 field from the name in order tot transfer
    for drink in drink_list:
        drink["base64name"] = base64.encodestring(drink["name"])

    # set gpio
    Bartender.set_gpio()
    # make obj
    bartender = Bartender()
    # start as thread
    thread = Thread(target=bartender.start_operation)
    thread.start()



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
        Bartender.clean_gpio()
        print("Cleaned GPIO")
