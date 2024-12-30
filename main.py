import time
from machine import Pin, I2C, PWM

from BTkeyboard.Buzzer import Buzzer
from BTkeyboard.LED_ssd1306_screen import Run as oLED_run
from BTkeyboard.bluetooth import Device as BluetoothDevice
from BTkeyboard.keyboard import Key
from BTkeyboard.keys_config import KeyCode
from BTkeyboard.knob import Knob
import ufont
from hid_services import Keyboard
from ssd1306 import SSD1306_I2C

# 指示灯
big_led = Pin(33, Pin.OUT)
big_led.value(0)

# 全局变量
knob_rotate_left_status = 0
knob_rotate_right_status = 0
knob_rotate_status = (0, 0)
keycode = KeyCode()
# 操作系统
# 读取BTkeyboard/config.json文件，获取"设备系统"参数
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
mode_texts = {
    0: {"display": ("原始", "按钮图标_64"),
        "key": [[keycode.KC_BSPACE, keycode.KC_KP_SLASH, keycode.KC_KP_ASTERISK, keycode.KC_KP_MINUS],
                [keycode.KC_KP_7, keycode.KC_KP_8, keycode.KC_KP_9, keycode.KC_KP_PLUS],
                [keycode.KC_KP_4, keycode.KC_KP_5, keycode.KC_KP_6, keycode.KC_KP_ENTER],
                [keycode.KC_KP_1, keycode.KC_KP_2, keycode.KC_KP_3, keycode.KC_KP_DOT],
                [0x00, 0x00, 0x00, keycode.KC_KP_0]]},
    1: {"display": ("代码", "按钮图标_64"),
        "key": [["替换", "注释", "进格", "退格"],
                ["查找", "优化代码", "优化import", "恢复"],
                ["全选", "跳转助记标签", "连接行", "撤回"],
                ["复制", "粘贴", "剪切", "另存为"],
                [0x00, 0x00, 0x00, "保存"]]},
    2: {"display": ("常规", "按钮图标_64"),
        "key": [["创建文件夹", "删除文件", "切换上一个桌面", "切换下一个桌面"],
                ["返回桌面", "最小化", "展示窗口", "恢复"],
                ["全选", "替换", "打印", "撤回"],
                ["复制", "粘贴", "剪切", "另存为"],
                [0x00, 0x00, 0x00, "保存"]]},
    3: {"display": ("P S", "按钮图标_64"),
        "key": [[0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00]]},
    4: {"display": ("OBS", "按钮图标_64"),
        "key": [[0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00]]},
    5: {"display": ("L2D", "按钮图标_64"),
        "key": [[0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00],
                [0x00, 0x00, 0x00, 0x00]]},
    6: {"display": ("音C", "音乐图标_64"),
        "key": [[1, 2, 3, 4],
                [5, 6, 7, 0],
                [11, 12, 13, 0],
                [14, 15, 16, 17],
                [0, 0, 0, 0]]}
}

# 初始化ssd1306 oLED屏幕
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
ssd = SSD1306_I2C(128, 64, i2c)
uFont = ufont.BMFont("unifont-14-12888-16.v3.bmf")
ssd_object = oLED_run(ssd=ssd, uFont=uFont)
# 初始化蜂鸣器
buzzer = Buzzer(PWM(Pin(32, Pin.OUT), freq=900, duty=0))
# 创建蓝牙对象
bt = BluetoothDevice("ESP32_Keyboard")
# 初始化旋钮
knobs = Knob()
knob_click = knobs.Click(io_pins={0: Pin(25, Pin.IN, Pin.PULL_DOWN), 1: Pin(26, Pin.IN, Pin.PULL_DOWN)})
L_io_pins = {0: Pin(14, Pin.IN, Pin.PULL_DOWN), 1: Pin(27, Pin.IN, Pin.PULL_DOWN)}
R_io_pins = {0: Pin(13, Pin.IN, Pin.PULL_DOWN), 1: Pin(12, Pin.IN, Pin.PULL_DOWN)}
key = Key([Pin(15, Pin.OUT), Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)],
          [Pin(5, Pin.IN, Pin.PULL_UP), Pin(18, Pin.IN, Pin.PULL_UP), Pin(19, Pin.IN, Pin.PULL_UP),
           Pin(23, Pin.IN, Pin.PULL_UP)])


def display_mode():
    global mode_index
    if mode_index in mode_texts:
        text, icon = mode_texts[mode_index]["display"]
        ssd_object.ssd_unicode(string=text, x=0, y=32, font_size=32, half_char=True, show=True)
        ssd_object.ssd_type_matrix_text(icon, 64, 0, fill=True, show=True)


display_mode()


def display_os():
    """
    显示操作系统
    :return:
    """
    global os_name
    ssd_object.ssd_unicode(string=f"   ", x=32, y=11, font_size=8)
    ssd_object.ssd_normal_text(os_name_dict[os_name], 32, 11)
    ssd_object.ssd_normal_show()


display_os()


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


