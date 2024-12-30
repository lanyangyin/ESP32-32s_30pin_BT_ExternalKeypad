import time


def create_tone_list(current_tone_list: list, speed_list: list, breath_list: list):
    """
    根据当前提示音列表，速度列表，呼吸列表生成乐谱
    :param current_tone_list: 当前提示音列表
    :param speed_list: 速度列表
    :param breath_list: 呼吸列表
    :return: 乐谱
    """
    # 音乐列表
    music = [(d, s, u) for d, s, u in zip(current_tone_list, speed_list, breath_list)]  # 音调，速度，呼吸
    return music


class Buzzer:
    def __init__(self, PWM, current_tone='C'):
        self.PWM = PWM
        self.current_tones_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
        self.current_tone_index = self.current_tones_index[current_tone]  # 当前提示音的音调索引
        self.tone_list = {
            0: {-1: 221, -2: 248, -3: 278, -4: 294, -5: 330, -6: 371, -7: 416, 1: 441, 2: 495, 3: 556, 4: 589, 5: 661,
                6: 742, 7: 833, 11: 882, 12: 990, 13: 1112, 14: 1178, 15: 1322, 16: 1484, 17: 1665, 0: 0},
            1: {11: 248, 12: 278, 13: 294, 14: 330, 15: 371, 16: 416, 17: 467, 1: 495, 2: 556, 3: 624, 4: 661, 5: 742,
                6: 833, 7: 935, -1: 990, -2: 1112, -3: 1178, -4: 1322, -5: 1484, -6: 1665, -7: 1869, 0: 0},
            2: {-1: 131, -2: 147, -3: 165, -4: 175, -5: 196, -6: 221, -7: 248, 1: 262, 2: 294, 3: 330, 4: 350, 5: 393,
                6: 441, 7: 495, 11: 525, 12: 589, 13: 661, 14: 700, 15: 786, 16: 882, 17: 990, 0: 0},
            3: {11: 147, 12: 165, 13: 175, 14: 196, 15: 221, 16: 248, 17: 278, 1: 294, 2: 330, 3: 350, 4: 393, 5: 441,
                6: 495, 7: 556, -1: 589, -2: 661, -3: 700, -4: 786, -5: 882, -6: 990, -7: 1112, 0: 0},
            4: {11: 165, 12: 175, 13: 196, 14: 221, 15: 234, 16: 262, 17: 294, 1: 330, 2: 350, 3: 393, 4: 441, 5: 495,
                6: 556, 7: 624, -1: 661, -2: 700, -3: 786, -4: 882, -5: 990, -6: 1112, -7: 1248, 0: 0},
            5: {11: 175, 12: 196, 13: 221, 14: 234, 15: 262, 16: 294, 17: 330, 1: 350, 2: 393, 3: 441, 4: 465, 5: 556,
                6: 624, 7: 661, -1: 700, -2: 786, -3: 882, -4: 935, -5: 1049, -6: 1178, -7: 1322, 0: 0},
            6: {11: 196, 12: 221, 13: 234, 14: 262, 15: 294, 16: 330, 17: 371, 1: 393, 2: 441, 3: 495, 4: 556, 5: 624,
                6: 661, 7: 742, -1: 786, -2: 882, -3: 990, -4: 1049, -5: 1178, -6: 1322, -7: 1484, 0: 0}
        }

    def music(self, music_list):
        """
        播放音乐
        :param music_list: 音乐列表
        :param tone: 音调
        :return:
        """
        for current_tone, speed, breath in music_list:
            self.music_play(current_tone, speed, breath)

    def music_play(self, current_tone: int, speed: int, breath: bool, current_tone_change: int = 0):
        """
        播放提示音
        :param current_tone: 音调，-1到17
        :param speed: 速度,几分音符
        :param breath: 是否呼吸，True为呼吸，False为不呼吸
        :param current_tone_change: 大调变化，范围为-1和1，0表示不变化，正数表示升高，负数表示降低
        """
        tones = self.tone_list[self.current_tone_index + current_tone_change]  # 选择音调
        self.PWM.duty(900)  # 设置占空比为900，即0.875占空比
        self.PWM.freq(tones[current_tone])  # 设置频率
        time.sleep_ms(int(500 / speed))  # 延时
        if breath:  # 呼吸
            self.PWM.duty(0)
            time.sleep_ms(10)

    def play(self, i, tone: str = "C"):
        """
        播放音符
        :param i: 音符
        :param tone: 音调
        :return:
        """
        if i == 0:
            self.PWM.duty(0)
            self.PWM.freq(40000000)
        else:
            self.PWM.duty(900)
            self.PWM.freq(self.tone_list[self.current_tones_index[tone]][i])

    def stop_tone(self):
        """
        停止提示音
        """
        self.PWM.duty(0)
        self.PWM.freq(0)
