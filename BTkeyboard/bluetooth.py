import time

from lib.hid_services import Keyboard


class Device:
    def __init__(self, Keyboard_nme: str = "micropython_Keyboard"):
        # 创建键盘设备
        self.keyboard = Keyboard(Keyboard_nme)
        # 设置一个回调函数来捕获设备状态的变化
        self.keyboard.set_state_change_callback(self.keyboard_state_callback)
        # # 启动键盘设备
        self.keyboard.start()

    # 捕获设备状态事件的函数
    def wait_for_confirmation(self, i: int):
        """
        等待键盘广播中的状态改变或超时
        :param i: 广播3*[i]秒,每隔3秒检查一次状态
        """
        while i > 0 and self.keyboard.get_state() is Keyboard.DEVICE_ADVERTISING:  # 等待键盘广播中的状态改变或超时
            time.sleep(3)  # 每3秒检查一次状态
            i -= 1

    def keyboard_state_callback(self):
        """
        键盘状态变化回调函数
        :return:
        """
        # 根据设备的当前状态执行不同的操作
        state = self.keyboard.get_state()
        if state is Keyboard.DEVICE_IDLE:
            return  # 设备空闲时不做任何操作
        elif state is Keyboard.DEVICE_ADVERTISING:
            return  # 设备正在广播时不做任何操作
        elif state is Keyboard.DEVICE_CONNECTED:
            return  # 设备已连接时不做任何操作
        else:
            return  # 未知状态时不做任何操作

    def keyboard_event_callback(self, bytes):
        """
        键盘事件回调函数
        :param bytes:
        :return:
        """
        # 用于处理键盘事件的回调函数，这里仅打印接收到的字节
        print("键盘状态回调与字节: ", bytes)

    def advertise(self):
        # 开始广播键盘设备
        self.keyboard.start_advertising()

    def stop_advertise(self):
        # 停止广播键盘设备
        self.keyboard.stop_advertising()

    def send_char(self, char):
        """
        发送一个字符，只处理字母和空格
        :param char: 要发送的字符
        """
        # 根据输入字符发送HID报告
        if char == " ":
            mod = 0  # 无修饰键
            code = 0x2C  # 空格键对应的HID代码
        elif ord("a") <= ord(char) <= ord("z"):
            mod = 0  # 无修饰键
            code = 0x04 + ord(char) - ord("a")  # 小写字母对应的HID代码
            # 例如，'a' 对应 0x04, 'b' 对应 0x05, ..., 'z' 对应 0x1A
        elif ord("A") <= ord(char) <= ord("Z"):
            mod = 1  # 左Shift修饰键
            code = 0x04 + ord(char) - ord("A")  # 大写字母对应的HID代码
            # 例如，'A' 对应 0x04, 'B' 对应 0x05, ..., 'Z' 对应 0x1A
        elif ord("1") <= ord(char) <= ord("9"):
            mod = 0  # 无修饰键
            code = 0x1E + ord(char) - ord("1")  # 数字键对应的HID代码
            # 例如，'0' 对应 0x27, '1' 对应 0x28, ..., '9' 对应 0x2C
        elif char == "0":
            mod = 0  # 无修饰键
            code = 0x27  # 数字0对应的HID代码
        elif char == "/":  # 处理键盘上的符号
            mod = 0  # 左Shift修饰键
            code = 0x38  # 符号/对应的HID代码
        elif char == "*":
            mod = 1  # 左Shift修饰键
            code = 0x25  # 符号*对应的HID代码
        elif char == "-":
            mod = 0  # 左Shift修饰键
            code = 0x2D  # 符号-对应的HID代码
        elif char == "+":
            mod = 1  # 左Shift修饰键
            code = 0x2E  # 符号+对应的HID代码
        elif char == ".":
            mod = 0  # 左Shift修饰键
            code = 0x37
        elif char == "\n":
            mod = 0  # 无修饰键
            code = 0x28  # 回车键对应的HID代码
        elif char == "\t":
            mod = 0  # 无修饰键
            code = 0x2B  # 制表符键对应的HID代码
        elif char == "\b":
            mod = 0  # 无修饰键
            code = 0x2A  # 退格键对应的HID代码
        elif char == "\r":
            mod = 0  # 无修饰键
            code = 0x29  # 回车键对应的HID代码
        else:
            mod = 0
            code = 0x00
            # assert 0  # 对于其他字符，抛出断言错误，假设只处理字母和空格
            pass

        # 设置要发送的键码
        self.keyboard.set_keys(code)
        # 设置修饰键
        self.keyboard.set_modifiers(left_shift=mod)
        # 发送HID报告
        self.keyboard.notify_hid_report()
        # 等待2毫秒以确保按键事件被正确处理
        time.sleep_ms(2)

        # 释放按键和修饰键
        self.keyboard.set_keys()  # 不传递参数表示释放所有按键
        self.keyboard.set_modifiers()  # 不传递参数表示释放所有修饰键
        # 再次发送HID报告以确保按键被释放
        self.keyboard.notify_hid_report()
        # 等待2毫秒以确保释放事件被正确处理
        time.sleep_ms(2)

    def send_string(self, st):
        """
        发送一个字符串
        :param st: 要发送的字符串
        """
        # 发送一个字符串
        for c in st:
            self.send_char(c)
            time.sleep_ms(10)

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
                # 停止键盘设备
                self.keyboard.stop()

    # 仅用于测试
    def stop(self):
        # 停止键盘设备
        self.keyboard.stop()

