import os
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from hardware.bartender import Bartender
from hardware.drinks import *  # this provides the drink list mentioned
from time import sleep
from threading import Thread

app = Flask(__name__)


# index (same as cocktail overvieuw)
@app.route('/')
def index():
    try:
        return render_template("drinks.html", drink_list=drink_list)
    except Exception as ex:
        print(ex)
        abort(404)


# detail cocktail
@app.route('/drinks')
def drinks():
    try:
        return render_template("drinks.html", drink_list=drink_list)
    except Exception as ex:
        print(ex)
        abort(404)


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


@app.route("/basic-menu")
def basicmenu():
    try:
        # request given item
        item = base64.decodestring(request.args.get("item"))
        type = base64.decodestring(request.args.get("type"))

        #emty var
        description = ""

        # small changes in name for more info
        if (type == "pump_selection"):
            description = "Select the drink installed in the machine"
        elif (type == "menu"):
            description = "Configure"
        elif (type == "clean"):
            description = "Clean the machine"
        elif (type == "back"):
            description = ""

        # sent besic page with menu item on
        return render_template("basic-menu.html", item=item, description=description)

    except Exception as ex:
        print(ex)
        abort(404)


# admin (alcohol, toggle, ...)
@app.route('/admin')
def admin():
    return render_template("admin.html")


# # path for config
# @app.route('/configure')
# def configure():
#     # basic configure page
#     return render_template("configure.html")
#
#
# # pump selection
# @app.route('/pumps')
# def pumps():
#     # request pump
#     pump = request.args.get("pump")
#     pump = base64.decodestring(pump)
#     # resuest list af available liquids
#     return render_template("pumps.html", pump=pump)
#
#
# # pump drink selection
# @app.route('/pump')
# def pump():
#     # request the drink from the menu
#     drink_in_menu = request.args.get("drink_in_menu")
#     # resuest list af available liquids
#     return render_template("pump.html", drink_in_menu=drink_in_menu)
#
#
# # clean machine
# @app.route('/clean')
# def clean():
#     return render_template("clean.html")
#
# #simple page to show back
# @app.route('/back')
# def back():
#     return render_template("back.html")


# starts the hw
def start_hardware():
    print("turning on hw")

    # set gpio
    Bartender.set_gpio()

    # make obj (make it global available)
    global bartender
    bartender = Bartender()

    # start
    bartender.start_operation()

def create_base64():
    # adds a base64 field from the name in order tot transfer
    # not the best way but no classes
    for drink in drink_list:
        drink["base64name"] = base64.encodestring(drink["name"])

#
def set_full_screen():
    # hit full screen (wat a bit)
    sleep(15)
    print("smashed F11")
    os.system("sudo xdotool key F11")


if __name__ == '__main__':
    try:
        # turn on hw, create base 64
        start_hardware()
        create_base64()

        # set full screen as threat
        screen_thread = Thread(target=set_full_screen)
        screen_thread.start()

        # set server vars
        # set port 8080
        port = int(os.environ.get("PORT", 8080))
        # set ip
        host = "169.254.55.5"
        # pas parms and set debug
        app.run(host=host, port=port, debug=False, threaded=True)

        #app.run(port=port, debug=False, threaded=True)


    except Exception as ex:
        print(ex)
        print("Interupted")

    finally:
        bartender.clean_gpio()
        print("Cleaned GPIO")
