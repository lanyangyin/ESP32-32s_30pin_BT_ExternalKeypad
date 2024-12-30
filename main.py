import time
from machine import Pin, I2C, PWM
from BTkeyboard.Buzzer import Buzzer
from BTkeyboard.LED_ssd1306_screen import Run as oLED_run
from BTkeyboard.bluetooth import Device as BluetoothDevice
from BTkeyboard.bt_hid_output import bt_show
from BTkeyboard.keyboard import Key
from BTkeyboard.keys_config import KeyCode
from BTkeyboard.knob import Knob
from BTkeyboard.mode_key_set import mode_texts
from lib import ufont
from lib.hid_services import Keyboard
from lib.ssd1306 import SSD1306_I2C

# 指示灯
big_led = Pin(33, Pin.OUT)
big_led.value(0)

# 创建蓝牙对象
bt = BluetoothDevice("ESP32_Keyboard")
bt.active(False)
time.sleep(1)  # 等待蓝牙初始化
bt.active(True)
# 等待蓝牙连接
btgs = bt.keyboard.get_state()
while btgs is not Keyboard.DEVICE_CONNECTED:
    # 如果设备空闲，则开始广播或直到设备连接
    if btgs is Keyboard.DEVICE_IDLE:
        bt.keyboard.start_advertising()  # 开始广播
        bt.wait_for_confirmation(60)  # 等待广播或连接
        if btgs is Keyboard.DEVICE_ADVERTISING:  # 如果仍在广播
            bt.keyboard.stop_advertising()  # 则停止广播
    btgs = bt.keyboard.get_state()
time.sleep(5)  # 设备未连接时，使用较长的睡眠时间以节省电量


# 初始化ssd1306 oLED屏幕
i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=400000)
ssd = SSD1306_I2C(128, 64, i2c)
uFont = ufont.BMFont("fonts/unifont-14-12888-16.v3.bmf")
ssd_object = oLED_run(ssd=ssd, uFont=uFont)
# 初始化蜂鸣器
buzzer = Buzzer(PWM(Pin(32, Pin.OUT), freq=900, duty=0))
# 初始化旋钮
knobs = Knob()
knob_click = knobs.Click(io_pins={0: Pin(25, Pin.IN, Pin.PULL_DOWN), 1: Pin(26, Pin.IN, Pin.PULL_DOWN)})
L_io_pins = {0: Pin(14, Pin.IN, Pin.PULL_DOWN), 1: Pin(27, Pin.IN, Pin.PULL_DOWN)}
R_io_pins = {0: Pin(13, Pin.IN, Pin.PULL_DOWN), 1: Pin(12, Pin.IN, Pin.PULL_DOWN)}
key = Key([Pin(15, Pin.OUT), Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)],
          [Pin(5, Pin.IN, Pin.PULL_UP), Pin(18, Pin.IN, Pin.PULL_UP), Pin(19, Pin.IN, Pin.PULL_UP),
           Pin(23, Pin.IN, Pin.PULL_UP)])


# 全局变量
knob_rotate_left_status = 0
knob_rotate_right_status = 0
knob_rotate_status = (0, 0)
keycode = KeyCode()
# 操作系统
os_name_dict = {True: "Win", False: "MAC"}
os_name = True
anti_mis_contact_lock_button = False  # 防止误触锁定按钮，默认情况下不开启
mode_index = 0
mode_read_index = 0
display_once = True
# 双击、左右键按下时间记录
double_click_keep_time = 0
left_click_keep_time = 0
right_click_keep_time = 0
# 双键按下后抬起一个键，左右键预备时间记录
left_click_ready_time = 0
right_click_ready_time = 0
rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
clockwise = {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}
anticlockwise = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}


def display_mode():
    global mode_index
    if mode_index in mode_texts:
        text, icon = mode_texts[mode_index]["display"]
        ssd_object.ssd_unicode(string=text, x=0, y=32, font_size=32, half_char=True, show=True)
        ssd_object.ssd_type_matrix_text(icon, 64, 0, fill=True, show=True)


