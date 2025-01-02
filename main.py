#         Copyright (C) 2024  lanyangyin
#
#         This program is free software: you can redistribute it and/or modify
#         it under the terms of the GNU General Public License as published by
#         the Free Software Foundation, either version 3 of the License, or
#         (at your option) any later version.
#
#         This program is distributed in the hope that it will be useful,
#         but WITHOUT ANY WARRANTY; without even the implied warranty of
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#         GNU General Public License for more details.
#
#         You should have received a copy of the GNU General Public License
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.
#         2436725966@qq.com
import _thread
import json
import math
import time

from machine import Pin, I2C, PWM

from BTkeyboard.BT_hid_output import OutputHidIncident
from lib import ufont
from lib.hid_services import Keyboard
from lib.ssd1306 import SSD1306_I2C


# 定义蓝牙对象
class BluetoothDevice:
    def __init__(self):
        """
        初始化蓝牙对象
        """
        # 创建键盘设备
        with open("BTkeyboard/bt.json", "r") as f:
            self.keyboard = Keyboard(json.load(f)["name"])
        # 设置一个回调函数来捕获设备状态的变化
        self.keyboard.set_state_change_callback(self.keyboard_state_callback)

    def active(self, active: bool = None):
        """
        设置键盘的活动状态
        :param active: True  # 使能键盘。 False  # 禁止键盘。 None  # 不修改当前状态。
        :return: 0  # 设备未进行广播或连接。 1    # 设备处于空闲状态，可以进行广播。  2  # 设备正在广播。  3  # 设备已连接。

        """
        if active is None:
            return self.keyboard.get_state()
        else:
            if active:
                # 启动键盘设备
                self.keyboard.start()
            else:
                if self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:  # 如果仍在广播
                    # 停止广播键盘设备
                    self.keyboard.stop_advertising()
                # 停止键盘设备
                self.keyboard.stop()

    # 捕获设备状态事件的函数
    def wait_for_confirmation(self, i: int):
        """
        等待键盘广播中的状态改变或超时
        :param i: 广播3*[i]秒,每隔3秒检查一次状态
        """
        while i > 0 and self.active() is Keyboard.DEVICE_ADVERTISING:  # 等待键盘广播中的状态改变或超时
            time.sleep(3)  # 每3秒检查一次状态
            i -= 1

    def keyboard_state_callback(self):
        """
        键盘状态变化回调函数
        :return:
        """
        # 根据设备的当前状态执行不同的操作
        state = self.active()
        if state is Keyboard.DEVICE_IDLE:
            return  # 设备空闲时不做任何操作
        elif state is Keyboard.DEVICE_ADVERTISING:
            return  # 设备正在广播时不做任何操作
        elif state is Keyboard.DEVICE_CONNECTED:
            return  # 设备已连接时不做任何操作
        else:
            return  # 未知状态时不做任何操作


