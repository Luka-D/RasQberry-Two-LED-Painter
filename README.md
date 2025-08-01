# RasQberry-Two-LED-Painter

This is a program for the RasQberry Two Project, designed to paint an image to be displayed on the LED array.

The git repo for the RasQberry Two Project can be found [here](https://github.com/JanLahmann/RasQberry-Two).

## Installation

Install all the necessary dependencies using pip:

```pip install -r requirements.txt```

You will also need to install the `libxcb` library using the following command:

```sudo apt-get install libxcb-cursor-dev```

## How to Run

Run the script using:

```python3 LED_painter.py```

Additionally, you can also save your images to a JSON file by going to `File -> Save` in the toolbar. These images can be later displayed on the LED array by running the following command and pasting the path of the saved file into the console:

```python3 display_to_LEDs_from_file.py```

To turn off all of the LEDs, you can run this script:

```python3 turn_off_LEDs.py```

**! Note:** To run this script on a Raspberry Pi 5, you need to have SPI set up and use the proper wiring configuration. Instructions for wiring and setting up SPI can be found [here](https://rasqberry.org/3d-model/hardware-assembly-guide).


