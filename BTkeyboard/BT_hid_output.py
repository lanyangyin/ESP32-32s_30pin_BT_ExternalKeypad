def OutputHidIncident(bt, once_click, os_name):
    if once_click == "新建文件夹":
        print("创建文件夹")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(0x11)
    elif once_click == "删除文件":
        print("删除文件")
        if os_name:
            bt.keyboard.set_keys(0x4C)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(0x2A)
    elif once_click == "复制":
        print("复制")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x06)
    elif once_click == "剪切":
        print("剪切")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x1B)
    elif once_click == "粘贴":
        print("粘贴")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x19)
    elif once_click == "全选":
        print("全选")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x04)
    elif once_click == "保存":
        print("保存")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x16)
    elif once_click == "另存为":
        print("另存为")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(0x16)
    elif once_click == "查找":
        print("查找")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x09)
    elif once_click == "替换":
        print("替换")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x15)
    elif once_click == "打印":
        print("打印")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x13)
    elif once_click == "返回桌面":
        print("返回桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(0x07)
        else:
            bt.keyboard.set_keys(0x44)
    elif once_click == "切换下一个桌面":
        print("切换下一个桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_gui=True)
        else:
            bt.keyboard.set_modifiers(left_control=True)
        bt.keyboard.set_keys(0x4F)
    elif once_click == "切换上一个桌面":
        print("切换上一个桌面")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_gui=True)
        else:
            bt.keyboard.set_modifiers(left_control=True)
        bt.keyboard.set_keys(0x50)
    elif once_click == "展示窗口":
        print("展示窗口")
        if os_name:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(0x2B)
        else:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(0x52)
    elif once_click == "最小化":
        print("最小化")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
            bt.keyboard.set_keys(0x2C)
            bt.keyboard.set_keys(0x11)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(0x0B)
    elif once_click == "跳转助记标签":
        print("跳转助记标签")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_alt=True)
        bt.keyboard.set_keys(0x3C)
    elif once_click == "进格":
        print("进格")
        bt.keyboard.set_keys(0x2B)
    elif once_click == "退格":
        print("退格")
        bt.keyboard.set_modifiers(left_shift=True)
        bt.keyboard.set_keys(0x2B)
    elif once_click == "撤回":
        print("撤回")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x1D)
    elif once_click == "恢复":
        print("恢复")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(0x1D)
    elif once_click == "关闭窗口":
        print("关闭窗口")
        if os_name:
            bt.keyboard.set_modifiers(left_alt=True)
            bt.keyboard.set_keys(0x3D)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
            bt.keyboard.set_keys(0x14)
    elif once_click == "注释":
        print("注释")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x38)
    elif once_click == "优化代码":
        print("优化代码")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_alt=True)
        bt.keyboard.set_keys(0x0F)
    elif once_click == "优化import":
        print("优化import")
        bt.keyboard.set_modifiers(left_control=True, left_alt=True)
        bt.keyboard.set_keys(0x12)
    elif once_click == "光标末移":
        print("光标末移")
        bt.keyboard.set_modifiers(left_alt=True, left_shift=True)
        bt.keyboard.set_keys(0x0A)
    elif once_click == "连接行":
        print("连接行")
        bt.keyboard.set_modifiers(left_alt=True, left_shift=True)
        bt.keyboard.set_keys(0x0D)
    elif once_click == "ps画笔直径减":
        print("ps画笔直径减")
        bt.keyboard.set_keys(0x2F)
    elif once_click == "ps画笔直径加":
        print("ps画笔直径加")
        bt.keyboard.set_keys(0x30)
    elif once_click == "ps缩放减":
        print("ps缩放减")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True)
        bt.keyboard.set_keys(0x2D)
    elif once_click == "ps缩放加":
        print("ps缩放加")
        if os_name:
            bt.keyboard.set_modifiers(left_control=True, left_shift=True)
        else:
            bt.keyboard.set_modifiers(left_gui=True, left_shift=True)
        bt.keyboard.set_keys(0x2E)
    else:
        bt.keyboard.set_keys(once_click)
    bt.keyboard.notify_hid_report()
    bt.keyboard.set_modifiers()
    bt.keyboard.set_keys()
    bt.keyboard.notify_hid_report()