def display_os():
    """
    显示操作系统
    :return:
    """
    global os_name
    ssd_object.ssd_unicode(string=f"   ", x=32, y=11, font_size=8)
    ssd_object.ssd_normal_text(os_name_dict[os_name], 32, 11)
    ssd_object.ssd_normal_show()


def display_lock():
    """
    显示锁定按钮
    :return:
    """
    global anti_mis_contact_lock_button
    if anti_mis_contact_lock_button:
        ssd_object.ssd_type_matrix_text("关锁图标_32", 0, 0, fill=True, show=True)
    else:
        ssd_object.ssd_unicode(string=f" ", x=0, y=0, font_size=32, show=True)


display_mode()
display_os()
display_lock()


def key_show_clear():
    bt.keyboard.set_modifiers()
    bt.keyboard.set_keys()
    bt.keyboard.notify_hid_report()


# 监听旋钮事件
def get_knob_rotate():
    global rp, lp, rnt, lnt
    rnt = R_io_pins[0].value(), R_io_pins[1].value()
    lnt = L_io_pins[0].value(), L_io_pins[1].value()
    if rnt != rp[3]:
        rp[0] = rp[1]
        rp[1] = rp[2]
        rp[2] = rp[3]
        rp[3] = rnt
        if rp == clockwise:  # 顺时针
            rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            return 0, 1
        elif rp == anticlockwise:  # 逆时针
            rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            return 0, -1
    if lnt != lp[3]:
        lp[0] = lp[1]
        lp[1] = lp[2]
        lp[2] = lp[3]
        lp[3] = lnt
        if lp == clockwise:  # 顺时针
            lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            return 1, 0
        elif lp == anticlockwise:  # 逆时针
            lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            return -1, 0
    return 0, 0


