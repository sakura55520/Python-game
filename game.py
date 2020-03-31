 
# 0 - 模块区
import jieba
import os
import sys
import math
import random
import pygame
import datetime
from pygame.locals import *


class Player(object):
    def __init__(self, img, rect, speed):
        self.ful_img = img
        self.img = self.ful_img
        self.rect = rect
        self.speed = speed
        self.num = 0

    def update(self, screen, press_keys):
        if press_keys[K_a]:
            self.rect.left -= self.speed
            if self.rect.left <= 0:
                self.rect.left = 0
        if press_keys[K_d]:
            self.rect.left += self.speed
            if self.rect.right >= 250:
                self.rect.right = 250
        if press_keys[K_w]:
            self.rect.top -= self.speed
            if self.rect.top <= 0:
                  self.rect.top = 0
        if press_keys[K_s]:
            self.rect.top += self.speed
            if self.rect.bottom >= 800:
                  self.rect.bottom = 800
        self.num += 1
        if self.num % 3 == 0:
            self.num = 0
        return [(self.rect.left + self.rect.right)/2, (self.rect.top + self.rect.bottom)/2], self.img


# 主要的工作区域
if __name__ == '__main__':

    # 1 - 设置区

    # 1.1 - 窗口设置区
    white = (255, 255, 255)
    screen_width, screen_height = 1368, 800
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Python_Game")

    # 1.2 - 基础设置区
    pygame.init()

    pygame.font.init()
    
    font = pygame.font.SysFont('SimHei',32)
    start = 0
    win = 0
    running = 0

    distance = 200
    health_value = 194
    health_value_max = 194
    fin_time = 200
    start_time = datetime.datetime.now()

    rect_player = Rect(50, 50, 133, 142)
    player_speed = 2
    player_pos = []

    monsters = []
    monster_speed = 1

    wave_set = []
    wave_speed = 1.5
    wave_max = 2

    fig_path = r'C:\Users\Sakura\Desktop\pythongame\gamefile/'
    paper = pygame.image.load(fig_path + 'paper.jpg').convert_alpha()
    paper = pygame.transform.scale(paper, (1368, 800))

    wall = pygame.image.load(fig_path + 'walls.png').convert_alpha()
    wall_width = wall.get_width()
    wall_height = wall.get_height()

    player = pygame.image.load(fig_path + 'beggers.png').convert_alpha()
    player_width = player.get_width()
    player_height = player.get_height()

    waves = pygame.image.load(fig_path + 'waves.png').convert_alpha()
    sub_wave = waves.subsurface(Rect((0, 0), (waves.get_width() / 5, waves.get_height())))
    sub_wave_width = sub_wave.get_width()
    sub_wave_height = sub_wave.get_height()

    monster_img1 = pygame.image.load(fig_path + 'monster1.png').convert_alpha()
    monster_width = monster_img1.get_width()
    monster_height = monster_img1.get_height()
    monster_img = monster_img1

    health_bar_img = pygame.image.load(fig_path + "health.png")
    health_bar_height = health_bar_img.get_height()

    health_img = pygame.image.load(fig_path + "health.png")
    health_height = health_img.get_height()

    victory = pygame.image.load(fig_path + 'victory.jpg')
    victory = pygame.transform.scale(victory, (1368, 800))
    game_over = pygame.image.load(fig_path + 'game_over.jpg')
    game_over = pygame.transform.scale(game_over, (1368, 800))

    start_img = pygame.image.load(fig_path + 'start.jpg').convert_alpha()

    # 2 - 游戏区
    while not start:
        screen.fill(white)
        screen.blit(start_img, (0, 0))
        
        
        text = font.render("按空格开始游戏!",
                           True, (250, 50, 200))
        text_Rect = text.get_rect()
        text_Rect.centerx = screen.get_rect().centerx
        text_Rect.centery = screen.get_rect().centery + 200
        screen.blit(text, text_Rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    start = 1
                    running = 1
                    pygame.mixer.music.load(fig_path + "bgm.mp3")
                    pygame.mixer.music.play(1, 0.0)
                    pygame.mixer.music.set_volume(0.15)
                    start_time = datetime.datetime.now()

    PL = Player(player, rect_player, player_speed)
    # 2.2 - 游戏进行区
    while running:
        # 2.2.1 - 游戏显示区
        screen.fill(white)
        screen.blit(paper, (0, 0))
        for height in range(0, screen_height, wall_height):
            screen.blit(wall, (distance, height))

        press_keys = pygame.key.get_pressed()
        player_pos, player_img = PL.update(screen, press_keys)

        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - (player_pos[1] + player_height),
                           position[0] - (player_pos[0] + player_width))
        player_rot = pygame.transform.rotate(player_img, 360 - angle * 57.29)
        player_pos1 = (player_pos[0] - player_rot.get_rect().width / 2,
                       player_pos[1] - player_rot.get_rect().height / 2)
        screen.blit(player_rot, player_pos1)

        for wave in wave_set:
            index = 0
            vel_x = math.cos(wave[0]) * wave_speed
            vel_y = math.sin(wave[0]) * wave_speed
            wave[1] += vel_x
            wave[2] += vel_y
            if wave[1] < - sub_wave_width or wave[1] > screen_width \
                    or wave[2] < - sub_wave_height or wave[2] > screen_height:
                wave_set.pop(index)
            index += 1
            for projectile in wave_set:
                wave1 = pygame.transform.rotate(sub_wave, 360 - projectile[0] * 57.29)
                screen.blit(wave1, (projectile[1], projectile[2]))
        monster_timer = random.choice(range(200))
        if monster_timer < 1:
            monsters.append([screen_width,
                             random.randint(monster_height, screen_height - monster_height)])
        index = 0

        for monster in monsters:
            if monster[0] < - monster_width:
                monsters.pop(index)
            monster[0] -= monster_speed
            monster_rect = pygame.Rect(monster_img.get_rect())
            monster_rect.top = monster[1]
            monster_rect.left = monster[0]
            if monster_rect.left < wall_width + distance:
                health_value -= random.randint(20, 50)
                monsters.pop(index)
            index1 = 0
            for wave in wave_set:
                wave_rect = pygame.Rect(sub_wave.get_rect())
                wave_rect.left = wave[1]
                wave_rect.top = wave[2]
                # 检查两个矩形块是否交叉
                if monster_rect.colliderect(wave_rect):
                    wave_set.pop(index1)
                    try:
                        monsters.pop(index)
                    except IndexError as error:
                        print("IndexError: " + str(error))
                index1 += 1
            index += 1

        for monster in monsters:
            screen.blit(monster_img, monster)

        font = pygame.font.Font(None, 42)
        cur_time = datetime.datetime.now()
        play_time = (cur_time - start_time).seconds
        if play_time % 60 < 10:
            time_str = ":0"
        else:
            time_str = ":"
        survived_text = font.render(
            str(play_time // 60) +
            time_str +
            str(play_time % 60),
            True, (0, 0, 0)
        )
        text_Rect = survived_text.get_rect()
        text_Rect.topright = [screen_width - 5, 5]
        screen.blit(survived_text, text_Rect)

        health_bar_img = pygame.transform.scale(health_bar_img,
                                                (health_value_max, health_bar_height))
        screen.blit(health_bar_img, [0, 5])

        if health_value < 0:
            health_value = 0
        health_img = pygame.transform.smoothscale(health_img,
                                            (health_value, health_height))
        screen.blit(health_img, [0, 5])

        pygame.display.flip()

        # 2.2.2 - 游戏操作区
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and len(wave_set) < wave_max:
                position = pygame.mouse.get_pos()
                wave_set.append([math.atan2(position[1] - (player_pos1[1] + player_height),
                                            position[0] - (player_pos1[0] + player_width)),
                                 player_pos1[0], player_pos1[1]])

        if pygame.time.get_ticks() >= fin_time * 1000:
            running = 0
            win = 1
        if health_value == 0:
            running = 0
            win = 0

    while not running and start:

        pygame.mixer.music.stop()
        if win:
            screen.blit(victory, (0, 0))
            pygame.font.init()
    
            font = pygame.font.SysFont('SimHei',32)

            text = font.render("胜利 !",
                               True, (250, 50, 200))
            text_Rect = text.get_rect()
            text_Rect.centerx = screen.get_rect().centerx + 20
            text_Rect.centery = screen.get_rect().centery - 250
            screen.blit(text, text_Rect)
        if not win:
            screen.blit(game_over, (0, 0))
            
            pygame.font.init()
    
            font = pygame.font.SysFont('SimHei',32)

            text = font.render("失败 !",
                               True, (250, 50, 200))
            text_Rect = text.get_rect()
            text_Rect.centerx = screen.get_rect().centerx + 20
            text_Rect.centery = screen.get_rect().centery - 250
            screen.blit(text, text_Rect)
            
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
