"""KinCony CO16 GMT020-02-7P ST7789 display (320x240 landscape).

Manufacturer configuration:
https://www.kincony.com/forum/showthread.php?tid=9791

Installed by mip as co16_tft_config.py. SPI2 is shared with the SD, MAX
and optional LoRa peripherals; GPIO5 and GPIO40 also share LoRa signals.
"""

# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Matt Trentini

from machine import Pin, SPI
import st7789py as st7789

TFA = 0
BFA = 0
WIDE = 1
TALL = 0
SCROLL = 0  # orientation for scroll.py
FEATHERS = 1  # orientation for feathers.py


def config(rotation=WIDE, baudrate=20000000):
    """Return the CO16 display, defaulting to 320x240 landscape at 20 MHz.

    rotation uses the driver's existing native 240x320 rotation table.
    The manufacturer uses rotation 1 with BGR (MADCTL 0x68), inversion
    on, and SPI mode 0. The driver's default initialization already
    supplies the manufacturer's porch, power and gamma register values.

    Do not use machine.SDCard on this SPI host concurrently. Serialize
    shared-SPI transfers, deselect the LCD before handing off the bus,
    and do not use the optional LoRa module's shared reset/backlight pins.
    """
    for number in (9, 14, 13):
        Pin(number, Pin.OUT, value=1)  # SD, MAX and LoRa chip selects

    cs = Pin(4, Pin.OUT, value=1)
    backlight = Pin(40, Pin.OUT, value=0)
    spi = SPI(
        2,
        baudrate=baudrate,
        polarity=0,
        phase=0,
        sck=Pin(11),
        mosi=Pin(10),
        miso=Pin(12),
    )
    tft = st7789.ST7789(
        spi,
        240,
        320,
        reset=Pin(5, Pin.OUT, value=1),
        cs=cs,
        dc=Pin(0, Pin.OUT, value=1),
        backlight=backlight,
        rotation=rotation,
        color_order=st7789.BGR,
    )
    cs.on()
    return tft
