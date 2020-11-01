import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard





def run_game():

    # 初始化游戏并创建一个屏幕对象：初始化背景设置,让Pygame能够正确地工作

    pygame.init()

    # 初始化全部音频，并加载爆炸声音乐

    pygame.mixer.init()

    # 爆炸声

    explode_sound = pygame.mixer.Sound("sound\EXPLO6.wav")

    # 子弹射击的声音

    bullet_sound = pygame.mixer.Sound("sound\shot1.wav")



    pw_settings = Settings()

    """实参(1200, 800)是一个元组，指定了游戏窗口的尺寸。

            通过将这些尺寸值传递给pygame.display.set_mode()

            我们创建了一个宽1200像素、高800像素的游戏窗口"""

    """调用pygame.display.set_mode()来创建一个名为screen的显示窗口，

    这个游戏的所有图形元素都将在其中绘制。每个元素（如外星人或飞船）都是一个surface对象"""

    screen = pygame.display.set_mode((pw_settings.screen_width, pw_settings.screen_height))



    # 窗口标题

    pygame.display.set_caption('Plane War')



    # 创建Play按钮

    play_button = Button(pw_settings, screen, "Play")



    # 创建一个用于存储游戏统计信息的实例，并创建记分牌

    stats = GameStats(pw_settings)

    sb = Scoreboard(pw_settings, screen, stats)



    # 创建一艘飞船、一个子弹编组和一个外星人编组



    # 创建一艘飞船

    ship = Ship(pw_settings, screen)



    # 创建一个用于存储子弹的编组，添加进去实例后对bullets调用 就能对bullets里面的每个bullet调用

    bullets = Group()



    # 创建一个外星人编组

    aliens = Group()



    # 创建外星人群

    gf.create_fleet(pw_settings, screen, aliens)



    timer = 1



    # 开始游戏的主循环

    while True:

        timer += 1

        gf.check_events(pw_settings, screen, stats, sb, play_button, ship, aliens, bullets, bullet_sound)

        if stats.game_active:

            ship.update()

            gf.update_bullets(pw_settings, screen, stats, sb, ship, aliens, bullets, explode_sound)

            gf.update_aliens(pw_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(pw_settings, screen, stats, sb, ship, aliens, bullets, play_button)





run_game()