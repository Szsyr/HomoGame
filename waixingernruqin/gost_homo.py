import pygame
from pygame.sprite import Sprite

class Gost(Sprite):
    """表单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载外星人图像并初始化其rect属性
        self.image = pygame.image.load('tuxianbei/xianbei.png')
        self.rect = self.image.get_rect()

        #每个先辈都初始化在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #储存先辈的精确位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果处于边缘就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动先辈"""
        self.x += (self.settings.gost_speed * self.settings.fleet_direction)
        self.rect.x = self.x

