2026-10-05 — 1.0.0
-----------------

  - Synchronized this fork with russhughes upstream master (`7265925`).
  - Added the KinCony CO16 GMT020-02-7P configuration using the existing
    native 240x320 rotation table, rotation 1, BGR, and SPI2 mode 0 at 20 MHz.
  - Deselect SD, MAX and LoRa chip selects before display construction and
    explicitly release LCD chip select after construction.
  - Added a minimal mip manifest installing the driver and `co16_tft_config`
    from this fork without fonts, assets or dependencies.
  - Documented manufacturer initialization/geometry, a font-free color-bar
    example, and SPI-host, command-only chip-select and shared-LoRa-pin limits.

2023-11-29
----------

  - Changed examples to use the same source code, with different
    `tft_config.py` and `tft_buttons.py` modules. This is to make it easier to support additional devices and configurations.
  - Added `tft_buttons.py` modules to support the buttons.
  - Added `tft_config.py` modules to support different configurations.
  - Added examples to demonstrate and test new features.
  - Changed `text()` method to user micropython.viper to improve performance.
  - Added `polygon()` method to draw polygons with optional rotation. This is not fast, but it works.
  - Added `make-example.py` script to generate documentation for examples, configs and utilities.
  - Added documentation for examples, configs and utilities extracted from docstrings using `make-example.py`.
  - Added color_order parameter to st7789py to allow different color orders.
  - Added custom_init parameter to st7789py to allow custom initialization of the display.
  - Added custom_rotation parameter to st7789py to allow custom display sizes, rotations and byte swapping for color data.
  - Added `pbitmap` method to support drawing bitmap graphics one line at a time.
  - Added `examples/upload_all.sh` script to upload all examples to the board.
  - Added `run_all.sh` script to run all examples on the board.
  - Updated and improved documentation.
