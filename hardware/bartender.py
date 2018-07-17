import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import sys
import RPi.GPIO as GPIO
import json
import threading
import traceback
import os
import base64

from time import sleep
from dotstar import Adafruit_DotStar
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options

# var to change the size of the screen
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# pin for menu + pin (and bounce time)
MENU_PLUS_BTN_PIN = 26
MENU_PLUS_BTN_BOUNCE = 1000

# pin for menu - pin (and bounce time)
MENU_MIN_BTN_PIN = 19
MENU_MIN_BTN_BOUNCE = 1000

# pin for selct pin (and bounce time)
SELECT_BTN_PIN = 13
SELECT_PIN_BOUNCE = 2000

# set pin for alcohol button
ALCOHOL_BTN_PIN = 5
ALCOHOL_PIN_BOUNCE = 2000

# set pin for alcohol button
ADMIN_BTN_PIN = 6
ADMIN_PIN_BOUNCE = 2000

# for display
OLED_RESET_PIN = 14
OLED_DC_PIN = 15

# neopixel pins and vars
NUMBER_NEOPIXELS = 45
NEOPIXEL_DATA_PIN = 22
NEOPIXEL_CLOCK_PIN = 27
NEOPIXEL_BRIGHTNESS = 64

# number, liquid the pump can "move", tweek if amount is incorrect
FLOW_RATE = 60.0 / 100.0

# vars from the web site
server_host =  "169.254.55.5"
#server_host =  "127.0.0.1"
server_port =  "8080"
root_path = "/"


