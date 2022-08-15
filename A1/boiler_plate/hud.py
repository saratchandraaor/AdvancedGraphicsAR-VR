import pygame
from pygame.locals import *
import time
import os

 
GRAY = (200, 200, 200)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
BROWN = (60*2.55,40*2.55,0)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

class HUD:
    def __init__(self):

        width = 240
        height = 240

        self.screen = pygame.display.set_mode((width, height))

        self.background = BROWN

    def display(self,score,health,tasks_done,total_tasks,max_time,en,caught,exited_maze,light):

        time_left = int(100*(max_time - pygame.time.get_ticks()/1000))/100

        self.font = pygame.font.SysFont('didot.ttc', 36)

        self.status_img = self.font.render('Keep Going', True, GRAY)


        if score>=500:
            self.score_img = self.font.render('Score : '+str(score), True, GREEN)
        else:
            self.score_img = self.font.render('Score : '+str(score), True, GRAY)

        if health<=400 and health>0:
            self.health_img = self.font.render('Health : '+str(health), True, RED)
        else:
            self.health_img = self.font.render('Health : '+str(health), True, GRAY)
        
        if health<=0:
            self.status_img = self.font.render('You died!', True, RED)


        if tasks_done==total_tasks:
            self.tasks_img = self.font.render('Tasks Done : '+str(tasks_done)+"/"+str(total_tasks), True, GREEN)
        else:
            self.tasks_img = self.font.render('Tasks Done : '+str(tasks_done)+"/"+str(total_tasks), True, GRAY)

        if not en:
            if time_left>=0:
                if time_left<=max_time/2:
                    self.time_left_img = self.font.render('Time_Left : '+str(time_left), True, RED)
                else:
                    self.time_left_img = self.font.render('Time_Left : '+str(time_left), True, GRAY)
        if time_left<=0:
            self.time_left_img = self.font.render('Time_Left : 0.00', True, RED)
            self.status_img = self.font.render('Time Up', True, RED)

        if caught:
            self.status_img = self.font.render('Imposter got you!!', True, RED)

        if exited_maze:
            self.status_img = self.font.render('YOU WON!!!', True, GREEN)

        if light==0:
            self.light_img = self.font.render('Lights Off', True, GRAY)
        if light==1:
            self.light_img = self.font.render('Lights On', True, GREEN)

        self.screen.fill(self.background)

        self.screen.blit(self.score_img, (0, 0))
        self.screen.blit(self.health_img, (0, 40))
        self.screen.blit(self.tasks_img, (0, 80))
        self.screen.blit(self.time_left_img, (0, 120))
        self.screen.blit(self.light_img, (0, 160))

        self.screen.blit(self.status_img, (0, 200))



        pygame.display.update()

        return not time_left>=0

    def quit(self):
        pygame.quit()