class Key:
    def __init__(self, col_pins_list, row_pins_list):
        """
        键类的构造函数。
        :param col_pins_list:
        :param row_pins_list:
        """
        self.col_pins_list = col_pins_list
        self.row_pins_list = row_pins_list
        self.keys = [
            [(0,0), (0,1), (0,2), (0,3)],
            [(1,0), (1,1), (1,2), (1,3)],
            [(2,0), (2,1), (2,2), (2,3)],
            [(3,0), (3,1), (3,2), (3,3), (3,4)]
        ]

    def show(self):
        """
        显示按键
        """
        for j, col_pin in enumerate(self.col_pins_list):
            col_pin.value(0)  # 将当前列设置为低电平
            for i, row_pin in enumerate(self.row_pins_list):
                if row_pin.value() == 0:  # 检测行引脚的状态
                    # 将当前列恢复为高电平
                    col_pin.value(1)
                    return self.keys[i][j]  # 返回按下的按键
            col_pin.value(1)  # 将当前列恢复为高电平
        return None  # 没有按键被按下

    def status(self):
        """
        显示按键状态
        """
        col_pin_set = set()
        row_pin_set = set()
        status_dict = {"col_pin": col_pin_set, "row_pin": row_pin_set}
        for j, col_pin in enumerate(self.col_pins_list):
            col_pin.value(0)  # 将当前列设置为低电平
            for i, row_pin in enumerate(self.row_pins_list):
                if row_pin.value() == 0:  # 检测行引脚的状态
                    status_dict["row_pin"].add(i)
                    status_dict["col_pin"].add(j)
            col_pin.value(1)  # 将当前列恢复为高电平
        return status_dict
