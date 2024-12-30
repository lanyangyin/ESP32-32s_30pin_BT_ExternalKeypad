import _thread

import time
from machine import Pin, I2C, PWM
from BTkeyboard.Buzzer import Buzzer
from BTkeyboard.LED_ssd1306_screen import Run as oLED_run
from BTkeyboard.bluetooth import Device as BluetoothDevice
from BTkeyboard.keyboard import Key
from BTkeyboard.keys_config import KeyCode
from BTkeyboard.knob import Knob
from lib import ufont
from lib.hid_services import Keyboard
from lib.ssd1306 import SSD1306_I2C# 创建蓝牙对象
bt = BluetoothDevice("ESP32_Keyboard")



bt.active(True)