import os
import threading
from flask import Flask
from flask import render_template
from flask import request
from hardware.bartender import Bartender
from hardware.drinks import drink_list
from threading import Thread
from RPi import GPIO

app = Flask(__name__)


# index
@app.route('/')
def index():
    return render_template("index.html", cocktail_list=drink_list)


# detail cocktail
@app.route('/drinks')
def detail():
    cocktail = request.args.get("cocktail")

    return render_template("admin.html")


# admin (cleaning, managing, ...)
@app.route('/admin')
def admin():
    return render_template("admin.html")


def start_hardware():
    # can be romeved afterwards (script seems to be unable to restart otherwise)
    Bartender.set_gpio()
    bartender = Bartender()
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

    except Exception as ex:
        print(ex)
        print("Interupted")

    finally:
        Bartender.clean_gpio()
        print("Cleaned GPIO")