# 定义旋钮对象
class KnobDevice:
    def __init__(self, Knob_pin_id_list: list):
        """
        初始化旋钮对象
        :param Knob_pin_id_list: [左旋扭左侧,左旋扭右侧,右旋扭左侧,右旋扭右侧，左旋扭按下，右旋扭按下]
        """
        self.Knob_pin_list = []
        for pin_id_index, pin_id in enumerate(Knob_pin_id_list):
            self.Knob_pin_list[pin_id_index] = Pin(pin_id, Pin.IN, Pin.PULL_DOWN)
        self.double_click_keep_time = 0
        self.left_click_keep_time = 0
        self.right_click_keep_time = 0
        self.left_click_ready_time = 0
        self.right_click_ready_time = 0
        self.lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
        self.rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
        self.click_state = 0
        self.rotate_state = [0, 0]

    def click(self):
        # 点击旋钮
        # 读取旋钮按下状态
        knob_click = self.Knob_pin_list[4].value(), self.Knob_pin_list[5].value()
        if knob_click == (1, 0):
            # 防止双键按下抬起时左键的误触发，
            # 双键按下后抬起右键后，这时左键的按下时间为预备时间，
            # 预备时间时双键按下时间不会清空，依然视为双键按下
            # 超出预备时间才算真正开始按下左键
            if self.double_click_keep_time > 0:
                self.left_click_ready_time += 1
                if self.left_click_ready_time == 1:
                    print(f"双键按下后，左键准备")
                if self.left_click_ready_time == 50:  # 预备持续时间
                    print(f"左键预备结束")
                    self.double_click_keep_time = 0
            if self.double_click_keep_time == 0:
                self.double_click_keep_time = 0
                self.right_click_keep_time = 0
                self.left_click_ready_time = 0
                self.right_click_ready_time = 0
                self.left_click_keep_time += 1
                if self.left_click_keep_time == 1:
                    print(f"左键按下")
                if self.left_click_keep_time == 140:
                    print(f"左键长按，{self.left_click_keep_time}秒")
                    self.click_state = 11
        if knob_click == (0, 1):
            # 防止双键按下抬起时右键的误触发，
            # 双键按下后抬起左键后，这时右键的按下时间为预备时间，
            # 预备时间时双键按下时间不会清空，依然视为双键按下
            # 超出预备时间才算真正开始按下右键
            if self.double_click_keep_time > 0:
                self.right_click_ready_time += 1
                if self.right_click_ready_time == 1:
                    print(f"双键按下后，右键预备")
                if self.right_click_ready_time == 50:  # 预备持续时间
                    print(f"右键预备结束")
                    self.double_click_keep_time = 0
            if self.double_click_keep_time == 0:
                self.double_click_keep_time = 0
                self.left_click_keep_time = 0
                self.right_click_keep_time += 1
                self.left_click_ready_time = 0
                self.right_click_ready_time = 0
                if self.right_click_keep_time == 1:
                    print(f"右键按下")
                if self.right_click_keep_time == 140:
                    print(f"右键长按，{self.right_click_keep_time}毫秒")
                    self.click_state = 22
        if knob_click == (1, 1):
            self.left_click_keep_time = 0
            self.right_click_keep_time = 0
            self.left_click_ready_time = 0
            self.right_click_ready_time = 0
            self.double_click_keep_time += 1
            if self.double_click_keep_time == 1:
                print(f"双键按下")
            if self.double_click_keep_time == 140:
                print(f"双键长按，{self.double_click_keep_time}毫秒")
                self.click_state = 33
        if knob_click == (0, 0):
            if self.left_click_keep_time:
                print(f"左键抬起,{self.left_click_keep_time}")
                if self.right_click_keep_time < 100:
                    print(f"左键单击,{self.left_click_keep_time}")
                    self.click_state = 1
            if self.right_click_keep_time:
                print(f"右键抬起,{self.right_click_keep_time}")
                if self.right_click_keep_time < 100:
                    print(f"右键单击,{self.right_click_keep_time}")
                    self.click_state = 2
            if self.double_click_keep_time:
                print(f"双键抬起,{self.double_click_keep_time}")
                if self.double_click_keep_time < 100:
                    print(f"双键单击,{self.double_click_keep_time}")
                    self.click_state = 3
            self.click_state = 0
            self.double_click_keep_time = 0
            self.left_click_keep_time = 0
            self.right_click_keep_time = 0
            self.left_click_ready_time = 0
            self.right_click_ready_time = 0
        time.sleep_ms(1)

    def rotate(self):
        # 旋钮状态
        lnt = self.Knob_pin_list[0].value(), self.Knob_pin_list[1].value()
        if lnt != self.lp[3]:
            self.lp[0] = self.lp[1]
            self.lp[1] = self.lp[2]
            self.lp[2] = self.lp[3]
            self.lp[3] = lnt
        if self.lp == {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}:  # 逆时针
            self.lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            print("左旋扭逆时针")
            self.rotate_state[0] = -1
        elif self.lp == {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}:  # 顺时针
            self.lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            print("左旋扭顺时针")
            self.rotate_state[0] = 1
        elif self.lp == {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}:  # 静止
            self.rotate_state[0] = 0
        rnt = self.Knob_pin_list[2].value(), self.Knob_pin_list[3].value()
        if rnt != self.rp[3]:
            self.rp[0] = self.rp[1]
            self.rp[1] = self.rp[2]
            self.rp[2] = self.rp[3]
            self.rp[3] = rnt
        if self.rp == {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}:  # 逆时针
            self.rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            print("右旋扭逆时针")
            self.rotate_state[1] = -1
        elif self.rp == {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}:  # 顺时针
            self.rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            print("右旋扭顺时针")
            self.rotate_state[1] = 1
        elif self.rp == {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}:  # 静止
            self.rotate_state[1] = 0


