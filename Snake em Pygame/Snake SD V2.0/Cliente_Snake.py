import pygame
from pygame.locals import *
import random, sys
import time
import Pyro4

def colisao(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

nome = input("Nome Do Jogador: ")

#Definido cores
Verde = (50,205,153)
Branco = (255,255,255)
Preto = (0,0,0)

#Inciando o Pygame
pygame.init()

#Definindo Posições
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

#Zerando a váriavel Pontos para iniciar o jogo
Pontos = 0

#Conectando com o Servidor
ns = Pyro4.locateNS()
uri = ns.lookup('Obj')
Remoto = Pyro4.Proxy(uri)

#Definindo Largura e Altura da Tela do jogo
tela = pygame.display.set_mode((650,750))

#Nome da Janela
pygame.display.set_caption('Snake SD Versão 2.0')

#Icone da Janela
Icone = pygame.image.load("Dados\\Icone.jpg")
pygame.display.set_icon(Icone)

#Um objeto font é necessário para escrever valores na HUD do jogo
fonte = pygame.font.SysFont("arial", 30)

#Desenhar a HUD
score = fonte.render ("", True, Branco)
PlayerNome = fonte.render (nome, True, Branco)

#Carregando a imagem de Fundo
Fundo = pygame.image.load("Dados\\Fundo.jpg")
FundoGameOver = pygame.image.load("Dados\\FundoGameOver.png")

#Carregando a imagem do icone Player
Player = pygame.image.load("Dados\\Player.png")
Player = pygame.transform.scale(Player, (40,40)) #Transformando a imagem na escala informada

#Carregando a imagem do icone Score
Iscore= pygame.image.load("Dados\\score.png")
Iscore = pygame.transform.scale(Iscore, (40,40)) #Transformando a imagem na escala informada

Comida = pygame.Surface((10,10))
Comida.fill(Verde)
Pos_Comida = Remoto.Pos_Aleatoria() #Iniciando com uma posiçãp aleatória definida pela função que se encontra no servidor

snake = [(200, 200), (210, 200), (220,200)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill(Branco)

my_direction = LEFT
clock = pygame.time.Clock()
sair = False
FimDeJogo = False

while sair != True:
    clock.tick(10)
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            break
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
                
    #Verificando a Colisao da Snake com a Comida
    if colisao(snake[0],Pos_Comida):
        Pos_Comida = Remoto.Pos_Aleatoria()
        snake.append((0,0))
        Pontos += 5
        pygame.mixer.music.load("Dados\\Efeito.mp3")
        pygame.mixer.music.play()
    
    #Verificando a Colisao da Snake com as bordas do jogo
    if snake[0][0] == 0 or snake[0][1] == 50 or snake[0][0] == 650 or snake[0][1] == 750:
        FimDeJogo = True

    #Movimentação da Snake  
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

    #Tela de Game Over   
    while FimDeJogo == True:
        tela.blit(FundoGameOver,(0,0))
        pygame.display.update()
        pygame.mixer.music.load("Dados\\GameOver.mp3")
        pygame.mixer.music.play()
        time.sleep(5)
        pygame.quit()
        break
        
    #Atualizando as informações na Tela
    tela.blit(Fundo,(0,0))
    score = fonte.render ("Score: " + str(Pontos), True, Branco)
    tela.blit(score,(50,5))
    tela.blit(Iscore,(0,5))
    tela.blit(Player,(360,5))
    tela.blit(PlayerNome,(410,5))
    tela.blit(Comida,Pos_Comida)
    for pos in snake:
       tela.blit(snake_skin,pos)
     
    pygame.display.update()




