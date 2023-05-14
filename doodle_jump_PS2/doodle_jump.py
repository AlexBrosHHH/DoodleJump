# Подключение модулей
from pygame import *
from random import randint
import os
from datetime import datetime


# Создание главного окна
win_width = 400
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('DoodleJump!')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
clock = time.Clock()


# Подключение шрифтов
font.init()
big_font = font.Font('DoodleJump.ttf', 78)
small_font = font.Font('DoodleJump.ttf', 42)


# Класс для объектов
class GameObjects(sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Класс для главного героя
class Doodle(GameObjects):
    isJump = False
    jumpCount = 7
    gravity = 25
    img_left = transform.scale(image.load('doodle.png'), (90, 100))
    img_right = transform.flip(img_left, True, False)


    # Метод прыжка
    def jump(self):
        if self.isJump:
            self.rect.y -= self.jumpCount * 9
            self.jumpCount -= 1
            if self.jumpCount <= 0:
                self.jumpCount = 7
                self.isJump = False


    # Метод управления
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.image = self.img_right
            self.rect.x += 25
        if keys[K_a]:
            self.image = self.img_left
            self.rect.x -= 25


# Создание объектов
doodle = Doodle('doodle.png', 250, 400, 90, 100)


platform_group = sprite.Group()
p_count = 4
p_x = 220
p_y = 600


for i in range(p_count):
    platform = GameObjects('platform_green.png', p_x, p_y, 100, 30)
    p_x = randint(50, win_width - 100)
    p_y -= 200
    platform_group.add(platform)


# Игровой цикл
phase_menu = True
phase_game = False
phase_lose = False


score = 0
high_score = 0


game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
       
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and phase_menu == True:
            x, y = e.pos
            if start_button.collidepoint(x, y):
                doodle.rect.x = 150
                phase_game = True
                phase_menu = False


            if exit_button.collidepoint(x, y):
                game = False


    window.blit(background, (0, 0))
    doodle.reset()


    if phase_menu:
        doodle.rect.x = 250
        logo_text = big_font.render('Doodle Jump', True, (0, 0, 0))
        window.blit(logo_text, (30, 130))


        # Кнопка НАЧАТЬ ИГРУ
        start_button = Rect(30, 250, 250, 70)
        draw.rect(window, (199, 195, 44), start_button)
        start_text = small_font.render('Start Game', True, (0, 0, 0))
        window.blit(start_text, (40, 260))


        # Кнопка ВЫХОД
        exit_button = Rect(30, 350, 130, 70)
        draw.rect(window, (199, 195, 44), exit_button)
        exit_text = small_font.render('Exit', True, (0, 0, 0))
        window.blit(exit_text, (40, 360))


    if phase_game:
        doodle.jump()
        doodle.update()


        platform_group.draw(window)


        # Падение дудла
        if doodle.isJump == False:
            doodle.rect.y += doodle.gravity


        # Касание с платформой
        if sprite.spritecollide(doodle, platform_group, False) and doodle.isJump == False:
            doodle.isJump = True


        # Движение платформ
        if doodle.isJump == True and doodle.rect.y < 200:
            for platform in platform_group:
                platform.rect.y += doodle.jumpCount * 12
                score += 1


        # Постоянное обновление платформ
        for platform in platform_group:
            if platform.rect.y > win_height:
                platform.rect.x = randint(0, win_width - 100)
                platform.rect.y = -45


        # Перемещение через стенки
        if doodle.rect.x > win_width:
            doodle.rect.x = -90
        if doodle.rect.x < -90:
            doodle.rect.x = win_width
       


        # Очки
        score_text = small_font.render('score: ' + str(score), True, (0, 0, 0))
        window.blit(score_text, (220, 0))
       
        # Переход на финальный экран
        if doodle.rect.y >= win_height:


            # База данных очков
            if os.path.exists('score_base.txt'):
                score_base = open('score_base.txt', 'a')
                score_base.write(str(datetime.now()) + ' score:' + str(score) + '\n')
                score_base.close()
            else:
                score_base = open('score_base.txt', 'w+')
                score_base.write(str(datetime.now()) + ' score:' + str(score) + '\n')
                score_base.close()


            score_base = open('score_base.txt', 'r')
            lines = score_base.readlines()
            results = []
            for line in lines:
                result = line.split('score:')
                if len(result) == 2:
                    results.append(int(result[1][:-1]))
            score_base.close()
            high_score = max(results)


            phase_lose = True
            phase_game = False


    if phase_lose:
        # Надпись проигрыша
        lose_text = transform.rotate(big_font.render('game over!', True, (200, 0, 0)), -10)
        window.blit(lose_text, (30, 130))


        # Очки
        score_text = small_font.render('your score: ' + str(score), True, (0, 0, 0))
        window.blit(score_text, (30, 300))


        high_score_text = small_font.render('high score: ' + str(high_score), True, (0, 0, 0))
        window.blit(high_score_text, (30, 350))


        # Кнопка рестарт


        # Кнопка меню


    # Обновление дисплея
    display.update()
    clock.tick(30)

