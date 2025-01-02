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
import network

from BTkeyboard.BT_hid_output import OutputHidIncident
from BTkeyboard.bluetooth import Device as BluetoothDevice
from lib import ufont
from lib.hid_services import Keyboard
from lib.ssd1306 import SSD1306_I2C

# 创建网络对象
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)
# 创建蜂鸣器对象
pwm_pin = Pin(32, Pin.OUT)
Buzzer = PWM(pwm_pin, freq=40000000, duty=0)
# 创建指示灯对象
pilot_lamp = Pin(33, Pin.OUT)
# 创建蓝牙对象
bt = BluetoothDevice("ESP32_Keyboard")
# 创建屏幕对象
ssd = SSD1306_I2C(128, 64, I2C(0, sda=Pin(21), scl=Pin(22), freq=400000))
uFont = ufont.BMFont("fonts/unifont-14-12888-16.v3.bmf")
# 定义全局变量
network_is = False  # 网络连接状态
musical_scale = 2  # 音阶
double_click_keep_time = 0
left_click_keep_time = 0
right_click_keep_time = 0
left_click_ready_time = 0
right_click_ready_time = 0
rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
with open(f"BTkeyboard/config.json", "r") as f:
    mode_index = json.load(f)["mode_index"]
with open(f"BTkeyboard/config.json", "r") as f:
    lock_mode = json.load(f)["lock_mode"]
with open(f"BTkeyboard/config.json", "r") as f:
    win_os_is = json.load(f)["win_os_is"]
with open(f"BTkeyboard/mode_list.json", "r") as f:
    mode_list = json.load(f)["data"]
    mode_num = len(mode_list)
    mode_name = mode_list[mode_index]
    del mode_list
with open(f"BTkeyboard/mode_music_is/{mode_name}.json", "r") as f:
    mode_music_is = json.load(f)["data"]
with open(f"BTkeyboard/mode_keyboard_data/{mode_name}.json", "r") as f:
    _keys = json.load(f)["data"]
with open(f"BTkeyboard/mode_knob_Rotate_data/{mode_name}.json", "r") as f:
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


# 初始化网络
ap.active(False)
sta.active(False)

# 初始化蓝牙
bt.active(True)

# 初始化屏幕
# 显示标题
uFont.text(display=ssd, string=mode_name, x=0, y=32, font_size=32, show=True, half_char=True)
with open(f"BTkeyboard/mode_type_matrix/{mode_name}.json", "r") as f:
    ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)
# 显示锁定模式
if lock_mode:
    with open(f"BTkeyboard/lock_type_matrix/1.json", "r") as f:
        ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
else:
    with open(f"BTkeyboard/lock_type_matrix/0.json", "r") as f:
        ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
# 显示操作系统
uFont.text(display=ssd, string={True: "O", False: "A"}[win_os_is], x=32, y=0, font_size=32)
ssd.show()

# 初始化指示灯
pilot_lamp.value(0)

# 初始化蜂鸣器
if mode_music_is:
    Buzzer.duty(0)
    Buzzer.freq(40000000)
else:
    Buzzer.deinit()
    pwm_pin.value(0)


def bt_run():
    while True:
        # 如果设备空闲，则开始广播或直到设备连接
        if bt.keyboard.get_state() is Keyboard.DEVICE_IDLE and not network_is:
            bt.keyboard.start_advertising()  # 开始广播
            bt.wait_for_confirmation(60)  # 等待广播或连接
            if bt.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:  # 如果仍在广播
                bt.keyboard.stop_advertising()  # 则停止广播
        time.sleep(2)


# 创建线程
_thread.start_new_thread(bt_run, ())

