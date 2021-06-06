
from pygame import *
from random import randint

#шрифты и надписи
font.init()
font1 = font.SysFont("Arial", 73)
win_left_text = font1.render('Выёграл левый игрок!', True, (255, 255, 255))
win_left_text2 = font1.render('SPACE для перезапуска', True, (255, 255, 255))
win_right_text = font1.render('Выйграл правый игрок!', True, (180, 0, 0))
win_right_text2 = font1.render('SPACE для перезапуска', True, (180, 0, 0))
font2 = font.SysFont("Arial", 20)
off_music = font2.render('Нажмите Р для выкл. музыки', True, (255, 0, 0))
on_music = font2.render('Нажмите O для вкл. музыки', True, (255, 0, 0))

#нам нужны такие картинки:
img_back = "background.jpg"
img_plat = "platform.png"
img_ball = "ball.png"

left_score = 0 #счёт левого игрока
right_score = 0 #счёт правого игрока

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
 
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Ping-pong")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаём спрайты
left_plat = Player(img_plat, 10, 250, 50, 200, 10)
right_plat = Player(img_plat, 600, 250, 50, 200, 10)

ball = Player(img_ball, 100, 100, 80, 80, 5)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна      
end_game = False

while run:
    #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
 
        #пишем текст на экране (счётчик)
        left_score_text = font2.render(str(left_score), 1, (255, 255, 255))
        window.blit(left_score_text, (200, 10))

        right_score_text = font2.render(str(right_score), 1, (255, 255, 255))
        window.blit(right_score_text, (250, 10)) 

        #текст вкл/выкл музыка
        window.blit(on_music, (0, 455))
        window.blit(off_music, (0, 475))
        
        #производим движения спрайтов
        left_plat.update()
        right_plat.update()
        ball.update()
 
        #обновляем их в новом местоположении при каждой итерации цикла
        left_plat.reset()
        right_plat.reset()
        ball.reset()

        #условие победы левого игрока
        if left_score == 5:
            end_game = True
            window.blit(win_left_text, (200, 200))
            window.blit(win_left_text2, (10, 250))

        #условие победы правого игрока
        if right_score == 5:
            end_game = True
            window.blit(win_right_text, (200, 200))
            window.blit(win_right_text2, (10, 250))

        #перезапуск игры
        if end_game == True:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    end_game = False
                    left_score = 0
                    right_score = 0

        #включение/выключение фоновой музыки
        if e.type == KEYDOWN:
            if e.key == K_p:
                mixer.music.pause()
                        
        if e.type == KEYDOWN:
            if e.key == K_o:
                mixer.music.unpause()

        display.update()
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)