import machine
from drivers.ssd1306.ssd1306 import SSD1306_I2C
from drivers.ssd1306.ssd1306 import SSD1306 as SSD

WIDTH = const(128)
HEIGHT = const(32)
pscl = machine.Pin(9, machine.Pin.OPEN_DRAIN)
psda = machine.Pin(8, machine.Pin.OPEN_DRAIN)
i2c = machine.SoftI2C(scl=pscl, sda=psda)

ssd = SSD1306_I2C(WIDTH, HEIGHT, i2c)