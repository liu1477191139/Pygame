class Settings():
    """存储《飞机大战》的所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""

        # 屏幕设置
        self.screen_width = 450
        self.screen_height = 900

        # 背景设置：设置背景色,默认为黑色，设置为浅灰色
        self.bg_color = (230, 230, 230)

        # 飞船设置：速度为1.5，生命值为3
        self.ship_limit = 3

        # 子弹设置：这些设置创建宽3像素、高15像素的深灰色子弹。屏幕中数量最多为3。
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人设置：下落速度为10
        self.fleet_drop_speed = 10

        # 游戏节奏加速倍率
        self.speedup_scale = 1.1

        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""

        # 飞船速度为0.3，子弹速度为0.3，外星人速度为0.05
        self.ship_speed_factor = 0.3
        self.bullet_speed_factor = 0.3
        self.alien_speed_factor = 0.05

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 2

    def increase_speed(self):
        """提高速度设置和外星人点数"""

        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
