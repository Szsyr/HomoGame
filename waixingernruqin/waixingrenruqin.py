import sys
from time import sleep
import pygame
from settings import Settings
from gamestart import GameStart
from scoreboard import Scoreboard
from button import Button
from xianbei import Xianbei
from bullet import Bullet
from gost_homo import Gost

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_heght = self.screen.get_rect().height
        pygame.display.set_caption("先辈小游戏")

        #创建一个游戏统计信息的实例
        #  并创建积分牌
        self.starts = GameStart(self)
        self.sb = Scoreboard(self)
        
        self.xianbei = Xianbei(self)
        self.bullets = pygame.sprite.Group()
        self.gosts = pygame.sprite.Group()

        self._create_fleet()

        #创建Play按钮
        self.play_button = Button(self, "Play")

        #音乐
        self.musci()


    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()

            if self.starts.game_active:
                self.xianbei.update()
                self._update_bullets()
                self._update_gosts()
                self.music_pass()

            self._update_screen()
            
    def _check_events(self):
        """相应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """玩家在单机Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.starts.game_active:
            #重置游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计信息
            self.starts.reset_start()
            self.starts.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_xianbeis()


            #清空余下的先辈和子弹
            self.gosts.empty()
            self.bullets.empty()

            #创建新先辈并居中
            self._create_fleet()
            self.xianbei.center_xianbei()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.xianbei.moving_right = True
            self.music_pass()
        elif event.key == pygame.K_LEFT:
            self.xianbei.moving_left = True
            self.music_pass()
        elif event.key == pygame.K_q:
            self._end_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.xianbei.moving_right = False
            self.music_down()
        elif event.key == pygame.K_LEFT:
            self.xianbei.moving_left = False
            self.music_down()

    def music_pass(self):
        self.settings.sound.play()

    def music_down(self):
        self.settings.sound.stop()


    def _fire_bullet(self):
        """创建一颗子弹并加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新新子弹位置并删除消失的子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_gost_collisions()

    def _check_bullet_gost_collisions(self):
        #检测是否有子弹击中先辈
        # 如果是 就删除相应的子弹和先辈
        collections = pygame.sprite.groupcollide(
            self.bullets, self.gosts, True ,True
        )
        if collections:
            for gosts in collections.values():
                self.starts.score += self.settings.gost_points * len(gosts)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.gosts:
            # 删除现有的子弹并新建一群先辈
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.starts.level += 1
            self.sb.prep_level()

    def _update_gosts(self):
        """检查是否处于边缘并
        更新先辈群中的所有先辈位置"""
        self._check_fleet_edges()
        self.gosts.update()

        #检测先辈和先辈的碰撞
        if pygame.sprite.spritecollideany(self.xianbei, self.gosts):
            self._xainbei_hit()

        #检查是否到达底端
        self._check_gosts_bottom()

    def _create_fleet(self):
        """创建先辈群"""
        #创建一个一个一个先辈，并计算一行可容纳几个
        #间距为宽度
        gost = Gost(self)
        gost_width, gost_height = gost.rect.size
        gost_width = gost.rect.width
        a_space_x = self.settings.screen_width - (2 * gost_width)
        number_gosts_x = a_space_x // (2 * gost_width)

        #计算屏幕可容纳多少先辈
        xainbei_height = self.xianbei.rect.height
        a_space_y = (self.settings.screen_heght - (3 * gost_height) - xainbei_height)
        number_rows = a_space_y // (2 * gost_height)

        for row_number in range(number_rows):
             for gost_number in range(number_gosts_x):
                self._creat_gost(gost_number, row_number)


    def _creat_gost(self, gost_number, row_number):
        """创建一个先辈并放在当前行列"""
        gost = Gost(self)
        gost_width, gost_height = gost.rect.size
        gost.x = gost_width + 2 * gost_width * gost_number
        gost.rect.x = gost.x
        gost.rect.y = gost.rect.height + 2 * gost.rect.height * row_number
        self.gosts.add(gost)

    def _check_fleet_edges(self):
        """到边缘时采取的措施"""
        for gost in self.gosts.sprites():
            if gost.check_edges():
                self._chang_fleet_direction()
                break

    def _chang_fleet_direction(self):
        """下移并改变方向"""
        for gost in self.gosts.sprites():
            gost.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.xianbei.blitme()
        for bullet in self.bullets.sprites():
            bullet.drow_bullet()
        self.gosts.draw(self.screen)

        #显示得分
        self.sb.show_score()

        #如果处于非活跃状态就绘制Play按钮
        if not self.starts.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _xainbei_hit(self):
        """响应先辈被先辈撞到"""
        if self.starts.xianbeis_left > 0:
            #将xianbei_left 减一并更新记分牌
            self.starts.xianbeis_left -= 1
            self.sb.prep_xianbeis()

            #清空余下的先辈和子弹
            self.gosts.empty()
            self.bullets.empty()

            #创建一群新先辈，并将先辈放到底部中央
            self._create_fleet()
            self.xianbei.center_xianbei()

            #暂停
            sleep(0.5)
        else:
            self.starts.game_active = False
            pygame.mouse.set_visible(True)

    def _check_gosts_bottom(self):
        """检查先辈是否到达底端"""
        screen_rect = self.screen.get_rect()
        for gost in self.gosts.sprites():
            if gost.rect.bottom >= screen_rect.bottom:
                #像先辈被撞到一样处理
                self._xainbei_hit()
                break

    def _end_game(self):
        """保存最高纪录并退出"""
        self.starts.save_high_score()
        sys.exit()

    def musci(self):
        pygame.mixer.init()
        pygame.mixer.music.load('tianlai.mp3')
        pygame.mixer.music.play(-1, 0)

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
