from color_setup import ssd, i2c  # Create a display instance
from gui.core.colors import *
from gui.core.writer import Writer
from gui.core.nanogui import refresh
from gui.widgets.label import Label
from gui.widgets.textbox import Textbox
from gui.widgets.meter import Meter

import time
import machine
import builtins
import uasyncio
from machine import SoftI2C
import adafruit_sgp30

import gui.fonts.freesans20 as freesans20
import gui.fonts.arial10 as arial10
import arial28 as arial28

def bootscreen():
    global largeWriter, smallWriter
    tbLogo = Textbox(largeWriter, 2, 0, 95, 1, bdcolor=BLACK)
    tbLogo.append('itenium')
    refresh(ssd)
    meter = Meter(smallWriter, 2, 110, height=28, width=10, divisions=0, style=Meter.BAR)
    for i in range(15):
        meter.value(i/15)
        refresh(ssd)
        time.sleep(1)
    refresh(ssd, True)  # clear display.
    
async def measure():
    global smallWriter
    tbCO2 = Textbox(smallWriter, 8, 1, 110, 1, bdcolor=BLACK)
    tbTVOC = Textbox(smallWriter, 20, 1, 110, 1, bdcolor=BLACK)
    while True:
        co2eq, tvoc = sgp30.iaq_measure()
        tbCO2.append(f'CO2: %d ppm' % co2eq)
        tbTVOC.append(f'TVOC: %d ppm' % tvoc)
        refresh(ssd)
        await uasyncio.sleep(5)

# Setup SGP30 CO2 sensor on same I2C port as display
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

## Setup display
refresh(ssd, True)  # clear display.
Writer.set_textpos(ssd, 0, 0)
smallWriter = Writer(ssd, arial10, verbose=False)
smallWriter.set_clip(True, True, False)
largeWriter = Writer(ssd, arial28, verbose=False)
largeWriter.set_clip(True, True, False)

# Show the boot screen
bootscreen()

# Start the main loop
event_loop = uasyncio.get_event_loop()
event_loop.create_task(measure())
event_loop.run_forever()
