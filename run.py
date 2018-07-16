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
drink_making_web = True


# region Webpages
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
@app.route("/drink", methods=["GET"])
def drink():
    # request if cocktail was given
    drink_name = request.args.get("drink")

    # if coctail does not exist throw 404
    try:
        drink = get_drink_from_base64name(drink_name)
        return render_template("drink.html", drink=drink, drink_making_web=drink_making_web)
    except Exception as ex:
        print(ex)
        abort(404)


@app.route("/drink", methods=["POST"])
def drink_post():

    try:
        if drink_making_web == True:
            # request if cocktail was given
            drink_name = request.args.get("drink")

            # if coctail does not exist throw 404
            try:
                drink = get_drink_from_base64name(drink_name)
                bartender.makeDrink(drink["name"], drink["ingredients"])

            except Exception as ex:
                print(ex)
                abort(404)
        else:
            abort(403)


    except Exception as ex:
        print(ex)
        abort(400)


@app.route("/making")
def making():
    try:
        drink_name =  request.args.get("drink")
        drink = get_drink_from_base64name(drink_name)

        return render_template("making.html", drink = drink)

    except Exception as ex:
        print(ex)


@app.route("/basic-menu")
def basicmenu():
    try:
        # request given item
        item = base64.decodestring(request.args.get("item"))
        type = base64.decodestring(request.args.get("type"))

        # emty var
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


# settings (alcohol, toggle, ...)
@app.route('/settings', methods=['GET'])
def settings():
    try:
        return render_template("settings.html", pump_config="", )
    except:
        abort(400)


@app.route('/settings', methods=['POST'])
def settings_post():
    try:
        #key = request.args.get("key")
        form_type = (request.form['type'])

        if form_type ==  "clean":
            bartender.clean()

        elif form_type == "shutdown":
            bartender.shutdown()

        elif form_type == "drink_making_web_enable":
            try:
                if request.form["drink_making_web_enable"] == '1':
                    drink_making_web = True

            except:
                drink_making_web = False

    except:
        abort(400)


# endregion


# region Normal Functions
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


# adds a base64 field from the name in order tot transfer
# not the best way but no classes
def create_base64():
    for drink in drink_list:
        drink["base64name"] = base64.encodestring(drink["name"])


# function, "presses" f11 for firefox fullscreen
def set_full_screen():
    # hit full screen (wat a bit)
    sleep(15)
    print("smashed F11")
    os.system("sudo xdotool key F11")


# endregion


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

        # app.run(port=port, debug=False, threaded=True)


    except Exception as ex:
        print(ex)
        print("Interupted")

    finally:
        # clean gpio
        bartender.clean_gpio()

        # kill firefox
        os.system("pkill firefox")

        print("Cleaned GPIO")
