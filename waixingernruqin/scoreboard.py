import pygame.font
from pygame.sprite import Group
from xianbei import Xianbei

class Scoreboard:
    """显示得分的类"""

    def __init__(self, ai_game):
        """初始化显示得分的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.starts = ai_game.starts

        #字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_xianbeis()

    def prep_score(self):
        """将得分转化为渲染图像"""
        rounded_score = round(self.starts.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分和等级, 余下的先辈数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.xianbeis.draw(self.screen)

    def prep_high_score(self):
        """将最高得分转换为渲染图像"""
        high_score = round(self.starts.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        #将最高得分放在屏幕顶端中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = self.screen_rect.top

    def check_high_score(self):
        """检查是否产生了最高得分"""
        if self.starts.score > self.starts.high_score:
            self.starts.high_score = self.starts.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = str(self.starts.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_xianbeis(self):
        """显示还剩下多少先辈"""
        self.xianbeis = Group()
        for xainbei_number in range(self.starts.xianbeis_left):
            xianbei = Xianbei(self.ai_game)
            xianbei.rect.x = 10 + xainbei_number * xianbei.rect.width
            xianbei.rect.y = 10
            self.xianbeis.add(xianbei)