while True:
    # 读取旋钮按下状态
    knob_click = Pin(25, Pin.IN, Pin.PULL_DOWN).value(), Pin(26, Pin.IN, Pin.PULL_DOWN).value()
    if knob_click == (1, 1):
        left_click_keep_time = 0
        right_click_keep_time = 0
        left_click_ready_time = 0
        right_click_ready_time = 0
        double_click_keep_time += 1
        if double_click_keep_time == 1:
            print(f"双键按下")
        if double_click_keep_time == 140:
            print(f"双键按下超过{double_click_keep_time}毫秒")
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
        time.sleep_ms(1)
    if knob_click == (1, 0):
        # 防止双键按下抬起时左键的误触发，
        # 双键按下后抬起右键后，这时左键的按下时间为预备时间，
        # 预备时间时双键按下时间不会清空，依然视为双键按下
        # 超出预备时间才算真正开始按下左键
        if double_click_keep_time > 0:
            left_click_ready_time += 1
            if left_click_ready_time == 1:
                print(f"双键按下后，左键准备")
            if left_click_ready_time == 50:  # 预备持续时间
                print(f"左键预备结束")
                double_click_keep_time = 0
        if double_click_keep_time == 0:
            double_click_keep_time = 0
            right_click_keep_time = 0
            left_click_ready_time = 0
            right_click_ready_time = 0
            left_click_keep_time += 1
            if left_click_keep_time == 1:
                print(f"左键按下")
            if left_click_keep_time == 140:
                print(f"左键按下超过{left_click_keep_time}秒")
                network_is = not network_is
                if network_is:
                    ssd.fill(0)
                    print(f"网络已开启")
                    bt.active(False)
                    ap.active(True)
                    with open(f"BTkeyboard/ap.json", "r") as f:
                        ap_config = json.load(f)
                        if len(ap_config["password"]) >= 8:
                            ap.config(essid=ap_config["essid"], authmode=network.AUTH_WPA_WPA2_PSK, password=ap_config["password"])
                            print(f"AP已开启,账号为{ap_config['essid']},密码为{ap_config['password']}")
                            ssd.text(ap_config['essid'], 0, 0, 1)
                            ssd.text(ap_config['password'], 0, 8, 1)
                        else:
                            ap.config(essid=ap_config["essid"], authmode=network.AUTH_OPEN)
                            print(f"AP已开启,账号为{ap_config['essid']}")
                            ssd.text(ap_config['essid'], 0, 0, 1)
                    ssd.text(ap.ifconfig()[0], 0, 16, 1)
                    ssd.show()
                    sta.active(True)
                    del ap_config
                    with open(f"BTkeyboard/sta.json", "r") as f:
                        sta_config = json.load(f)
                        if len(sta_config) == 0:
                            print(f"未配置STA连接信息")
                            ssd.text("StaNotConfigured", 0, 32, 1)
                            ssd.show()
                        else:
                            pass
                    del sta_config
                else:
                    ssd.fill(0)
                    ssd.show()
                    print(f"网络已关闭")
                    sta.active(False)
                    ap.active(False)
                    bt.active(True)
                    # 初始化屏幕
                    # 显示标题
                    uFont.text(display=ssd, string=mode_name, x=0, y=32, font_size=32, show=True, half_char=True)
                    with open(f"BTkeyboard/mode_type_matrix/{mode_name}.json", "r") as f:
                        ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)
                    # 显示锁定模式
                    if lock_mode:
                        with open(f"BTkeyboard/lock_type_matrix/1.json", "r") as f:
                            ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
                    else:
                        with open(f"BTkeyboard/lock_type_matrix/0.json", "r") as f:
                            ssd_type_matrix_text(json.load(f), x=0, y=0, show=True, fill=True)
                    # 显示操作系统
                    uFont.text(display=ssd, string={True: "O", False: "A"}[win_os_is], x=32, y=0, font_size=32)
                    ssd.show()
                    del f
        time.sleep_ms(1)
    if knob_click == (0, 1):
        # 防止双键按下抬起时右键的误触发，
        # 双键按下后抬起左键后，这时右键的按下时间为预备时间，
        # 预备时间时双键按下时间不会清空，依然视为双键按下
        # 超出预备时间才算真正开始按下右键
        if double_click_keep_time > 0:
            right_click_ready_time += 1
            if right_click_ready_time == 1:
                print(f"双键按下后，右键预备")
            if right_click_ready_time == 50:  # 预备持续时间
                print(f"右键预备结束")
                double_click_keep_time = 0
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
                if bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
                    OutputHidIncident(bt, _knobs[5], win_os_is)
        time.sleep_ms(1)
    if knob_click == (0, 0):
        if double_click_keep_time:
            print(f"双键抬起,{double_click_keep_time}")
            if double_click_keep_time < 100:  # 单击
                if not network_is:
                    # 切换os
                    win_os_is = not win_os_is
                    # 切换系统时，记录进BTkeyboard/config.json的“win_os_is”参数中
                    with open(f"BTkeyboard/config.json", "r") as f:
                        config = json.load(f)
                        config["win_os_is"] = win_os_is
                    with open(f"BTkeyboard/config.json", "w") as f:
                        print(config)
                        f.write(json.dumps(config))
                    del config, f
                    # 切换系统时，更新显示屏上的操作系统字母
                    uFont.text(display=ssd, string={True: "O", False: "A"}[win_os_is], x=32, y=0, font_size=32)
                    ssd.show()
        if left_click_keep_time:
            print(f"左键抬起,{left_click_keep_time}")
            if left_click_keep_time < 100:  # 单击
                if not network_is:
                    # 切换模式
                    mode_index = (mode_index - 1) % mode_num
                    # 切换模式时，记录进BTkeyboard/config.json的“mode_index”参数中
                    with open(f"BTkeyboard/config.json", "r") as f:
                        config = json.load(f)
                        config["mode_index"] = mode_index
                    with open(f"BTkeyboard/config.json", "w") as f:
                        print(config)
                        f.write(json.dumps(config))
                    del config
                    # 更新模式名称
                    with open(f"BTkeyboard/mode_list.json", "r") as f:
                        mode_list = json.load(f)["data"]
                        mode_name = mode_list[mode_index]
                        del mode_list
                    # 更新显示屏模式内容
                    uFont.text(display=ssd, string=mode_name, x=0, y=32, font_size=32,
                               show=True, half_char=True)
                    with open(f"BTkeyboard/mode_type_matrix/{mode_name}.json", "r") as f:
                        ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)
                    # 重置蜂鸣器
                    with open(f"BTkeyboard/mode_music_is/{mode_name}.json", "r") as f:
                        mode_music_is = json.load(f)["data"]
                    if mode_music_is:
                        # 重新创建蜂鸣器对象
                        Buzzer = PWM(Pin(32, Pin.OUT), freq=40000000, duty=0)
                    else:
                        # 关闭蜂鸣器
                        Buzzer.deinit()
                        pwm_pin.value(0)
                    # 重置键盘数据
                    with open(f"BTkeyboard/mode_keyboard_data/{mode_name}.json", "r") as f:
                        _keys = json.load(f)["data"]
                    # 重置旋钮数据
                    with open(f"BTkeyboard/mode_knob_Rotate_data/{mode_name}.json", "r") as f:
                        _knobs = json.load(f)["data"]
                    del f
        if right_click_keep_time:
            print(f"右键抬起,{right_click_keep_time}")
            if right_click_keep_time < 100:   # 单击
                if not network_is:
                    # 切换模式
                    mode_index = (mode_index + 1) % mode_num
                    # 切换模式时，记录进BTkeyboard/config.json的“mode_index”参数中
                    with open(f"BTkeyboard/config.json", "r") as f:
                        config = json.load(f)
                        config["mode_index"] = mode_index
                    with open(f"BTkeyboard/config.json", "w") as f:
                        print(config)
                        f.write(json.dumps(config))
                    del config
                    # 更新模式名称
                    with open(f"BTkeyboard/mode_list.json", "r") as f:
                        mode_list = json.load(f)["data"]
                        mode_name = mode_list[mode_index]
                        del mode_list
                    # 更新显示屏模式内容
                    uFont.text(display=ssd, string=mode_name, x=0, y=32, font_size=32,
                               show=True, half_char=True)
                    with open(f"BTkeyboard/mode_type_matrix/{mode_name}.json", "r") as f:
                        ssd_type_matrix_text(json.load(f), x=64, y=0, show=True, fill=True)
                    # 重置蜂鸣器
                    with open(f"BTkeyboard/mode_music_is/{mode_name}.json", "r") as f:
                        mode_music_is = json.load(f)["data"]
                    if mode_music_is:
                        # 重新创建蜂鸣器对象
                        Buzzer = PWM(Pin(32, Pin.OUT), freq=40000000, duty=0)
                    else:
                        # 关闭蜂鸣器
                        Buzzer.deinit()
                        pwm_pin.value(0)
                    # 重置键盘数据
                    with open(f"BTkeyboard/mode_keyboard_data/{mode_name}.json", "r") as f:
                        _keys = json.load(f)["data"]
                    # 重置旋钮数据
                    with open(f"BTkeyboard/mode_knob_Rotate_data/{mode_name}.json", "r") as f:
                        _knobs = json.load(f)["data"]
                    del f
        double_click_keep_time = 0
        left_click_keep_time = 0
        right_click_keep_time = 0
        left_click_ready_time = 0
        right_click_ready_time = 0

    # 键盘事件
    if not network_is:
        if bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
            # 飞行灯
            pilot_lamp.value(1)
        if not lock_mode:
            if bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:  # 设备连接蓝牙才响应键盘事件
                # 旋钮状态
                rnt = Pin(13, Pin.IN, Pin.PULL_DOWN).value(), Pin(12, Pin.IN, Pin.PULL_DOWN).value()
                lnt = Pin(14, Pin.IN, Pin.PULL_DOWN).value(), Pin(27, Pin.IN, Pin.PULL_DOWN).value()
                if rnt != rp[3]:
                    rp[0] = rp[1]
                    rp[1] = rp[2]
                    rp[2] = rp[3]
                    rp[3] = rnt
                if rp == {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}:  # 顺时针
                    rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                    # 音量+
                    OutputHidIncident(bt, _knobs[3], win_os_is)
                elif rp == {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}:  # 逆时针
                    rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                    # 音量-
                    OutputHidIncident(bt, _knobs[2], win_os_is)
                if lnt != lp[3]:
                    lp[0] = lp[1]
                    lp[1] = lp[2]
                    lp[2] = lp[3]
                    lp[3] = lnt
                if lp == {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}:  # 顺时针
                    lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                    # 亮度+
                    OutputHidIncident(bt, _knobs[1], win_os_is)
                elif lp == {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}:  # 逆时针
                    lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                    # 亮度-
                    OutputHidIncident(bt, _knobs[0], win_os_is)
                del rnt, lnt

            if bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED or mode_music_is:
                # 键盘事件
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
                if not mode_music_is:
                    if line_col is not None and bt.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
                        print(line_col)  # 返回按下的按键
                        once_click = _keys[line_col[0]][line_col[1]]
                        OutputHidIncident(bt, _keys[line_col[0]][line_col[1]], win_os_is)
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
    else:
        pilot_lamp.value(0)  # 关闭飞行灯
