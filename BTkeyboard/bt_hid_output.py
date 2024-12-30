from BTkeyboard.keys_config import KeyCode

keycode = KeyCode()


def bt_show(once_click, os_name, bt):
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
