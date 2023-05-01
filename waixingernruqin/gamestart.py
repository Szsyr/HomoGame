class GameStart:
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.read_high_score()
        self.reset_start()

        #游戏刚启动时处于非活跃状态
        self.game_active = False
    def reset_start(self):
        """游戏运行期间可能变化的信息统计"""
        self.xianbeis_left = self.settings.xianbei_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        """将最高分保存在high_score中"""
        high_score_str = str(self.high_score)
        filename = 'score.txt'
        with open(filename, 'w') as file_object:
            file_object.write(high_score_str)

    def read_high_score(self):
        """
        读取最高分
        没有就为0
        """
        filename = 'score.txt'
        try:
            with open(filename) as file_object:
                contents = file_object.read()
                self.high_score = int(contents)
        except FileNotFoundError:
            self.high_score = 0