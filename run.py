import os
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from flask import redirect
from flask import session
from hardware.bartender import Bartender
from hardware.drinks import *  # this provides the drink list mentioned
from time import sleep
from threading import Thread
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'D7ZrQQ0/p7n R~Xhh!jmN]APX/,?CR'

# region Webpages
# index (same as cocktail overvieuw)
@app.route('/')
def index():
    try:
        return redirect("/drinks", 300)
    except Exception as ex:
        print(ex)
        abort(400)


# detail cocktail
@app.route('/drinks')
def drinks():
    try:
        if bartender.alcohol_enabled:
            return render_template("drinks.html", drink_list=drink_list)
        else:
            # listcomprehension for filtering
            filtered_drink_list = [drink for drink in drink_list if drink["alcoholic"] == False]
            return render_template("drinks.html", drink_list=filtered_drink_list)
    except Exception as ex:
        print(ex)
        abort(400)


# path for one drink
@app.route("/drink", methods=["GET"])
def drink():
    try:
        # request if cocktail was given
        drink_name = request.args.get("drink")

        # if coctail does not exist throw 404
        try:
            drink = get_drink_from_base64name(drink_name)
            return render_template("drink.html", drink=drink, web_orders=bartender.weborders)
        except Exception as ex:
            print(ex)
            abort(404)
    except:
        abort(400)


@app.route("/drink", methods=["POST"])
def drink_post():

    try:
        if bartender.weborders == True:
            # request if cocktail was given
            drink_name = request.args.get("drink")

            # if coctail does not exist throw 404
            try:
                drink = get_drink_from_base64name(drink_name)

                # check if alcoholic and allowed
                if drink["alcoholic"] == True and bartender.alcohol_enabled == False:
                    # forbidden
                    abort(403)
                else:
                    # make the drink
                    bartender.makeDrink(drink["name"], drink["ingredients"])
                    return render_template("done.html", drink=drink)

            except Exception as ex:
                # not found
                abort(404)
        else:
            # forbidden
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
        abort(400)

@app.route("/cancel")
def cancel():
    try:
        drink_name =  request.args.get("drink")
        drink = get_drink_from_base64name(drink_name)

        return render_template("cancel.html", drink = drink)

    except Exception as ex:
        abort(400)

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
        abort(400)


# admin (alcohol, toggle, ...)
@app.route('/admin', methods=['GET'])
def admin(error = ""):
    try:
        if 'username' in session:
            return redirect("/settings", 300)
        else:
            return render_template("admin.html", error=error)
    except:
        abort(400)


@app.route('/admin', methods=['POST'])
def admin_post():

    try:
        password = request.form.get('password')
        username = request.form.get('username')

        print(password)

        if check_password_hash("pbkdf2:sha256:1000$2Hfx3SqO$db68641165e5d1090ba1cc5cb2d8c2a28726b4ffabd6ed8d38b044b37feb2f10", password) == True or check_password_hash("pbkdf2:sha256:1000$OjDNDdaJ$59c70018fdaf1b0c353f4a8ab83294fb579297ea2ea43b9e3a03cff99fd2d99a", password):
            session['username'] = username
            return redirect('/settings')
        else:
            return render_template("admin.html", error="Wrong password or username")

    except Exception as ex:
        print(ex)
        abort(400)



# settings (alcohol, toggle, ...)
@app.route('/settings', methods=['GET'])
def settings():
    try:
        if 'username' in session:
        # if True:
            return render_template("settings.html", pump_config= bartender.pump_configuration, drink_options=get_option_names())
        else:
            #unautorised
            abort(401)
    except:
        abort(400)


@app.route('/settings', methods=['POST'])
def settings_post():
    try:
        if 'username' in session:
        # if True:
            form_type = (request.form['type'])

            if form_type == "clean":
                bartender.clean()

            elif form_type == "shutdown":
                bartender.shutdown()

            elif form_type == "enable_weborders":
                # boolean flip
                bartender.weborders = bartender.weborders ^ 1

            elif form_type == "enable_alcohol":
                # boolean flip
                bartender.alcohol_enabled = bartender.alcohol_enabled ^ 1

            elif form_type == "logoff":
                # clear the session
                session.clear()
                return redirect("/admin", 303)

            return redirect("/settings", code=303)

        else:
            #unauthorised
            abort(401)


    except:
        #bad request
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

        # drinks.filter_not_possible()

        # pas parms and set debug
        app.run(host=host, port=port, debug=False, threaded=True)

        # app.run(port=port, debug=False, threaded=True)


    # except Exception as ex:
    except Exception as ex:
        print(ex)
        print("Interupted")

    finally:
        # clean gpio
        bartender.clean_gpio()

        # kill firefox
        os.system("sudo pkill firefox")

        print("Cleaned GPIO, killed Firefox")
