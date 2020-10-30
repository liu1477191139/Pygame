import pygame
from pygame.sprite import Sprite

"""Bullet类继承了我们从模块pygame.sprite中导入的Sprite类。
通过使用精灵（Sprite），可将游戏中相关的元素编组，进而同时操作编组中的所有元素。"""


class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    # 为创建子弹实例，需要向__init__()传递pw_settings、screen和ship实例。
    def __init__(self, pw_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""

        # 调用super()来继承Sprite。
        super().__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置（飞机尖头）
        self.rect = pygame.Rect(0, 0, pw_settings.bullet_width, pw_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        # 设置子弹颜色速度
        self.color = pw_settings.bullet_color
        self.speed_factor = pw_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""

        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor

        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""

        pygame.draw.rect(self.screen, self.color, self.rect)
