from random import randint
from pygame import *

win_width = 1280
win_height = 720

window = display.set_mode((win_width, win_height))
display.set_caption('Doodle jump')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
clock = time.Clock()

# Класс для объектов
class GameObjects(sprite.Sprite):
    def __init__(self, ing, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image, load(img), (width), (height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def reset(self):
    window.blit(self.image, (self.rect. x, self.rect.y))

platform = GameObjects("platform_green.png", 500, 500, 137, 42)

doodle = GameObjects("doodle.png", 500, 500, 137, 42)

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

window.blit(background, (0, 0))
platform.reset()
doodle.reset()

display.update()
clock.tick(60)