# 创建蓝牙对象
bt = BluetoothDevice()
bt.active(True)
# 创建旋钮对象
Knob = KnobDevice([14, 27, 13, 12, 25, 26])
# 创建指示灯对象
pilot_lamp = Pin(33, Pin.OUT)
# 创建蜂鸣器对象
pwm_pin = Pin(32, Pin.OUT)
Buzzer = PWM(pwm_pin, freq=40000000, duty=0)
# 创建屏幕对象
ssd = SSD1306_I2C(128, 64, I2C(0, sda=Pin(21), scl=Pin(22), freq=400000))
uFont = ufont.BMFont("fonts/unifont-14-12888-16.v3.bmf")
# 定义全局变量
musical_scale = 2
double_click_keep_time = 0
left_click_keep_time = 0
right_click_keep_time = 0
left_click_ready_time = 0
right_click_ready_time = 0
rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
keyboard_mode_list = ["原始", "代码", "常规", "P S", "L2D", "OBS", "音乐"]
not_music_mode = {"原始": True, "代码": True, "常规": True, "P S": True, "L2D": True, "OBS": True, "音乐": False}
with open(f"BTkeyboard/config.json", "r") as f:
    mode_num = json.load(f)["mode_num"]
with open(f"BTkeyboard/config.json", "r") as f:
    lock_mode = json.load(f)["lock_mode"]
with open(f"BTkeyboard/config.json", "r") as f:
    os_name = json.load(f)["os_name"]