class KnobClickIncident:
    global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
        right_click_ready_time, mode_index, mode_read_index

    def __init__(self):
        self.ready_time = 50  # 双键按下后抬起后，这时某键的仍然按下时间为预备时间，单位ms

    def knob_double_click_down_incident(self):
        global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
            right_click_ready_time, mode_index, mode_read_index, anti_mis_contact_lock_button
        if knob_click.status() == {'left': 1, 'right': 1}:
            left_click_keep_time = 0
            right_click_keep_time = 0
            left_click_ready_time = 0
            right_click_ready_time = 0
            double_click_keep_time += 1
            if double_click_keep_time == 1:
                print(f"双键按下")
            if double_click_keep_time == 800:
                print(f"双键按下超过{double_click_keep_time}毫秒")
                anti_mis_contact_lock_button = not anti_mis_contact_lock_button
                display_lock()
            time.sleep_ms(1)

    def knob_left_click_down_incident(self):
        global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
            right_click_ready_time, mode_index, mode_read_index
        if knob_click.status() == {'left': 1, 'right': 0}:
            # 防止双键按下抬起时左键的误触发，
            # 双键按下后抬起右键后，这时左键的按下时间为预备时间，
            # 预备时间时双键按下时间不会清空，依然视为双键按下
            # 超出预备时间才算真正开始按下左键
            if double_click_keep_time > 0:
                left_click_ready_time += 1
                if left_click_ready_time == 1:
                    print(f"双键按下后，左键准备")
                if left_click_ready_time == self.ready_time:  # 预备持续时间
                    print(f"左键预备结束")
                    double_click_keep_time = 0
                time.sleep_ms(1)
            if double_click_keep_time == 0:
                double_click_keep_time = 0
                right_click_keep_time = 0
                left_click_ready_time = 0
                right_click_ready_time = 0
                left_click_keep_time += 1
                if left_click_keep_time == 1:
                    print(f"左键按下")
                if left_click_keep_time == 1000:
                    print(f"左键按下超过{left_click_keep_time}秒")
                time.sleep_ms(1)

    def knob_right_click_down_incident(self):
        global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
            right_click_ready_time, mode_index, mode_read_index
        if knob_click.status() == {'left': 0, 'right': 1}:
            # 防止双键按下抬起时右键的误触发，
            # 双键按下后抬起左键后，这时右键的按下时间为预备时间，
            # 预备时间时双键按下时间不会清空，依然视为双键按下
            # 超出预备时间才算真正开始按下右键
            if double_click_keep_time > 0:
                right_click_ready_time += 1
                if right_click_ready_time == 1:
                    print(f"双键按下后，右键预备")
                if right_click_ready_time == self.ready_time:  # 预备持续时间
                    print(f"右键预备结束")
                    double_click_keep_time = 0
                time.sleep_ms(1)
            if double_click_keep_time == 0:
                double_click_keep_time = 0
                left_click_keep_time = 0
                right_click_keep_time += 1
                left_click_ready_time = 0
                right_click_ready_time = 0
                if right_click_keep_time == 1:
                    print(f"右键按下")
                if right_click_keep_time == 140:
                    print(f"右键按下超过{right_click_keep_time}毫秒")
                    bt_show(keycode.KC_F13, os_name, bt)
                time.sleep_ms(1)

    def knob_right_click_up_time(self):
        global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
            right_click_ready_time, mode_index, mode_read_index, display_once, os_name
        if knob_click.status() == {'left': 0, 'right': 0}:
            if double_click_keep_time:
                print(f"双键抬起,{double_click_keep_time}")
                if double_click_keep_time < 70:
                    os_name = not os_name
                    display_os()
            if left_click_keep_time:
                print(f"左键抬起,{left_click_keep_time}")
                if left_click_keep_time < 50:
                    mode_read_index -= 1
                    if mode_read_index < 0:
                        mode_index = mode_read_index = list(mode_texts)[-1]
                    else:
                        mode_index = mode_read_index
                    print(f"切换模式{mode_index}")
                    display_mode()
            if right_click_keep_time:
                print(f"右键抬起,{right_click_keep_time}")
                if right_click_keep_time < 50:
                    mode_read_index += 1
                    if mode_read_index > list(mode_texts)[-1]:
                        mode_index = mode_read_index = 0
                    else:
                        mode_index = mode_read_index
                    print(f"切换模式{mode_index}")
                    display_mode()
            double_click_keep_time = 0
            left_click_keep_time = 0
            right_click_keep_time = 0
            left_click_ready_time = 0
            right_click_ready_time = 0


def movement():
    KCI = KnobClickIncident()
    global double_click_keep_time, left_click_keep_time, right_click_keep_time, left_click_ready_time, \
        right_click_ready_time, mode_index, mode_read_index, display_once, lp, rp
    while True:
        knob_a_rotate = get_knob_rotate()
        if knob_a_rotate == (0, -1):
            print(knob_a_rotate)
            bt_show(keycode.KC_F16, os_name, bt)
        elif knob_a_rotate == (0, 1):
            print(knob_a_rotate)
            bt_show(keycode.KC_F17, os_name, bt)
        elif knob_a_rotate == (-1, 0):
            print(knob_a_rotate)
            bt_show(keycode.KC_F14, os_name, bt)
        elif knob_a_rotate == (1, 0):
            print(knob_a_rotate)
            bt_show(keycode.KC_F15, os_name, bt)

        KCI.knob_double_click_down_incident()
        KCI.knob_left_click_down_incident()
        KCI.knob_right_click_down_incident()
        KCI.knob_right_click_up_time()

        key_show = key.show()
        if not anti_mis_contact_lock_button:
            if key_show is not None:
                if mode_index < list(mode_texts)[-1]:
                    bt_show(mode_texts[mode_index]["key"][key_show[1]][key_show[0]], os_name, bt)
                    time.sleep_ms(140)
                if mode_index == list(mode_texts)[-1]:
                    buzzer.play(mode_texts[mode_index]["key"][key_show[1]][key_show[0]])
            else:
                buzzer.play(0)


big_led.value(1)
movement()