def bt_show(once_click):
    """
    显示蓝牙键盘，一次点击按键
    :param once_click: 16进制键值或组合键名称
    :return:
    """
    if once_click == "新建文件夹":
        print("创建文件夹")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(keycode.KC_N)
    elif once_click == "删除文件":
        print("删除文件")
        if os_name:
            bt.keyboard.set_keys(keycode.KC_DELETE)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(keycode.KC_BSPACE)
    elif once_click == "复制":
        print("复制")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_C)
    elif once_click == "剪切":
        print("剪切")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_X)
    elif once_click == "粘贴":
        print("粘贴")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_V)
    elif once_click == "全选":
        print("全选")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_A)
    elif once_click == "保存":
        print("保存")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_S)
    elif once_click == "另存为":
        print("另存为")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(keycode.KC_S)
    elif once_click == "查找":
        print("查找")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_F)
    elif once_click == "替换":
        print("替换")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_R)
    elif once_click == "打印":
        print("打印")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_P)
    elif once_click == "返回桌面":
        print("返回桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(keycode.KC_D)
        else:
            bt.keyboard.set_keys(keycode.KC_F11)
    elif once_click == "切换下一个桌面":
        print("切换下一个桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_gui=True)
        else:
            bt.keyboard.set_modifiers(left_control=True)
        bt.keyboard.set_keys(keycode.KC_RIGHT)
    elif once_click == "切换上一个桌面":
        print("切换上一个桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_gui=True)
        else:
            bt.keyboard.set_modifiers(left_control=True)
        bt.keyboard.set_keys(keycode.KC_LEFT)
    elif once_click == "展示窗口":
        print("展示窗口")
        if os_name:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(keycode.KC_TAB)
        else:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(keycode.KC_UP)
    elif once_click == "最小化":
        print("最小化")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(keycode.KC_SPACE)
            bt.keyboard.set_keys(keycode.KC_N)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(keycode.KC_M)
    elif once_click == "跳转助记标签":
        print("跳转助记标签")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_alt=True)
        bt.keyboard.set_keys(keycode.KC_F3)
    elif once_click == "进格":
        print("进格")
        bt.keyboard.set_keys(keycode.KC_TAB)
    elif once_click == "退格":
        print("退格")
        bt.keyboard.set_modifiers(left_shift=True)
        bt.keyboard.set_keys(keycode.KC_TAB)
    elif once_click == "撤回":
        print("撤回")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_Z)
    elif once_click == "恢复":
        print("恢复")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(keycode.KC_Z)
    elif once_click == "关闭窗口":
        print("关闭窗口")
        if os_name:
            bt.keyboard.set_modifiers(left_alt=True)
            bt.keyboard.set_keys(keycode.KC_F4)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(keycode.KC_Q)
    elif once_click == "注释":
        print("注释")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(keycode.KC_SLASH)
    elif once_click == "优化代码":
        print("优化代码")
        if os_name:
            bt.keyboard.set_modifiers(left_gui=True, left_alt=True)
        else:
            bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        bt.keyboard.set_keys(keycode.KC_L)
    elif once_click == "优化import":
        print("优化import")
        bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        bt.keyboard.set_keys(keycode.KC_O)
    elif once_click == "光标末移":
        print("光标末移")
        bt.keyboard.set_modifiers(left_alt=True, left_shift=True)
        bt.keyboard.set_keys(keycode.KC_G)
    elif once_click == "连接行":
        print("连接行")
        bt.keyboard.set_modifiers(left_alt=True, left_shift=True)
        bt.keyboard.set_keys(keycode.KC_J)
    elif once_click is not str:
        bt.keyboard.set_keys(once_click)
    bt.keyboard.notify_hid_report()
    key_show_clear()


def key_show_clear():
    bt.keyboard.set_modifiers()
    bt.keyboard.set_keys()
    bt.keyboard.notify_hid_report()


bt.active(True)
# def bt_connect():
#     while True:
# 根据设备状态调整睡眠时间
if bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
    time.sleep(20)  # 设备已连接时，使用较短的睡眠时间以提高响应速度
else:
    # 如果设备空闲，则开始广播或直到设备连接
    if bt.keyboard.get_state() is Keyboard.DEVICE_IDLE:
        bt.keyboard.start_advertising()  # 开始广播
        bt.wait_for_confirmation(120)  # 等待广播或连接
        if bt.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:  # 如果仍在广播
            bt.keyboard.stop_advertising()  # 则停止广播
    time.sleep(2)  # 设备未连接时，使用较长的睡眠时间以节省电量


# _thread.start_new_thread(bt_connect, ())


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
                    bt_show(keycode.KC_F13)
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
            bt_show(keycode.KC_F16)
        elif knob_a_rotate == (0, 1):
            print(knob_a_rotate)
            bt_show(keycode.KC_F17)
        elif knob_a_rotate == (-1, 0):
            print(knob_a_rotate)
            bt_show(keycode.KC_F14)
        elif knob_a_rotate == (1, 0):
            print(knob_a_rotate)
            bt_show(keycode.KC_F15)

        KCI.knob_double_click_down_incident()
        KCI.knob_left_click_down_incident()
        KCI.knob_right_click_down_incident()
        KCI.knob_right_click_up_time()

        key_show = key.show()
        if not anti_mis_contact_lock_button:
            if key_show is not None:
                if mode_index < list(mode_texts)[-1]:
                    bt_show(mode_texts[mode_index]["key"][key_show[1]][key_show[0]])
                    time.sleep_ms(140)
                if mode_index == list(mode_texts)[-1]:
                    buzzer.play(mode_texts[mode_index]["key"][key_show[1]][key_show[0]])
            else:
                buzzer.play(0)


big_led.value(1)
movement()
