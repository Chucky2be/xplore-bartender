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

#index
@app.route('/')
def index():
    cocktail_list = drink_list
    return render_template("index.html", cocktail_list=cocktail_list)

#detail cocktail
@app.route('/detail')
def detail():
    cocktail = request.args.get("cocktail")
    print (cocktail)
    return render_template("admin.html")

#admin (cleaning, managing, ...)
@app.route('/admin')
def admin():
    return render_template("admin.html")


def start_hardware():
    Bartender.set_gpio()
    bartender = Bartender()
    thread = Thread(target=bartender.start_operation)
    thread.start()

if __name__ == '__main__':
    try:
        try:
            # turn on hw
            start_hardware()
            # set port 8080
            port = int(os.environ.get("PORT", 8080))
            # set ip
            host = "169.254.55.5"
            # pas parms and set debug
            # app.run(host=host, port=port, debug=True)
            app.run(host=host, port=port, debug=False)
            # turn on hw code

        except Exception as ex:
            print(ex)
        finally:
            print("end of code")
            GPIO.cleanup()
    except KeyboardInterrupt:
        print("Interupted")
