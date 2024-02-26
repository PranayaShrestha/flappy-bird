# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 21:00:34 2021

@author: Pranaya
"""

import pygame 
import sys
import random


def display_bird(x,y):
    SCREEN.blit(rotated_bird, (x, y))

def create_pipe():
    random_pipes = random.choice(pipes_height)
    bottom_pipe = PIPES.get_rect(midtop = (600, random_pipes))
    top_pipe = PIPES.get_rect(midbottom = (600, random_pipes-145))
    return bottom_pipe, top_pipe
    
def moving_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            SCREEN.blit(PIPES, pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPES, False, True)
            SCREEN.blit(flip_pipe, pipe)

def collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print('x')
            death_sound.play()
            game_active = False    
            return game_active
    return True
 
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_y_change * 3,1)
    return new_bird

def display_score(game_state):
    if game_state == "main_game":
        SCORE = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = SCORE.get_rect(center = (320, 80))
        SCREEN.blit(SCORE,score_rect)
    if game_state == "game_over":
        SCORE = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = SCORE.get_rect(center = (320, 480))
        SCREEN.blit(SCORE,score_rect)
        
        HIGH_SCORE = game_font.render(str(int(high_score)), True,(255,255,255))
        high_score_rect = HIGH_SCORE.get_rect(center = (320, 80))
        SCREEN.blit(HIGH_SCORE,high_score_rect)
    
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.init(44100, -16,1,2048)
pygame.display.init()
pygame.font.init()
#setting the display of the window
SCREEN = pygame.display.set_mode((640,500))
game_font = pygame.font.Font('04B_19.TTF',45)

#basic game variables
BACKGROUND = pygame.image.load('background.jpg')
BIRD = pygame.image.load('bird.ico')

bird_x = 50
bird_y = 250
bird_y_change = 0

PIPES = pygame.image.load('pipe-green.png')
pipes_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipes_height = [350, 300, 280]

GAME_OVER = pygame.image.load('message.png')
GAME_OVER_rect = GAME_OVER.get_rect(center = (320,250))

flapping_sound = pygame.mixer.Sound('audio_wing.ogg')
death_sound = pygame.mixer.Sound('audio_die.ogg')

score = 0
high_score = 0

#rect dimensions of the bird 
bird_rect = BIRD.get_rect(center = (bird_x,bird_y))
           
#main
running = True
game_active = True
while running:
    
    SCREEN.fill((0,0,0)) #setting the background color
    SCREEN.blit((BACKGROUND),(0,0))
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
            sys.exit()
        
        if event.type == pygame.KEYDOWN and game_active:
            bird_y_change = -6
            flapping_sound.play()
        
        if event.type == pygame.KEYUP and game_active:
            bird_y_change = 2
        
        if event.type == SPAWNPIPE:
            pipes_list.extend(create_pipe())
            
        if event.type == pygame.KEYDOWN and game_active == False:    
            game_active = True
            pipes_list.clear()
            bird_rect.center = (50, 250)
            bird_y_change = 0
            score = 0
        
    if game_active:
        #for the image of the bird to remain in the screen
        bird_y += bird_y_change #updating the config of the bird
        if bird_y <= 0:
            bird_y = 0
        if bird_y >= 450:
            bird_y = 450
        rotated_bird = rotate_bird(BIRD)
        game_active = collision(pipes_list)
    
        #for pipes
        pipes_list = moving_pipes(pipes_list)
        draw_pipes(pipes_list)
        display_bird(bird_x, bird_y)
        
        #score
        score += 0.015
        display_score('main_game')
    else:
        SCREEN.blit(GAME_OVER,GAME_OVER_rect)
        update_score(score,high_score)
        display_score('game_over')
        
    #updating the screen after each iteration
    pygame.display.update()
                
pygame.display.quit()
pygame.quit()