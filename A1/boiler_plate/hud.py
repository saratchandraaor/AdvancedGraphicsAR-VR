import pygame
from pygame.locals import *
import time
import os

 
GRAY = (200, 200, 200)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BROWN = (70,30,0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1100,0)

pygame.init()

class HUD:
    def __init__(self):

        width = 200
        height = 200

        self.screen = pygame.display.set_mode((width, height))

        self.background = BROWN

    def display(self,score,health,tasks_done,total_tasks,max_time):

        time_left = int(100*(max_time - pygame.time.get_ticks()/1000))/100

        self.font = pygame.font.SysFont('didot.ttc', 36)

        if score>=500:
            self.score_img = self.font.render('Score : '+str(score), True, GREEN)
        else:
            self.score_img = self.font.render('Score : '+str(score), True, GRAY)

        if health<=400:
            self.health_img = self.font.render('Health : '+str(health), True, RED)
        else:
            self.health_img = self.font.render('Health : '+str(health), True, GRAY)

        if tasks_done==total_tasks:
            self.tasks_img = self.font.render('Tasks Done : '+str(tasks_done)+"/"+str(total_tasks), True, GREEN)
        else:
            self.tasks_img = self.font.render('Tasks Done : '+str(tasks_done)+"/"+str(total_tasks), True, GRAY)

        if time_left>=0:
            if time_left<=30:
                self.time_left_img = self.font.render('Time_Left : '+str(time_left), True, RED)
            else:
                self.time_left_img = self.font.render('Time_Left : '+str(time_left), True, GRAY)
        else:
            self.time_left_img = self.font.render('Time Up', True, RED)


        self.screen.fill(self.background)

        self.screen.blit(self.score_img, (0, 0))
        self.screen.blit(self.health_img, (0, 40))
        self.screen.blit(self.tasks_img, (0, 80))
        self.screen.blit(self.time_left_img, (0, 120))

        pygame.display.update()

        return not time_left>=0

    def quit(self):
        pygame.quit()