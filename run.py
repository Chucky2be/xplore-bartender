import os
import threading
from flask import Flask
from flask import render_template
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
@app.route('/detail?cocktail')
def detail():
    return render_template("admin.html")

#admin (cleaning, managing, ...)
@app.route('/admin')
def admin():
    print ("route found")
    return render_template("admin.html")


def start_hardware():
    # #set to bcm
    # GPIO.setmode(GPIO.BCM)
    # # create obj
    # bartender = Bartender()
    # #starts the machine as a threat
    # th = Thread(target=bartender.start_operation)
    # th.start()
    bartender = Bartender()
    bartender.start_operation()


if __name__ == '__main__':
    try:
        # set port 8080
        port = int(os.environ.get("PORT", 8080))
        # set ip
        host = "169.254.55.5"
        # pas parms and set debug
        app.run(host=host, port=port, debug=True)
        # turn on hw code
        start_hardware()
    except Exception as ex:
        print(ex)
    finally:
        GPIO.cleanup()
