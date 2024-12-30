class Knob:
    class Click:
        def __init__(self, io_pins: dict):
            """

            :param io_pins: Pins for IO
            """
            self.io_pins = io_pins

        def status(self):
            io_pins_value = {}
            io_pins_dict = {0: 'left', 1: 'right'}
            for io_pin in self.io_pins:
                io_pins_value[io_pins_dict[io_pin]] = self.io_pins[io_pin].value()
            return io_pins_value

    class Rotate:
        def __init__(self, L_io_pins: dict, R_io_pins: dict):
            """

            :param L_io_pins: Pins for IO of left column
            :param R_io_pins: Pins for IO of right column
            """
            self.L_io_pins = L_io_pins
            self.R_io_pins = R_io_pins
            self.clockwise_basics = {0: (0, 0), 1: (0, 1)}
            self.anticlockwise_basics = {0: (0, 0), 1: (1, 0)}
            self.clockwise = {0: (0, 0), 1: (0, 1), 2: (1, 1), 3: (1, 0)}
            self.anticlockwise = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}

        def l_status(self):
            """
            左旋扭左右引脚状态
            :return:
            """
            return self.L_io_pins[0].value(), self.L_io_pins[1].value()

        def r_status(self):
            """
            右旋扭左右引脚状态
            :return:
            """
            return self.R_io_pins[0].value(), self.R_io_pins[1].value()

        def l_rotate_basics(self):
            """
            左旋转基础函数
            :return: 1 顺时针 -1 逆时针 0 停止
            """
            p = {0: (0, 0), 1: (0, 0)}
            nt = self.l_status()
            p[0] = p[1]
            p[1] = nt
            if p == self.clockwise_basics:  # 顺时针
                return 1
            elif p == self.anticlockwise_basics:  # 逆时针
                return -1
            return 0

        def r_rotate_basics(self):
            p = {0: (0, 0), 1: (0, 0)}
            nt = self.r_status()
            p[0] = p[1]
            p[1] = nt
            if p == self.clockwise_basics:  # 顺时针
                return 1
            elif p == self.anticlockwise_basics:  # 逆时针
                return -1
            return 0

        def l_rotate(self):
            p = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            nt = self.l_status()
            while nt == (0, 0):
                nt = self.l_status()
                while nt != (0, 0):
                    nt = self.l_status()
                    if nt != p[3]:
                        p[0] = p[1]
                        p[1] = p[2]
                        p[2] = p[3]
                        p[3] = nt
                    if p == self.clockwise:  # 顺时针
                        return 1
                    elif p == self.anticlockwise:  # 逆时针
                        return -1

        def r_rotate(self):
            p = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            nt = self.r_status()
            while nt == (0, 0):
                nt = self.r_status()
                while nt != (0, 0):
                    nt = self.r_status()
                    if nt != p[3]:
                        p[0] = p[1]
                        p[1] = p[2]
                        p[2] = p[3]
                        p[3] = nt
                    if p == self.clockwise:  # 顺时针
                        return 1
                    elif p == self.anticlockwise:  # 逆时针
                        return -1

        def all_rotate(self):
            rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
            rnt = self.r_status()
            lnt = self.l_status()
            while rnt == (0, 0) and lnt == (0, 0):
                rnt = self.r_status()
                lnt = self.l_status()
                while rnt != (0, 0) or lnt != (0, 0):
                    if rnt != (0, 0):
                        rnt = self.r_status()
                        if rnt != rp[3]:
                            rp[0] = rp[1]
                            rp[1] = rp[2]
                            rp[2] = rp[3]
                            rp[3] = rnt
                        if rp == self.clockwise:  # 顺时针
                            rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                            return 0, 1
                        elif rp == self.anticlockwise:  # 逆时针
                            rp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                            return 0, -1
                    if lnt != (0, 0):
                        lnt = self.l_status()
                        if lnt != lp[3]:
                            lp[0] = lp[1]
                            lp[1] = lp[2]
                            lp[2] = lp[3]
                            lp[3] = lnt
                        if lp == self.clockwise:  # 顺时针
                            lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                            return 1, 0
                        elif lp == self.anticlockwise:  # 逆时针
                            lp = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0)}
                            return -1, 0

