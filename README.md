MicroPython LCD Driver in Python
================================

This is Matt Trentini's fork of
[russhughes/st7789py_mpy](https://github.com/russhughes/st7789py_mpy),
originally based on [devbis/st7789py_mpy](https://github.com/devbis/st7789py_mpy).
The driver remains MIT licensed; upstream copyright notices are retained.

This driver has support for:

- 320x240, 240x240, 135x240, and 128x128 pixel and other displays
- RGB and BGR Color Orders
- Display rotation
- Hardware based scrolling
- Drawing text using converted PC BIOS bitmap fonts
- Drawing text using converted TrueType fonts.
- Drawing converted bitmaps

This is a work in progress. Documentation can be found in the docs directory
and at https://russhughes.github.io/st7789py_mpy/

KinCony CO16 installation
------------------------

On a network-connected MicroPython device:

```python
import mip
mip.install("github:mattytrentini/st7789py_mpy")
```

Alternatively, install from a computer connected to the board:

```sh
mpremote mip install github:mattytrentini/st7789py_mpy
```

The root `package.json` (version `1.0.0`) installs only `st7789py.py` and
`co16_tft_config.py`; it has no dependencies and does not install fonts, bitmap
assets or other board configurations. The source configuration is
`tft_configs/kincony_co16/tft_config.py`, following the upstream configuration
pattern, and is installed under the board-specific module name.

### Panel geometry and initialization

The [manufacturer's CO16 display example](https://www.kincony.com/forum/showthread.php?tid=9791)
identifies the GMT020-02-7P panel and specifies 320x240 landscape, SPI mode 0
at 20 MHz, BGR color order, MADCTL `0x68` (`MX | MV | BGR`), and inversion on.
`co16_tft_config.config()` uses native constructor dimensions **240x320** and
the existing **rotation 1** table entry: width 320, height 240, zero offsets,
MADCTL `0x60 | BGR = 0x68`, and no pixel byte swapping. No custom geometry
or rotation table is needed. These settings are checked against the published
source; actual display operation must still be verified on the board.

The upstream default initialization already contains the manufacturer's
display-function, RGB565 pixel-format, porch, gate, VCOM, power, frame-rate,
positive/negative gamma and inversion settings. No `custom_init` is required.
Upstream retains its own reset timing, initializes twice, sets rotation after
initialization, and clears the display before enabling the backlight; this is
not a byte-for-byte reproduction of the Arduino startup timing.

### Color-bar example (no font required)

```python
import co16_tft_config
import st7789py as st7789

tft = co16_tft_config.config()  # rotation=1, baudrate=20000000
colors = (
    st7789.RED, st7789.GREEN, st7789.BLUE,
    st7789.CYAN, st7789.MAGENTA, st7789.YELLOW,
)
for index, color in enumerate(colors):
    x0 = index * tft.width // len(colors)
    x1 = (index + 1) * tft.width // len(colors)
    tft.fill_rect(x0, 0, x1 - x0, tft.height, color)
tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
tft.cs.on()  # explicit shared-bus handoff
```

`config(rotation=1, baudrate=20000000)` returns a normal `ST7789` instance.
Rotations 0/2 produce 240x320 portrait; 1/3 produce 320x240 landscape.
The SPI and constructor configuration is:

| Signal | CO16 configuration |
| --- | --- |
| SPI | `SPI(2, baudrate=20000000, polarity=0, phase=0)` |
| SCK / MOSI / MISO | GPIO11 / GPIO10 / GPIO12 |
| LCD CS / DC | GPIO4 / GPIO0 |
| LCD RESET / backlight | GPIO5 / GPIO40 |
| Unused SD / MAX / LoRa CS | GPIO9 / GPIO14 / GPIO13, driven high before construction |
| Driver | `ST7789(spi, 240, 320, rotation=1, color_order=st7789.BGR, ...)` |

### Shared-bus and LoRa limits

- The configuration owns/reinitializes SPI2 and leaves LCD CS high after
  construction. Call it once; it is not a shared-bus arbitration layer.
- The SD, MAX and optional LoRa peripherals share GPIO11/10/12. Their CS
  lines are deselected during display setup. Serialize all access, keep other
  CS lines high during LCD transfers, and restore mode 0/20 MHz before LCD
  use if another SPI client changes those settings.
- Do **not** use `machine.SDCard` concurrently on this SPI host; hardware-host
  ownership is not made safe merely by deselecting the SD chip. SPI1 Ethernet
  is separate and is not reconfigured by this module.
- GPIO5 (LCD reset) and GPIO40 (LCD backlight) share optional LoRa signals.
  LCD reset/backlight use is not compatible with independent simultaneous
  LoRa operation on those pins.
- Upstream's command-only `soft_reset()`, `sleep_mode()` and
  `inversion_mode()` can leave LCD CS low. Before another SPI device uses the
  bus, explicitly call `tft.cs.on()` after these operations (and after a
  failed transfer). Normal completed drawing operations finish with a data
  write and release CS. This fork does not change the generic driver's
  transaction behavior.


Examples
--------

See the examples directory for example programs that run on:

- ESP32
  - Generic ESP32 320x240
  - KinCony CO16 GMT020-02-7P 320x240
  - LilyGo T-DISPLAY 135x240
  - LilyGo T-Dongle-S3 80x160 (ST7735)
  - LilyGo T-embed 170x320
  - LILYGO T-QT Pro 128x128 (GC9107)
  - M5STACK AtomS3 128x128 (GC9107)
  - M5STACK CORE2 320x240 (ILI9342)
  - M5STACK CORE 320x240 (ILI9342)
  - M5STACK CoreS3 320x240 (ILI9342)

- RP2040
  - LilyGo T-DISPLAY RP2040 135x240
  - RP2040-Touch-LCD-1.28 240x240 (GC9A01)
  - Waveshare Pico LCD 1.14 135x240
  - Waveshare Pico LCD 1.3 240x240
  - Waveshare Pico LCD 2 240x320
