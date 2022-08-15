from random import randint
import numpy as np
from time import time
from math import sqrt

class Player:
    def __init__(self,button_width,button_height,enemy_width,enemy_height):
        self.button_height = button_height
        self.button_width = button_width

        self.health = 1000
        self.tasks_total = 2
        self.tasks_done = 0
        self.score =300
        self.button_coords = [0,0,button_width,button_height]
        self.enemy_coords = [0,0,enemy_width,enemy_height]
        self.task_coords = [0,0,button_width,button_height]
        self.pbutton_coords = [0,0,button_width,button_height]
        
        self.obstacle_coords = []
        self.powerup_coords = []

        for i in range(3):
            self.obstacle_coords.append([0,0,button_width,button_height])
    
        for i in range(3):
            self.powerup_coords.append([0,0,button_width,button_height])
    
        
        self.enemy_state = True
        self.task_state = True
        self.pbutton_state = True
        self.button_state = True

        self.obstacle_state = [True,True,True]
        self.powerup_state = [False,False,False]

        self.exit = False

        self.time = 0

        self.exited_maze = False

        self.caught = False

    def get_player_stats(self):
        self.time =  time()

        return [self.health,self.score,self.tasks_done]
    
    def get_button(self,wall_coords,width,height):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)

            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.button_coords[0], self.button_coords[1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.button_coords
            button_vertices = []
            button_vertices.append(2*i[0]/width-1)
            button_vertices.append(2*i[1]/height-1)
            button_vertices.append(0)

            button_vertices.append(1)
            button_vertices.append(0)
            button_vertices.append(0)

            button_vertices.append(0)
            button_vertices.append(0)
        ##
            button_vertices.append((2*i[0]+2*i[2])/width-1)
            button_vertices.append(2*i[1]/height-1)
            button_vertices.append(0)

            button_vertices.append(0)
            button_vertices.append(1)
            button_vertices.append(0)

            button_vertices.append(1)
            button_vertices.append(0)
        ##
            button_vertices.append((2*i[0]+2*i[2])/width-1)
            button_vertices.append((2*i[1]+2*i[3])/height-1)
            button_vertices.append(0)

            button_vertices.append(0)
            button_vertices.append(0)
            button_vertices.append(1)

            button_vertices.append(1)
            button_vertices.append(1)
        ##
            button_vertices.append(2*i[0]/width-1)
            button_vertices.append((2*i[1]+2*i[3])/height-1)
            button_vertices.append(0)

            button_vertices.append(1)
            button_vertices.append(1)
            button_vertices.append(1)

            button_vertices.append(0)
            button_vertices.append(1)

            wall_v.append(button_vertices)

        button_vertices = wall_v

        button_vertices = np.array(button_vertices,dtype=np.float32)
        
        return button_vertices, self.button_coords

    def check_button_status(self,char_x,char_y,char_width,char_height,button_coords):
        if abs(char_x-button_coords[0])<=(char_width+button_coords[2])/2 and abs(char_y-button_coords[1])<=(char_height+button_coords[3])/2:
            self.enemy_state = False

    def check_health_status(self):
        if self.health <= 0:
            self.exit = True

    def check_exit_status(self,char_x,char_y,char_width,char_height,exit_coords,tasks_done):
        if abs(char_x-exit_coords[0])<=(char_width+exit_coords[2])/2 and abs(char_y-exit_coords[1])<=(char_height+exit_coords[3])/2 and tasks_done>=2:
            self.exited_maze = True
            self.exit = True

    def check_enemy_status(self,char_x,char_y,char_width,char_height,enemy_coords):
        if self.enemy_state and abs(char_x-enemy_coords[0])<=(char_width+enemy_coords[2])/2 and abs(char_y-enemy_coords[1])<=(char_height+enemy_coords[3])/2 :
            self.exit = True
            self.caught = True

    def get_enemy(self,wall_coords,width,height):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)
    
            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.enemy_coords[0], self.enemy_coords[1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.enemy_coords
            enemy_vertices = []
            enemy_vertices.append(2*i[0]/width-1)
            enemy_vertices.append(2*i[1]/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(0)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(0)
        ##
            enemy_vertices.append((2*i[0]+2*i[2])/width-1)
            enemy_vertices.append(2*i[1]/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(0)
        ##
            enemy_vertices.append((2*i[0]+2*i[2])/width-1)
            enemy_vertices.append((2*i[1]+2*i[3])/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(0)
            enemy_vertices.append(1)

            enemy_vertices.append(1)
            enemy_vertices.append(1)
        ##
            enemy_vertices.append(2*i[0]/width-1)
            enemy_vertices.append((2*i[1]+2*i[3])/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(1)
            enemy_vertices.append(1)

            enemy_vertices.append(0)
            enemy_vertices.append(1)

            wall_v.append(enemy_vertices)

        enemy_vertices = wall_v

        enemy_vertices = np.array(enemy_vertices,dtype=np.float32)
        
        return enemy_vertices, self.enemy_coords

    def get_task(self,wall_coords,width,height):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)

            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.task_coords[0], self.task_coords[1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.task_coords
            task_vertices = []
            task_vertices.append(2*i[0]/width-1)
            task_vertices.append(2*i[1]/height-1)
            task_vertices.append(0)

            task_vertices.append(1)
            task_vertices.append(0)
            task_vertices.append(0)

            task_vertices.append(0)
            task_vertices.append(0)
        ##
            task_vertices.append((2*i[0]+2*i[2])/width-1)
            task_vertices.append(2*i[1]/height-1)
            task_vertices.append(0)

            task_vertices.append(0)
            task_vertices.append(1)
            task_vertices.append(0)

            task_vertices.append(1)
            task_vertices.append(0)
        ##
            task_vertices.append((2*i[0]+2*i[2])/width-1)
            task_vertices.append((2*i[1]+2*i[3])/height-1)
            task_vertices.append(0)

            task_vertices.append(0)
            task_vertices.append(0)
            task_vertices.append(1)

            task_vertices.append(1)
            task_vertices.append(1)
        ##
            task_vertices.append(2*i[0]/width-1)
            task_vertices.append((2*i[1]+2*i[3])/height-1)
            task_vertices.append(0)

            task_vertices.append(1)
            task_vertices.append(1)
            task_vertices.append(1)

            task_vertices.append(0)
            task_vertices.append(1)

            wall_v.append(task_vertices)

        task_vertices = wall_v

        task_vertices = np.array(task_vertices,dtype=np.float32)
        
        return task_vertices, self.task_coords

    def get_pbutton(self,wall_coords,width,height):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)

            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.pbutton_coords[0], self.pbutton_coords[1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.pbutton_coords
            pbutton_vertices = []
            pbutton_vertices.append(2*i[0]/width-1)
            pbutton_vertices.append(2*i[1]/height-1)
            pbutton_vertices.append(0)

            pbutton_vertices.append(1)
            pbutton_vertices.append(0)
            pbutton_vertices.append(0)

            pbutton_vertices.append(0)
            pbutton_vertices.append(0)
        ##
            pbutton_vertices.append((2*i[0]+2*i[2])/width-1)
            pbutton_vertices.append(2*i[1]/height-1)
            pbutton_vertices.append(0)

            pbutton_vertices.append(0)
            pbutton_vertices.append(1)
            pbutton_vertices.append(0)

            pbutton_vertices.append(1)
            pbutton_vertices.append(0)
        ##
            pbutton_vertices.append((2*i[0]+2*i[2])/width-1)
            pbutton_vertices.append((2*i[1]+2*i[3])/height-1)
            pbutton_vertices.append(0)

            pbutton_vertices.append(0)
            pbutton_vertices.append(0)
            pbutton_vertices.append(1)

            pbutton_vertices.append(1)
            pbutton_vertices.append(1)
        ##
            pbutton_vertices.append(2*i[0]/width-1)
            pbutton_vertices.append((2*i[1]+2*i[3])/height-1)
            pbutton_vertices.append(0)

            pbutton_vertices.append(1)
            pbutton_vertices.append(1)
            pbutton_vertices.append(1)

            pbutton_vertices.append(0)
            pbutton_vertices.append(1)

            wall_v.append(pbutton_vertices)

        pbutton_vertices = wall_v

        pbutton_vertices = np.array(pbutton_vertices,dtype=np.float32)
        
        return pbutton_vertices, self.pbutton_coords

    def get_obstacle(self,wall_coords,width,height,ii):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)

            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.obstacle_coords[ii][0], self.obstacle_coords[ii][1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.obstacle_coords[ii]
            obstacle_vertices = []
            obstacle_vertices.append(2*i[0]/width-1)
            obstacle_vertices.append(2*i[1]/height-1)
            obstacle_vertices.append(0)

            obstacle_vertices.append(1)
            obstacle_vertices.append(0)
            obstacle_vertices.append(0)

            obstacle_vertices.append(0)
            obstacle_vertices.append(0)
        ##
            obstacle_vertices.append((2*i[0]+2*i[2])/width-1)
            obstacle_vertices.append(2*i[1]/height-1)
            obstacle_vertices.append(0)

            obstacle_vertices.append(0)
            obstacle_vertices.append(1)
            obstacle_vertices.append(0)

            obstacle_vertices.append(1)
            obstacle_vertices.append(0)
        ##
            obstacle_vertices.append((2*i[0]+2*i[2])/width-1)
            obstacle_vertices.append((2*i[1]+2*i[3])/height-1)
            obstacle_vertices.append(0)

            obstacle_vertices.append(0)
            obstacle_vertices.append(0)
            obstacle_vertices.append(1)

            obstacle_vertices.append(1)
            obstacle_vertices.append(1)
        ##
            obstacle_vertices.append(2*i[0]/width-1)
            obstacle_vertices.append((2*i[1]+2*i[3])/height-1)
            obstacle_vertices.append(0)

            obstacle_vertices.append(1)
            obstacle_vertices.append(1)
            obstacle_vertices.append(1)

            obstacle_vertices.append(0)
            obstacle_vertices.append(1)

            wall_v.append(obstacle_vertices)

        obstacle_vertices = wall_v

        # obstacle_vertices = np.array(obstacle_vertices,dtype=np.float32)
        
        return obstacle_vertices, self.obstacle_coords

    def get_powerup(self,wall_coords,width,height,ii):
        fl = 1
        while fl ==1:
            k = randint(1,9)
            j = randint(1,9)

            wall_coords_temp = []

            for i in range(len(wall_coords)):
                wall_coords_temp.append(wall_coords[i][0:2])

            if [width*k/10,height*j/10] in wall_coords_temp:
                kk = 1
            else:
                fl = 0
                self.powerup_coords[ii][0], self.powerup_coords[ii][1] = width*k/10,height*j/10

        wall_v = []
        if True:
            i = self.powerup_coords[ii]
            powerup_vertices = []
            powerup_vertices.append(2*i[0]/width-1)
            powerup_vertices.append(2*i[1]/height-1)
            powerup_vertices.append(0)

            powerup_vertices.append(1)
            powerup_vertices.append(0)
            powerup_vertices.append(0)

            powerup_vertices.append(0)
            powerup_vertices.append(0)
        ##
            powerup_vertices.append((2*i[0]+2*i[2])/width-1)
            powerup_vertices.append(2*i[1]/height-1)
            powerup_vertices.append(0)

            powerup_vertices.append(0)
            powerup_vertices.append(1)
            powerup_vertices.append(0)

            powerup_vertices.append(1)
            powerup_vertices.append(0)
        ##
            powerup_vertices.append((2*i[0]+2*i[2])/width-1)
            powerup_vertices.append((2*i[1]+2*i[3])/height-1)
            powerup_vertices.append(0)

            powerup_vertices.append(0)
            powerup_vertices.append(0)
            powerup_vertices.append(1)

            powerup_vertices.append(1)
            powerup_vertices.append(1)
        ##
            powerup_vertices.append(2*i[0]/width-1)
            powerup_vertices.append((2*i[1]+2*i[3])/height-1)
            powerup_vertices.append(0)

            powerup_vertices.append(1)
            powerup_vertices.append(1)
            powerup_vertices.append(1)

            powerup_vertices.append(0)
            powerup_vertices.append(1)

            wall_v.append(powerup_vertices)

        powerup_vertices = wall_v

        # powerup_vertices = np.array(powerup_vertices,dtype=np.float32)
        
        return powerup_vertices, self.powerup_coords

    def check_powerup_status(self,char_x,char_y,char_width,char_height,powerup_coords,i):
        if self.powerup_state[i] and abs(char_x-self.powerup_coords[i][0])<=(char_width+self.powerup_coords[i][2])/2 and abs(char_y-self.powerup_coords[i][1])<=(char_height+self.powerup_coords[i][3])/2:
            self.powerup_state[i] = False
            self.score += 400

    def check_pbutton_status(self,char_x,char_y,char_width,char_height,pbutton_coords):
        if abs(char_x-pbutton_coords[0])<=(char_width+pbutton_coords[2])/2 and abs(char_y-pbutton_coords[1])<=(char_height+pbutton_coords[3])/2:
            if self.pbutton_state:
                self.powerup_state = [True,True,True]
                self.pbutton_state = False

    def check_task_status(self,char_x,char_y,char_width,char_height,task_coords):
        if abs(char_x-task_coords[0])<=(char_width+task_coords[2])/2 and abs(char_y-task_coords[1])<=(char_height+task_coords[3])/2 and self.task_state:
            self.task_state = False
            self.tasks_done += 1

    def check_obstacle_status(self,char_x,char_y,char_width,char_height,obstacle_coords,i):
        if self.obstacle_state[i] and abs(char_x-self.obstacle_coords[i][0])<=(char_width+self.obstacle_coords[i][2])/2 and abs(char_y-self.obstacle_coords[i][1])<=(char_height+self.obstacle_coords[i][3])/2:
            self.obstacle_state[i] = False
            self.health -= 400
            self.score -= 100

    def check_collision(self,wall_coords,char_x,char_y,char_width,char_height,direction=None):

        ret = []

        for i in wall_coords:

            wx1 = i[0]
            wy1 = i[1]

            w_width = i[2]
            w_height = i[3]

            px1 = char_x
            py1 = char_y

            wx = wx1-w_width/2
            wy = wy1-w_height/2

            px = px1-char_width/2
            py = py1-char_height/2

            dx = wx-px
            dy = wy-py
            
            d = -2
            # if direction == 'd':
            if dx>0 and abs(dx)<= (w_width+char_width)/4 +d and abs(dy) <= (w_height+char_height)/2 + 2*d:
                fl = 1
                ret.append('d')
                # return True
                
            
        # if direction == 'a':
            if dx<0 and abs(dx)<= (w_width+char_width)/2+d and abs(dy) <= (w_height+char_height)/2+2*d:
                fl = 1
                ret.append('a')
                # return True
        

        # if direction == 's':
            if dy<0 and abs(dx)<= (w_width+char_width)/2 +2*d and abs(dy) <= (w_height+char_height)/2+d:
                fl = 1
                ret.append('s')
                # return True
            
        
        # if direction == 'w':
            if dy>0 and abs(dx)<= (w_width+char_width)/2 +2*d and abs(dy) <= (w_height+char_height)/4+d:
                fl = 1
                ret.append('w')
                # return True
                

        return ret

    def enemy_movement(self,char_x,char_y,enemy_width,enemy_height,lights, wall_coords=None):
        enemy_x,enemy_y = self.enemy_coords[0],self.enemy_coords[1]
        width = 1000
        height = 1000
        if lights == 0:
            sp = 4
        else:
            sp = 2

        cce = self.check_collision(wall_coords,enemy_x,enemy_y,enemy_width*2,enemy_height*2)

        try:
            dx = sp*(char_x-enemy_x)/abs(sqrt((char_x-enemy_x)**2+(char_y-enemy_y)**2))
        except:
            dx = sp*(char_x-enemy_x)/abs(sqrt((char_x-enemy_x)**2+(char_y-enemy_y)**2)+0.000001)
        
        try:
            dy = sp*(char_y-enemy_y)/abs(sqrt((char_x-enemy_x)**2+(char_y-enemy_y)**2))
        except:
            dy = sp*(char_y-enemy_y)/abs(sqrt((char_x-enemy_x)**2+(char_y-enemy_y)**2)+0.000001)


        if dx>0 and 'd' in cce:
            dx = 0

        if dx<0 and 'a' in cce:
            dx = 0
        
        if dy>0 and 'w' in cce:
            dy = 0
        
        if dy<0 and 's' in cce:
            dy = 0

        self.enemy_coords[0] =enemy_x+dx
        self.enemy_coords[1] =enemy_y+dy
        wall_v = []
        i = self.enemy_coords
        if True:
            i = self.enemy_coords
            enemy_vertices = []
            enemy_vertices.append(2*i[0]/width-1)
            enemy_vertices.append(2*i[1]/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(0)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(0)
        ##
            enemy_vertices.append((2*i[0]+2*i[2])/width-1)
            enemy_vertices.append(2*i[1]/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(0)
        ##
            enemy_vertices.append((2*i[0]+2*i[2])/width-1)
            enemy_vertices.append((2*i[1]+2*i[3])/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(0)
            enemy_vertices.append(0)
            enemy_vertices.append(1)

            enemy_vertices.append(1)
            enemy_vertices.append(1)
        ##
            enemy_vertices.append(2*i[0]/width-1)
            enemy_vertices.append((2*i[1]+2*i[3])/height-1)
            enemy_vertices.append(0)

            enemy_vertices.append(1)
            enemy_vertices.append(1)
            enemy_vertices.append(1)

            enemy_vertices.append(0)
            enemy_vertices.append(1)

            wall_v.append(enemy_vertices)

        enemy_vertices = wall_v

        enemy_vertices = np.array(enemy_vertices,dtype=np.float32)
        
        return enemy_vertices, self.enemy_coords
