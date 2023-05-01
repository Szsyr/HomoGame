import pygame.mixer_music


class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width = 800
        self.screen_heght = 600
        self.bg_color = (230, 230, 230)

        #先辈gost设置
        self.gost_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #加快游戏进程
        self.speedup_scal = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        #先辈设置
        self.xianbei_speed = 1.5
        self.xianbei_limit = 3

        #子弹设置
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 10

        #音效
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('nubel-1uf37.wav')

    def initialize_dynamic_settings(self):
        """初始化随游戏进程而变化的数据"""
        self.xianbei_speed = 1.5
        self.bullet_speed = 3.0
        self.gost_speed = 1.0

        #self.fleet_direction = 1 表示向右 为-1表示向左
        self.fleet_direction = 1

        #积分
        self.gost_points = 50

    def increase_speed(self):
        """提高速度设置和先辈分数"""
        self.xianbei_speed *= self.speedup_scal
        self.bullet_speed *= self.speedup_scal
        self.gost_speed *= self.speedup_scal

        self.gost_points = int(self.gost_points * self.score_scale)