with open(f"BTkeyboard/mode_keyboard_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
    _keys = json.load(f)["data"]
with open(f"BTkeyboard/mode_knob_Rotate_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
    _knobs = json.load(f)["data"]
with open(f"BTkeyboard/buzzer_data/{musical_scale}.json", "r") as f:
    tone_dict = json.load(f)
del f


def ssd_type_matrix_text(font_data: dict, x: int, y: int, show: bool = False, clear: bool = False,
                         reverse: bool = False, fill: bool = False):
    """
    显示type_matrix字库中的字形
    :param font_data: 从字库中获取汉字的字体数据，包含字形的高度和宽度等信息
    :param x: 显示的x坐标
    :param y: 显示的y坐标
    :param show: 是否立即显示
    :param clear: 是否清空屏幕
    :param reverse: 是否反色
    :param fill: 是否填充
    :return:
    """
    if clear:
        ssd.fill(0)
    if reverse:
        fill = True
        reverse_dict = {0: 1, 1: 0}
    else:
        reverse_dict = {0: 0, 1: 1}
    index = 0  # 初始化索引，记录当前字形数据的位置
    # 遍历字形的高度
    for ty in range(font_data['height']):
        row_bytes = ''  # 用于存储汉字每一行的像素二进制数据
        # 遍历字形的列，计算需要的字节数
        for col in range(math.ceil(font_data['width'] / 8)):
            # 将字形数据转换为二进制字符串并去掉前缀'0b'
            point_data = bin(font_data["value"][index]).replace('0b', '')
            # 确保二进制字符串长度为8位，不足位数的用'0'填充
            while len(point_data) < 8:
                point_data = '0' + point_data
            # 将当前列的字形数据添加到raw_bytes中
            row_bytes += point_data
            index += 1  # 移动索引到下一个字形数据位置
        # 遍历当前行中的每个像素
        for tx in range(math.ceil(font_data['width'] / 8) * 8):
            # 根据fill参数和像素值决定是否绘制该点
            if fill or int(row_bytes[tx]):
                # 在LCD屏幕上绘制对应的像素点
                ssd.pixel(tx + x, ty + y, reverse_dict[int(row_bytes[tx])])
    if show:
        ssd.show()


# 初始化屏幕
# 显示标题
uFont.text(display=ssd, string=keyboard_mode_list[mode_num], x=0, y=32, font_size=32, show=True, half_char=True)
with open(f"BTkeyboard/mode_type_matrix/{keyboard_mode_list[mode_num]}.json", "r") as f:
    ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)
# 显示锁定模式
if lock_mode:
    with open(f"BTkeyboard/lock_type_matrix/1.json", "r") as f:
        ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
else:
    with open(f"BTkeyboard/lock_type_matrix/0.json", "r") as f:
        ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
# 显示操作系统
uFont.text(display=ssd, string={True: "O", False: "A"}[os_name], x=32, y=0, font_size=32)
ssd.show()

# 初始化指示灯
pilot_lamp.value(0)

# 初始化蜂鸣器
if not not_music_mode[keyboard_mode_list[mode_num]]:
    Buzzer.duty(0)
    Buzzer.freq(40000000)
else:
    Buzzer.deinit()
    pwm_pin.value(0)


def bt_connect():
    """
    蓝牙连接
    :return:
    """
    while True:
        if bt.active() is Keyboard.DEVICE_CONNECTED:  # 如果已连接
            pilot_lamp.value(1)  # 打开飞行灯
            time.sleep(10)  # 等待10秒
        else:
            pilot_lamp.value(0)  # 关闭飞行灯
            # 如果设备空闲，则开始广播或直到设备连接
            if bt.active() is Keyboard.DEVICE_IDLE:
                bt.keyboard.start_advertising()  # 开始广播
                bt.wait_for_confirmation(60)  # 等待广播或连接
                if bt.active() is Keyboard.DEVICE_ADVERTISING:  # 如果仍在广播
                    bt.keyboard.stop_advertising()  # 则停止广播


_thread.start_new_thread(bt_connect, ())  # 启动线程，连接蓝牙


def knob_rotate():
    """
    旋钮旋转
    :return:
    """
    while True:
        Knob.rotate()


_thread.start_new_thread(knob_rotate, ())  # 启动线程，旋钮旋转


def knob_click():
    """
    旋钮点击
    :return:
    """
    while True:
        Knob.click()


_thread.start_new_thread(knob_click, ())  # 启动线程，旋钮点击

while True:
    # 蓝牙连接
    if bt.active() is Keyboard.DEVICE_CONNECTED:
        # 读取旋钮按下状态
        if Knob.click_state == 22:
            if bt.active() is Keyboard.DEVICE_CONNECTED:
                bt.keyboard.set_keys(0x68)
                bt.keyboard.notify_hid_report()
                bt.keyboard.set_keys()
                bt.keyboard.notify_hid_report()

        if Knob.click_state == 33:
            lock_mode = not lock_mode
            if lock_mode:
                with open(f"BTkeyboard/lock_type_matrix/1.json", "r") as f:
                    ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
            else:
                with open(f"BTkeyboard/lock_type_matrix/0.json", "r") as f:
                    ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
            # 切换锁定模式时，记录进BTkeyboard/config.json的“设备锁定”参数中
            with open(f"BTkeyboard/config.json", "r") as f:
                config = json.load(f)
                config["lock_mode"] = lock_mode
            with open(f"BTkeyboard/config.json", "w") as f:
                print(config)
                f.write(json.dumps(config))
            del config

        if Knob.click_state == 1:
            mode_num = (mode_num - 1) % len(keyboard_mode_list)
            # 初始化蜂鸣器
            if not not_music_mode[keyboard_mode_list[mode_num]]:
                # 创建蜂鸣器对象
                Buzzer = PWM(Pin(32, Pin.OUT), freq=40000000, duty=0)
            else:
                Buzzer.deinit()
                pwm_pin.value(0)
            with open(f"BTkeyboard/config.json", "r") as f:
                config = json.load(f)
                config["mode_num"] = mode_num
            with open(f"BTkeyboard/config.json", "w") as f:
                print(config)
                f.write(json.dumps(config))
            del config
            with open(f"BTkeyboard/mode_keyboard_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
                _keys = json.load(f)["data"]
            with open(f"BTkeyboard/mode_knob_Rotate_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
                _knobs = json.load(f)["data"]
            uFont.text(display=ssd, string=keyboard_mode_list[mode_num], x=0, y=32, font_size=32,
                       show=True, half_char=True)
            with open(f"BTkeyboard/mode_type_matrix/{keyboard_mode_list[mode_num]}.json", "r") as f:
                ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)

        if Knob.click_state == 2:
            mode_num = (mode_num + 1) % len(keyboard_mode_list)
            # 初始化蜂鸣器
            if not not_music_mode[keyboard_mode_list[mode_num]]:
                # 创建蜂鸣器对象
                Buzzer = PWM(Pin(32, Pin.OUT), freq=40000000, duty=0)
            else:
                Buzzer.deinit()
                pwm_pin.value(0)
            with open(f"BTkeyboard/config.json", "r") as f:
                config = json.load(f)
                config["mode_num"] = mode_num
            with open(f"BTkeyboardconfig.json", "w") as f:
                print(config)
                f.write(json.dumps(config))
            del config
            with open(f"BTkeyboard/mode_keyboard_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
                _keys = json.load(f)["data"]
            with open(f"BTkeyboard/mode_knob_Rotate_data/{keyboard_mode_list[mode_num]}.json", "r") as f:
                _knobs = json.load(f)["data"]
            uFont.text(display=ssd, string=keyboard_mode_list[mode_num], x=0, y=32, font_size=32,
                       show=True, half_char=True)
            with open(f"BTkeyboard/mode_type_matrix/{keyboard_mode_list[mode_num]}.json", "r") as f:
                ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)

        if Knob.click_state == 3:
            os_name = not os_name
            # 切换系统时，记录进BTkeyboard/config.json的“设备系统”参数中
            with open(f"BTkeyboard/config.json", "r") as f:
                config = json.load(f)
                config["os_name"] = os_name
            with open(f"BTkeyboard/config.json", "w") as f:
                print(config)
                f.write(json.dumps(config))
            del config
            uFont.text(display=ssd, string={True: "O", False: "A"}[os_name], x=32, y=0, font_size=32)
            ssd.show()

        # 旋钮状态
        if Knob.rotate_state[1] == 1:
            OutputHidIncident(bt, _knobs[3], os_name)
        if Knob.rotate_state[1] == -1:
            OutputHidIncident(bt, _knobs[2], os_name)
        if Knob.rotate_state[0] == 1:
            OutputHidIncident(bt, _knobs[1], os_name)
        if Knob.rotate_state[0] == -1:
            OutputHidIncident(bt, _knobs[0], os_name)

        # 键盘事件
        if not lock_mode:
            line_col = None
            for j, col_pin in enumerate(
                    [Pin(15, Pin.OUT), Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]):
                col_pin.value(0)  # 将当前列设置为低电平
                for i, row_pin in enumerate(
                        [Pin(5, Pin.IN, Pin.PULL_UP), Pin(18, Pin.IN, Pin.PULL_UP), Pin(19, Pin.IN, Pin.PULL_UP),
                         Pin(23, Pin.IN, Pin.PULL_UP)]):
                    if row_pin.value() == 0:  # 检测行引脚的状态
                        # 将当前列恢复为高电平
                        col_pin.value(1)
                        line_col = j, i  # 记录当前按键的行列号
                col_pin.value(1)  # 将当前列恢复为高电平
            if not_music_mode[keyboard_mode_list[mode_num]]:
                if line_col is not None:
                    print(line_col)  # 返回按下的按键
                    once_click = _keys[line_col[0]][line_col[1]]
                    OutputHidIncident(bt, _keys[line_col[0]][line_col[1]], os_name)
                    time.sleep_ms(170)
            else:
                if line_col is not None:
                    if int(tone_dict[str(_keys[line_col[0]][line_col[1]])]) > 0:
                        Buzzer.duty(900)
                        Buzzer.freq(int(tone_dict[str(_keys[line_col[0]][line_col[1]])]))
                else:
                    Buzzer.duty(0)
                    Buzzer.freq(40000000)
                pass
