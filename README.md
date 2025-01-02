<h1 align="center">ESP32蓝牙键盘</h1>
<h2 align="center">适用于30pin的esp32或者esp32s模块</h2>

## 环境
MicroPython v1.24.1或以上，使用[官方固件](https://micropython.org/download/ESP32_GENERIC/)
- 512 kB SRAM or more
- 4MiB flash

## 原因
1. 想要一个可自定义功能的小键盘
2. 辅助一些复制、粘贴、切换桌面之类的快捷键日常使用
3. 帮助一些常用软件的的使用，如PS、OBS、L2D
4. esp32的价格比直接买别人做好的便宜很多
5. 初次接触可编程硬件，简单学习一下

## 硬件
- 自动复位按键
- esp32模组
- ssd1306 oled显示屏128x64
- 无源蜂鸣器
- 旋钮x2
- 杜邦线若干

## 功能
1. 蓝牙hid通信
2. 蓝牙数字小键盘
3. 亮度、音量调整
4. 快捷键定义
5. 按键宏定义
6. 音乐小键盘
7. 按键防误触
8. mac和win使用切换

## 简单使用方法
1. 按照接线图连接esp32模组和ssd1306 oled显示屏等其他元件
   - ![wiring_diagram.svg](wiring_diagram.svg)
2. 前往[官网](https://micropython.org/download/ESP32_GENERIC/)下载MicroPython固件
3. 下载并安装[thonny](https://thonny.org/)，使用它将MicroPython固件烧录到esp32模组中
4. 下载本项目代码，通过thonny将代码上传到esp32模组中
5. 上传完成后，重新插拔电源
6. 长按两个旋钮是锁定模式，短按两个旋钮是切换windows和mac模式，键盘按键按下后根据模式输出。
7. 锁定模式下只有键盘按键被禁用，其他动作正常生效
8. 蓝牙未连接时，指示灯会熄灭，且不可操作，连接后指示灯会亮，可正常操作。

## 自定义方法
### 键盘模式定义
1. 添加模式
   1. 添加一个模式相关的键盘定义，向[mode_keyboard_data](BTkeyboard%2Fmode_keyboard_data)文件夹中添加一个名称为模式名称的json文件，文件内容格式如下：
       ```json
       {"data": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]}
       ```
      - 请参考文件夹中的其他文件，或参考[按键定义](#按键定义)部分了解其内容解释。
      - 注意⚠️：显示中给名称留下了4个字节的空间，一个数字或者字母占用1个字节，一个中文占用2个字节，为保证显示效果，第4个字节请尽量不要使用英文或者符号。
   2. 添加一个模式相关的字模文件，向[mode_type_matrix](BTkeyboard%2Fmode_type_matrix)文件夹中添加一个名称为模式名称的txt文件，文件内容格式如下：
      ```json
      {"width": 64, "height": 64, "value": ["static const unsigned char"]}
      ```
      - 请参考文件夹中的其他文件，或参考[字模定义](#字模定义)部分了解其内容解释。
      - "static const unsigned char"数据可以前去[字模生成工具](https://www.zhetao.com/fontarray.html)生成。
      - 注意⚠️：字模文件大小限制为64x64，否则可能导致异常。
      - 注意⚠️：显示中给名称留下了4个字节的空间，一个数字或者字母占用1个字节，一个中文占用2个字节，为保证显示效果，第4个字节请尽量不要使用英文或者符号。
   3. 添加一个模式相关的旋钮定义，向[mode_knob_Rotate_data](BTkeyboard%2Fmode_knob_Rotate_data)文件夹中添加一个名称为模式名称的json文件，文件内容格式如下：
      ```json
      {"data": [105, 106, 107, 108, 104, 104]}
      ```
      - 请参考文件夹中的其他文件，或参考[旋钮定义](#旋钮定义)部分了解其内容解释。
      - 注意⚠️：显示中给名称留下了4个字节的空间，一个数字或者字母占用1个字节，一个中文占用2个字节，为保证显示效果，第4个字节请尽量不要使用英文或者符号。
   4. 打开[main.py](main.py)
      - 找到`not_music_mode`变量，这应该是一个字典，里面定义了键盘是否是音乐模式。
      - 找到`keyboard_mode_list`变量，这应该是一个列表，里面包含了所有可用的模式。
        - 将模式名称添加到列表中，
        - 注意⚠️：请确保该名称在[mode_keyboard_data](BTkeyboard%2Fmode_keyboard_data)、
        [mode_knob_Rotate_data](BTkeyboard%2Fmode_knob_Rotate_data)、
        [mode_type_matrix](BTkeyboard%2Fmode_type_matrix)中均有正确定义文件，并且在`not_music_mode`变量中也有正确的定义。
2. 删除模式
   1. 打开[main.py](main.py)
      - 找到`keyboard_mode_list`变量，这应该是一个列表，里面包含了所有可用的模式。
        - 将列表中要删除的模式名称删除即可。

### 按键定义
1. 每个模式对应的按键定义在[mode_keyboard_data](BTkeyboard%2Fmode_keyboard_data)中，按键定义格式如下：
   ```json
   {"data": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]}
   ```
   - 最外层的列表里面的5个列表表示5个按键行，每个列表中的4个元素表示每个按键所执行的功能。
   - 如果为数字会被识别为hid码可以为[16进制的hid码](https://www.freebsddiary.org/APC/usb_hid_usages)，hid为0时表示不按键，如果为字符串则为快捷键。
   - 注意⚠️：请确保该快捷键在[BT_hid_output.py](BTkeyboard%2FBT_hid_output.py)中被支持。
### 字模定义
1. 每个模式对应的字模定义在[mode_type_matrix](BTkeyboard%2Fmode_type_matrix)中，字模定义格式如下：
   ```json
   {"width": 64, "height": 64, "value": ["static const unsigned char"]}
   ```
   - "width"表示字模的宽度，"height"表示字模的高度，"value"表示字模的二进制数据。"static const unsigned char"数据可以前去[字模生成工具](https://www.zhetao.com/fontarray.html)生成。
   - 注意⚠️：字模文件大小限制为64x64，否则可能导致异常。
### 旋钮定义
1. 每个模式对应的旋钮定义在[mode_knob_Rotate_data](BTkeyboard%2Fmode_knob_Rotate_data)中，旋钮定义格式如下：
   ```json
   {"data": [105, 106, 107, 108, 104, 104]}
   ```
   - 列表中的每个元素依次表示为左旋扭逆时针，左旋扭顺时针，右旋扭逆时针，右旋扭顺时针，左旋扭单击，右旋钮单击所执行的功能。
   - 如果为数字会被识别为hid码可以为[16进制的hid码](https://www.freebsddiary.org/APC/usb_hid_usages)，hid为0时表示不按键，如果为字符串则为快捷键。
   - 注意⚠️：请确保该快捷键在[BT_hid_output.py](BTkeyboard%2FBT_hid_output.py)中被支持。
## 引用
- 蓝牙
  - [MicroPythonBLEHID](https://github.com/Heerkog/MicroPythonBLEHID)，作者：[Heerkog](https://github.com/Heerkog)
- ssd1306 oled 中文显示
  - [MicroPython-uFont](https://github.com/AntonVanke/MicroPython-uFont)，作者：[AntonVanke](https://github.com/AntonVanke)
- 字模
  - [字模生成工具](https://www.zhetao.com/fontarray.html)
- hid键码
  - [usb_hid_usages](https://www.freebsddiary.org/APC/usb_hid_usages)