class Bartender(MenuDelegate):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.running = False

        # set the oled screen height
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.btnMenuPlusPin = MENU_PLUS_BTN_PIN
        self.btnMenuMinPin = MENU_MIN_BTN_PIN
        self.btnSelectPin = SELECT_BTN_PIN
        self.btnAdminPin = ADMIN_BTN_PIN
        self.btnAlcoholPin = ALCOHOL_BTN_PIN

        # vars for toggle
        self.alcohol_enabled = False
        self.admin_enabled = False

        self.weborders = False

        # configure interrups for buttons
        GPIO.setup(self.btnMenuPlusPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnMenuMinPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnSelectPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnAdminPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnAlcoholPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


        # configure screen
        spi_bus = 0
        spi_device = 0
        gpio = gaugette.gpio.GPIO()
        spi = gaugette.spi.SPI(spi_bus, spi_device)

        # Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
        self.led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=OLED_RESET_PIN, dc_pin=OLED_DC_PIN,
                                            rows=self.screen_height,
                                            cols=self.screen_width)  # Change rows & cols values depending on your display dimensions.
        self.led.begin()
        self.led.clear_display()
        self.led.display()
        self.led.invert_display()
        time.sleep(0.5)
        self.led.normal_display()
        time.sleep(0.5)

        # load the pump configuration from file
        self.pump_configuration = Bartender.readPumpConfiguration()
        for pump in self.pump_configuration.keys():
            GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)

        # setup pixels:
        self.numpixels = NUMBER_NEOPIXELS  # Number of LEDs in strip

        # Here's how to control the strip from any two GPIO pins:
        datapin = NEOPIXEL_DATA_PIN
        clockpin = NEOPIXEL_CLOCK_PIN
        self.strip = Adafruit_DotStar(self.numpixels, datapin, clockpin)
        self.strip.begin()  # Initialize pins for output
        self.strip.setBrightness(NEOPIXEL_BRIGHTNESS)  # Limit brightness to ~1/4 duty cycle

        # turn everything off
        for i in range(0, self.numpixels):
            self.strip.setPixelColor(i, 0)
        self.strip.show()

        # add var so the system can go back
        self.lastpagecommand = ""

        print("Done initializing")

    @staticmethod
    def readPumpConfiguration():
        return json.load(open('hardware/pump_config.json'))

    @staticmethod
    def writePumpConfiguration(configuration):
        with open("hardware/pump_config.json", "w") as jsonFile:
            json.dump(configuration, jsonFile)

    def startInterrupts(self):
        GPIO.add_event_detect(self.btnMenuPlusPin, GPIO.FALLING, callback=self.menu_plus_btn, bouncetime=MENU_PLUS_BTN_BOUNCE)
        GPIO.add_event_detect(self.btnMenuMinPin, GPIO.FALLING, callback=self.menu_min_btn, bouncetime=MENU_MIN_BTN_BOUNCE)
        GPIO.add_event_detect(self.btnSelectPin, GPIO.FALLING, callback=self.select_btn, bouncetime=SELECT_PIN_BOUNCE)

        GPIO.add_event_detect(self.btnAlcoholPin, GPIO.FALLING, callback=self.alcohol_btn,bouncetime=ALCOHOL_PIN_BOUNCE)
        GPIO.add_event_detect(self.btnAdminPin, GPIO.FALLING, callback=self.admin_btn,bouncetime=ADMIN_PIN_BOUNCE)

    def stopInterrupts(self):
        GPIO.remove_event_detect(self.btnAlcoholPin)
        GPIO.remove_event_detect(self.btnAdminPin)
        GPIO.remove_event_detect(self.btnSelectPin)
        GPIO.remove_event_detect(self.btnMenuMinPin)
        GPIO.remove_event_detect(self.btnMenuPlusPin)

    def buildMenu(self, drink_list, drink_options, alcoholic_drinks_enabled=False, admin_options_enabled=False):
        # create a new main menu
        m = Menu("Main Menu")

        # add drink options
        drink_opts = []
        for d in drink_list:
            # check if allowed by admin button
            if alcoholic_drinks_enabled == False:
                # check if the drink has alcohol
                if d["alcoholic"] == False:  # -----!!!!-----
                    drink_opts.append(MenuItem('drink', d["name"], {"ingredients": d["ingredients"]}))  # -----!!!!-----
            else:
                drink_opts.append(MenuItem('drink', d["name"], {"ingredients": d["ingredients"]}))

        configuration_menu = Menu("Configure")

        # add pump configuration options
        pump_opts = []
        for p in sorted(self.pump_configuration.keys()):
            config = Menu(self.pump_configuration[p]["name"])
            # add fluid options for each pump
            for opt in drink_options:
                # star the selected option
                selected = "*" if opt["value"] == self.pump_configuration[p]["value"] else ""
                config.addOption(
                    MenuItem('pump_selection', opt["name"], {"key": p, "value": opt["value"], "name": opt["name"]}))
            # add a back button so the user can return without modifying
            config.addOption(Back("Back"))
            config.setParent(configuration_menu)
            pump_opts.append(config)

        # add pump menus to the configuration menu
        configuration_menu.addOptions(pump_opts)
        # add a back button to the configuration menu
        configuration_menu.addOption(Back("Back"))
        # adds an option that cleans all pumps to the configuration menu
        configuration_menu.addOption(MenuItem('clean', 'Clean'))
        # adds the option to power off
        configuration_menu.addOption(MenuItem('poweroff', 'Power off'))
        configuration_menu.setParent(m)

        # add drinks to options
        m.addOptions(drink_opts)

        # check if admin is enabled
        if admin_options_enabled == True:
            m.addOption(configuration_menu)

        # create a menu context
        self.menuContext = MenuContext(m, self)

    def filterDrinks(self, menu):
        """
        Removes any drinks that can't be handled by the pump configuration
        """
        for i in menu.options:
            if (i.type == "drink"):
                i.visible = False
                ingredients = i.attributes["ingredients"]
                presentIng = 0
                for ing in ingredients.keys():
                    for p in self.pump_configuration.keys():
                        if (ing == self.pump_configuration[p]["value"]):
                            presentIng += 1
                if (presentIng == len(ingredients.keys())):
                    i.visible = True
            elif (i.type == "menu"):
                self.filterDrinks(i)

    def selectConfigurations(self, menu):
        """
        Adds a selection star to the pump configuration option
        """
        for i in menu.options:
            if (i.type == "pump_selection"):
                key = i.attributes["key"]
                if (self.pump_configuration[key]["value"] == i.attributes["value"]):
                    i.name = "%s %s" % (i.attributes["name"], "*")
                else:
                    i.name = i.attributes["name"]
            elif (i.type == "menu"):
                self.selectConfigurations(i)

    def prepareForRender(self, menu):
        self.filterDrinks(menu)
        self.selectConfigurations(menu)
        return True

    def menuItemClicked(self, menuItem):
        if (menuItem.type == "drink"):
            self.makeDrink(menuItem.name, menuItem.attributes["ingredients"]) ###################################"
            return True
        elif (menuItem.type == "pump_selection"):
            self.pump_configuration[menuItem.attributes["key"]]["value"] = menuItem.attributes["value"]
            Bartender.writePumpConfiguration(self.pump_configuration)
            return True
        elif (menuItem.type == "clean"):
            self.clean()
            return True
        elif (menuItem.type == "poweroff"):
            self.shutdown()
            return True

        return False

    def clean(self):
        waitTime = 20
        pumpThreads = []

        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        self.running = True

        for pump in self.pump_configuration.keys():
            pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
            pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        self.progressBar(waitTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        self.menuContext.showMenu()

        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)  # ;

        # reenable interrupts
        # self.startInterrupts()
        self.running = False

    def shutdown(self):
        print("system will go off")
        os.system("sudo shutdown now")

    def displayMenuItem(self, menuItem):
        print menuItem.name
        self.led.clear_display()
        self.led.draw_text2(0, 20, menuItem.name, 2)
        self.led.display()

        print("set on oled")
        print(menuItem.type)
        print(menuItem.name)

        self.displayInBrowser(menuItem)

    def displayInBrowser(self, menuItem):
        # check the type and open the matching page
        if (menuItem.type == "drink"):
            path = "/drink?drink={0}".format(base64.encodestring(menuItem.name))
            self.create_exectute_display_command(path)

        else:
            path = "/basic-menu?item={0}&type={1}".format(base64.encodestring(menuItem.name), base64.encodestring(menuItem.type))
            self.create_exectute_display_command(path)


    def create_exectute_display_command(self, webpath):
        # makes the command with the given parms
        command = "DISPLAY=:0 firefox '{0}:{1}{2}' &".format(server_host,server_port,webpath)
        # execute
        os.system(command)

    def cycleLights(self):
        t = threading.currentThread()
        head = 0  # Index of first 'on' pixel
        tail = -10  # Index of last 'off' pixel
        color = 0xFF0000  # 'On' color (starts red)

        while getattr(t, "do_run", True):
            self.strip.setPixelColor(head, color)  # Turn on 'head' pixel
            self.strip.setPixelColor(tail, 0)  # Turn off 'tail'
            self.strip.show()  # Refresh strip
            time.sleep(1.0 / 50)  # Pause 20 milliseconds (~50 fps)

            head += 1  # Advance head position
            if (head >= self.numpixels):  # Off end of strip?
                head = 0  # Reset to start
                color >>= 8  # Red->green->blue->black
                if (color == 0): color = 0xFF0000  # If black, reset to red

            tail += 1  # Advance tail position
            if (tail >= self.numpixels): tail = 0  # Off end? Reset

    def lightsEndingSequence(self):
        # make lights green
        for i in range(0, self.numpixels):
            self.strip.setPixelColor(i, 0xFF0000)
        self.strip.show()

        time.sleep(5)

        # turn lights off
        for i in range(0, self.numpixels):
            self.strip.setPixelColor(i, 0)
        self.strip.show()

    def pour(self, pin, waitTime):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)

    def progressBar(self, waitTime):
        interval = waitTime / 100.0
        for x in range(1, 101):
            self.led.clear_display()
            self.updateProgressBar(x, y=35)
            self.led.display()
            time.sleep(interval)

    def makeDrink(self, drink, ingredients):
        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        self.running = True

        # show a page so the user knows it's buzzy
        self.create_exectute_display_command("/making?drink={0}".format(base64.encodestring(drink)))

        # launch a thread to control lighting
        lightsThread = threading.Thread(target=self.cycleLights)
        lightsThread.start()

        # Parse the drink ingredients and spawn threads for pumps
        maxTime = 0
        pumpThreads = []
        for ing in ingredients.keys():
            for pump in self.pump_configuration.keys():
                if ing == self.pump_configuration[pump]["value"]:
                    waitTime = ingredients[ing] * FLOW_RATE
                    if (waitTime > maxTime):
                        maxTime = waitTime
                    pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
                    pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        self.progressBar(maxTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        self.menuContext.showMenu()

        # stop the light thread
        lightsThread.do_run = False
        lightsThread.join()

        # show the ending sequence lights
        self.lightsEndingSequence()

        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)  # ;

        # reenable interrupts
        # self.startInterrupts()
        self.running = False

    def menu_plus_btn(self, ctx):
        print("plus hit")

        if not self.running:
            self.menuContext.advance()

    def menu_min_btn(self, ctx):
        print("min hit")

        if not self.running:
            self.menuContext.previous()

    def select_btn(self, ctx):

        if not self.running:
            print("cocktail selected")
            self.menuContext.select()
        else:
            print ("cocktail already being made")

    def alcohol_btn(self, ctx):
        print("alcohol hit")

        # rebuild the menu
        self.alcohol_enabled= self.alcohol_enabled ^ 1
        self.buildMenu(drink_list, drink_options, self.alcohol_enabled, self.admin_enabled)  # -----!!!!-----

    def admin_btn(self, ctx):
        print("admin hit")

        # rebuild the menu
        self.admin_enabled= self.admin_enabled ^ 1
        self.buildMenu(drink_list, drink_options, self.alcohol_enabled, self.admin_enabled)  # -----!!!!-----

    def updateProgressBar(self, percent, x=15, y=15):
        height = 10
        width = self.screen_width - 2 * x
        for w in range(0, width):
            self.led.draw_pixel(w + x, y)
            self.led.draw_pixel(w + x, y + height)
        for h in range(0, height):
            self.led.draw_pixel(x, h + y)
            self.led.draw_pixel(self.screen_width - x, h + y)
            for p in range(0, percent):
                p_loc = int(p / 100.0 * width)
                self.led.draw_pixel(x + p_loc, h + y)

    def run(self):
        self.startInterrupts()

    def start_operation(self):
        self.buildMenu(drink_list, drink_options)
        self.run()


    @staticmethod
    def set_gpio():
        GPIO.setmode(GPIO.BCM)

    def clean_gpio(self):
        self.stopInterrupts()
        GPIO.cleanup()


