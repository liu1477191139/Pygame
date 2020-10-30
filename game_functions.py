import sys
import random
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, pw_settings, screen, ship, bullets):
    """响应按键"""

    # 如果按下的是右箭头键，就将ship.moving_right设置为True，从而将飞船向右移动
    if event.key == pygame.K_RIGHT:
        # 修改移动标志向右移动飞船
        ship.moving_right = True

    # 如果按下的是左箭头键，就将ship.moving_left设置为True，从而将飞船向左移动
    elif event.key == pygame.K_LEFT:
        # 修改移动标志向左移动飞船
        ship.moving_left = True

    # 如果按下的是空格键，就开火
    elif event.key == pygame.K_SPACE:
        fire_bullet(pw_settings, screen, ship, bullets)

    # 如果按下的是Q键，就退出
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(pw_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""

    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < pw_settings.bullets_allowed:
        new_bullet = Bullet(pw_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""

    # 如果松开的是右箭头键，就将ship.moving_right设置为False，从而使飞船停止向右移动
    if event.key == pygame.K_RIGHT:
        # 修改移动标志停止向右移动飞船
        ship.moving_right = False
    # 如果松开的是左箭头键，就将ship.moving_left设置为False，从而使飞船停止向左移动
    elif event.key == pygame.K_LEFT:
        # 修改移动标志停止向左移动飞船
        ship.moving_left = False


def check_events(pw_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""

    for event in pygame.event.get():

        # 玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件，此时调用sys.exit()来退出游戏
        if event.type == pygame.QUIT:
            sys.exit()

        # Pygame检测到KEYDOWN事件时作出响应
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event, pw_settings, screen, ship, bullets)

        # Pygame检测到KEYUP事件时作出响应
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        # Pygame检测到MOUSEBUTTONDOWN事件时作出响应
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(pw_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(pw_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""

    # 判断鼠标位置与play_button位置是否碰撞（重叠）和游戏状态
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        pw_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(pw_settings, screen, aliens)
        ship.center_ship()


def update_screen(pw_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕
    screen.fill(pw_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()  # 绘制飞船
    aliens.draw(screen)  # 绘制外星人

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(pw_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""

    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(pw_settings, screen, stats, sb, aliens, bullets)


def check_bullet_alien_collisions(pw_settings, screen, stats, sb, aliens, bullets):
    """响应子弹和外星人的碰撞"""

    # 删除发生碰撞的子弹和外星人,collisions为字典类型
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 如果字典存在，就将得分加上一个外星人值的点数
    if collisions:

        # 遍历字典collisions，确保将消灭的每个外星人的点数都记入得分
        for aliens in collisions.values():
            stats.score += pw_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        pw_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(pw_settings, screen, aliens)


# def get_number_aliens_x(pw_settings, alien_width):
#     """计算每行可容纳多少个外星人"""
#
#     # 允许生成的外星人X轴的范围
#     available_space_x = pw_settings.screen_width - 2 * alien_width
#
#     # 确定一行可容纳多少个外星人，外星人间距为外星人宽度
#     number_aliens_x = int(available_space_x / (3 * alien_width))
#
#     return number_aliens_x


# def get_number_rows(pw_settings, ship_height, alien_height):
#     """计算屏幕可容纳多少行外星人"""
#
#     # 允许生成的外星人Y轴的范围
#     available_space_y = (pw_settings.screen_height - (9 * alien_height) - ship_height)
#
#     # 确定可容纳多少行外星人，外星人间距为外星人高度
#     number_rows = int(available_space_y / (3 * alien_height))
#
#     return number_rows


# def create_alien(pw_settings, screen, aliens, alien_number, row_number):
def create_alien(pw_settings, screen, aliens):
    """创建一个外星人并将其放在规定位置"""

    alien = Alien(pw_settings, screen)
    alien_width = alien.rect.width

    # # 确认x坐标
    # alien.x = alien_width + 3 * alien_width * alien_number

    alien.x = random.uniform(alien_width, pw_settings.screen_width - alien_width)
    alien.rect.x = alien.x

    # # 确认y坐标
    # alien.rect.y = 3 * alien.rect.height + 3 * alien.rect.height * row_number
    alien.rect.y = 3 * alien.rect.height

    aliens.add(alien)


def create_fleet(pw_settings, screen, aliens):
    """创建外星人群"""

    # # 创建一个外星人，并计算一行可容纳多少个外星人，可以容纳多少行
    # alien = Alien(pw_settings, screen)
    # number_aliens_x = get_number_aliens_x(pw_settings, alien.rect.width)
    # number_rows = get_number_rows(pw_settings, ship.rect.height, alien.rect.height)

    # # 创建外星人群
    # for row_number in range(number_rows):
    #     for alien_number in range(number_aliens_x):
    #         create_alien(pw_settings, screen, aliens, alien_number, row_number)

    create_alien(pw_settings, screen, aliens)



def check_fleet_edges(pw_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""

    # 注意是group中的每一个alien，所以遍历判断每一个alien
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(pw_settings, aliens)
            break


def change_fleet_direction(pw_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""

    # 注意是group中的每一个alien，所以遍历执行每一个alien
    # for alien in aliens.sprites():
    #     alien.rect.y += pw_settings.fleet_drop_speed
    pw_settings.fleet_direction *= -1


def update_aliens(pw_settings, screen, stats, sb, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""

    check_fleet_edges(pw_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(pw_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(pw_settings, screen, stats, sb, ship, aliens, bullets)


def check_aliens_bottom(pw_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""

    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # # 像飞船被撞到一样进行处理
            # ship_hit(pw_settings, screen, stats, sb, ship, aliens, bullets)
            # break
            # 出屏幕移除
            for alien in aliens.copy():
                if alien.rect.bottom >= 0:
                    aliens.remove(alien)


def ship_hit(pw_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:

        # 将剩余生命ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(pw_settings, screen, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
