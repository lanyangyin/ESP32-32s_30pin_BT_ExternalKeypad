import math

from fonts import type_matrix


class Run:
    def __init__(self, ssd, uFont):
        """
        初始化oLED显示屏对象
        :param ssd: 显示屏对象
        """
        self.type_matrix_date = type_matrix.byte2
        self.ssd = ssd
        self.uFont = uFont

    def ssd_normal_text(self, string: str, x: int = 0, y: int = 0, color: int = 1, reverse: bool = False,
                        show: bool = False, clear: bool = False):
        """
        官方的驱动,只能英文字符
        :param color: 颜色
        :param string: 要显示的字符串
        :param x: 显示的x坐标
        :param y: 显示的y坐标
        :param reverse: 是否反色
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :return:
        """
        if clear:
            self.ssd.fill(0)
        self.ssd.text(string, x, y, color)
        if reverse:
            self.ssd.invert(1)
        if not reverse:
            self.ssd.invert(0)
        if show:
            self.ssd.show()

    def ssd_normal_pixel(self, x: int, y: int, show: bool = False, clear: bool = False):
        """
        官方的驱动,只能英文字符
        :param x: 显示的x坐标
        :param y: 显示的y坐标
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :return:
        """
        if clear:
            self.ssd.fill(0)
        self.ssd.pixel(x, y, 1)
        if show:
            self.ssd.show()

    def ssd_normal_line(self, x1: int, y1: int, x2: int, y2: int, show: bool = False, clear: bool = False):
        """
        官方的驱动,只能英文字符
        :param x1: 显示的x1坐标
        :param y1: 显示的y1坐标
        :param x2: 显示的x2坐标
        :param y2: 显示的y2坐标
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :return:
        """
        if clear:
            self.ssd.fill(0)
        self.ssd.line(x1, y1, x2, y2, 1)
        if show:
            self.ssd.show()

    def ssd_normal_rectangle(self, x: int, y: int, width: int, height: int, show: bool = False, clear: bool = False,
                             fill: bool = False):
        """
        官方的驱动,只能英文字符
        :param x: 显示的x坐标
        :param y: 显示的y坐标
        :param width: 显示的宽度
        :param height: 显示的高度
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :param fill: 是否填充
        :return:
        """
        if clear:
            self.ssd.fill(0)
        if fill:
            self.ssd.rect(x, y, width, height, 1)
        else:
            self.ssd.fill_rect(x, y, width, height, 1)
        if show:
            self.ssd.show()

    def ssd_normal_clear(self):
        """
        清空屏幕
        :return:
        """
        self.ssd.fill(0)
        self.ssd.show()

    def ssd_normal_show(self):
        """
        显示屏幕
        :return:
        """
        self.ssd.show()

    def ssd_unicode(self, string: str, x: int = 0, y: int = 0, color: int = 1, font_size: int = 16,
                    reverse: bool = False, show: bool = False, clear: bool = False, half_char: bool = False):
        """
        显示中文
        :param half_char: 英文是否半角字符
        :param reverse: 是否反色
        :param color: 颜色
        :param string: 要显示的字符串
        :param x: 显示的x坐标
        :param y: 显示的y坐标
        :param font_size: 字体大小
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :return:
        """
        self.uFont.text(display=self.ssd, string=string, x=x, y=y, color=color, font_size=font_size, reverse=reverse,
                        show=show, clear=clear, half_char=half_char)

    def ssd_type_matrix_text(self, matrix_str: str, x: int, y: int, show: bool = False, clear: bool = False,
                             reverse: bool = False, fill: bool = False):
        """
        显示type_matrix字库中的字形
        :param matrix_str: 字形的名称
        :param x: 显示的x坐标
        :param y: 显示的y坐标
        :param show: 是否立即显示
        :param clear: 是否清空屏幕
        :param reverse: 是否反色
        :param fill: 是否填充
        :return:
        """
        if clear:
            self.ssd.fill(0)
        if reverse:
            fill = True
            reverse_dict = {0: 1, 1: 0}
        else:
            reverse_dict = {0: 0, 1: 1}
        index = 0  # 初始化索引，记录当前字形数据的位置
        # 从字库中获取汉字的字体数据，包含字形的高度和宽度等信息
        font_data = self.type_matrix_date[matrix_str]
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
                    self.ssd.pixel(tx + x, ty + y, reverse_dict[int(row_bytes[tx])])
        if show:
            self.ssd.show()

    def ssd_type_matrix_width_height(self, matrix_str: str):
        """
        获取type_matrix字库中的字形的宽度和高度
        :param matrix_str: 字形的名称
        :return: 字形的宽度和高度
        """
        font_data = self.type_matrix_date[matrix_str]
        return int(font_data['width']), int(font_data['height'])
