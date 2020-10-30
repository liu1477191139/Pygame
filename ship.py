import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, pw_settings, screen):
        """初始化飞机并设置其初始位置"""

        super().__init__()
        self.screen = screen
        self.pw_settings = pw_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')

        # 使用get_rect()获取相应surface的属性rect,将表示飞机的矩形存储在self.rect中
        self.rect = self.image.get_rect()

        # 将表示屏幕的矩形存储在self.screen_rect中
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 更新飞船的center值，而不是rect
            self.center += self.pw_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.pw_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞机"""

        # 第二个参用于指定绘制位置
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""

        self.center = self.screen_rect.centerx
