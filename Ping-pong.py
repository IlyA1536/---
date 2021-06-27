
from pygame import *
from random import randint

#фоновая музыка
mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

#подключение звуков
GOAL_sound = mixer.Sound('GOAL.wav')
hit_sound = mixer.Sound('HIT.wav')

#шрифты и надписи
font.init()
font1 = font.SysFont("Arial", 73)
win_left_text = font1.render('Выйграл левый игрок!', True, (255, 0, 0))
win_left_text2 = font1.render('SPACE для перезапуска', True, (255, 0, 0))
win_right_text = font1.render('Выйграл правый игрок!', True, (180, 0, 0))
win_right_text2 = font1.render('SPACE для перезапуска', True, (180, 0, 0))
font2 = font.SysFont("Arial", 20)
off_music = font2.render('Нажмите Р для выкл. музыки', True, (255, 0, 0))
on_music = font2.render('Нажмите O для вкл. музыки', True, (255, 0, 0))

#нам нужны такие картинки:
img_back = "background.jpg"
img_ball = "ball.png"
img_plat_right = 'plat_right.png'
img_plat_left = 'plat_left.png'

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
 
#класс правого игрока
class Player_right(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 105:
            self.rect.y += self.speed

#класс левого игрока
class Player_left(GameSprite):
    #метод для управления спрайтом клавишами клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 105:
            self.rect.y += self.speed

#класс спрайта-мяча
class Ball(GameSprite):
  	#движение мяча
    def update(self):
        speed_x
        speed_y

#Создаём окошко
win_width = 700
win_height = 500
display.set_caption("Ping-pong")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаём спрайты
left_plat = Player_left(img_plat_left, 0, 150, 30, 100, 10)
right_plat = Player_right(img_plat_right, 670, 150, 30, 100, 10)

ball = Ball(img_ball, 330, 220, 50, 50, 8)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна      
end_game = False #окончание игры

speed_x = 7
speed_y = 7

while run:
    #событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if not finish:
        ball.rect.x += speed_x 
        ball.rect.y += speed_y
        
        #обновляем фон
        window.blit(background,(0,0))
 
        #пишем текст на экране (счётчик)
        left_score_text = font2.render(str(left_score), 1, (255, 0, 0))
        window.blit(left_score_text, (350, 10))

        right_score_text = font2.render(str(right_score), 1, (255, 0, 0))
        window.blit(right_score_text, (400, 10)) 

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

        #отбивание мяча от платформ
        if sprite.collide_rect(left_plat, ball) or sprite.collide_rect(right_plat ,ball): 
            speed_x *= -1
            hit_sound.play()
            #увеличени скорости
            if speed_x <= 0:
                speed_x = speed_x + -1
                speed_y = speed_y + -1
            else:
                speed_x = speed_x + 1
                speed_y = speed_y + 1
            
        
        #отбивание мяча от верхних и нижних стенок
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1
            hit_sound.play()

        #гол левого
        if ball.rect.x < 0:
            right_score = right_score + 1
            GOAL_sound.play()
            ball = Ball(img_ball, 330, 220, 50, 50, 8)
            speed_x = -7
            speed_y = -7

        #гол правого
        if ball.rect.x > 700:
            left_score = left_score + 1
            GOAL_sound.play()
            ball = Ball(img_ball, 330, 220, 50, 50, 8)
            speed_x = 7
            speed_y = 7
        
        #условие победы левого игрока
        if left_score == 5:
            end_game = True
            window.blit(win_left_text, (40, 200))
            window.blit(win_left_text2, (10, 260))
            speed_x = 0
            speed_y = 0

        #условие победы правого игрока
        if right_score == 5:
            end_game = True
            window.blit(win_right_text, (40, 200))
            window.blit(win_right_text2, (10, 260))
            speed_x = 0
            speed_y = 0

        #перезапуск игры
        if end_game == True:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    end_game = False
                    left_score = 0
                    right_score = 0
                    ball = Ball(img_ball, 330, 220, 50, 50, 8)
                    speed_x = 7
                    speed_y = 7

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
