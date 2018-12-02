import pygame
from pygame.locals import *
import random, sys
import time
import Pyro4

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

nome = input("Nome Do Jogador: ")

#Definido cores
Verde = (50,205,153)
Branco = (255,255,255)
pygame.init()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

Pontos = 0

#Conectando com o Servidor
ns = Pyro4.locateNS()
uri = ns.lookup('Obj')
Remoto = Pyro4.Proxy(uri)

#Definindo Largura e Altura da Tela do jogo
tela = pygame.display.set_mode((650,650))

#Nome da Janela
pygame.display.set_caption('Snake SD Versão 1.0')

#Icone da Janela
Icone = pygame.image.load("Dados\\Icone.jpg")
pygame.display.set_icon(Icone)


#Um objeto font é necessário para escrever valores na HUD do jogo
fonte = pygame.font.SysFont("arial", 30)

#Desenhar a HUD
score = fonte.render ("", True, (255, 255, 255))
Jogador = fonte.render ("Jogador: "+nome, True, (255, 255, 255))

Comida = pygame.image.load("Dados\\Comida.png")
Comida = pygame.transform.scale(Comida, (10,10))
Pos_Comida = Remoto.Pos_Aleatoria()

snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((255,255,255))

my_direction = LEFT
clock = pygame.time.Clock()
sair = False

while sair != True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sair = True

        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT

    if collision(snake[0],Pos_Comida):
        Pos_Comida = Remoto.Pos_Aleatoria()
        snake.append((0,0))
        Pontos += 5
        pygame.mixer.music.load("Dados\\Efeito.mp3")
        pygame.mixer.music.play()
        
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    #Atualizando as informações na Tela
    tela.fill(Verde)
    score = fonte.render ("Score: " + str(Pontos), True, (255, 255, 255))
    tela.blit(score,(15,5))
    tela.blit(Jogador,(365,5))
    tela.blit(Comida,Pos_Comida)
    for pos in snake:
     tela.blit(snake_skin,pos)
     
    pygame.display.update()




