from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glm
import trimesh
import moderngl
import moderngl_window
from moderngl_window import *
import numpy as np
from pathlib import Path
from time import sleep
import keyboard
from random import randint
import cv2

from boiler_plate.basics import basics

global x1
global y1

global char_width
global char_height

global all_walls

window = 0                                           
width, height = 1000,1000

wall_width = width/10
wall_height = height/10

char_width = wall_width/5
char_height = wall_height/5

all_walls = []

x1=0
y1=0


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  
    glVertex2f(x, y)                                   
    glVertex2f(x + width, y)                           
    glVertex2f(x + width, y + height)                  
    glVertex2f(x, y + height)                          
    glEnd()  

def check_collision():
    fl = 0
    for i in all_walls:
        wx1 = i[0]
        wy1 = i[1]

        w_width = wall_width/i[2]
        w_height = wall_height/i[3]

        px1 = x1
        py1 = y1

        wx = wx1+w_width/2
        wy = wy1+w_height/2

        px = px1+char_width/2
        py = py1+char_height/2

        dx = wx-px
        dy = wy-py
        
        ret = []

        if dx>0 and abs(dx)<= (w_width+char_width)/2+1 and abs(dy) <= (w_height+char_height)/2+1:
            fl = 1
            ret.append('d')
        
        if dx<=0 and abs(dx)<= (w_width+char_width)/2+1 and abs(dy) <= (w_height+char_height)/2+1:
            fl = 1
            ret.append('a')

        if dy<=0 and abs(dx)<= (w_width+char_width)/2+1 and abs(dy) <= (w_height+char_height)/2+1:
            fl = 1
            ret.append('s')
        
        if dy>0 and abs(dx)<= (w_width+char_width)/2+1 and abs(dy) <= (w_height+char_height)/2+1:
            fl = 1
            ret.append('w')
        if fl == 1:
            break
    print(ret)
    return ret

def run():                                            
    global all_walls
    global x1
    global y1
    global char_height
    global char_width

    for i in range(10):
        for j in range(10):
            if randint(0,1) == 1:
                ki = randint(1,2)
                kj = randint(1,2)
                all_walls.append([wall_width*i,wall_height*j,ki,kj])

    # i = 5
    # j = 5
    # ki = 0.5
    # kj = 0.5
    # all_walls.append([wall_width*i,wall_height*j,ki,kj])
    
    print(all_walls)

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        glLoadIdentity()                                   
        refresh2d(width, height)                     
    
        ############ Keyboard control
        cc = check_collision()

        # print(cc)
        
        # if 'd' in cc:
        #     x1 -= 5
        # if 'a' in cc:
        #     x1 += 5
        # if 'w' in cc:
        #     y1 -= 5
        # if 's' in cc:
            # y1 += 5



        if keyboard.is_pressed("d"):
            if not 'd' in cc:
                x1+=5
            else:
                x1 -= 7
        if keyboard.is_pressed("a"):
            if not 'a' in cc :
                x1-=5
            else:
                x1+=7
        if keyboard.is_pressed("w"):
            if not 'w' in cc:
                y1+=5
            else:
                y1-=7
        if keyboard.is_pressed("s"):
            if not 's' in cc:
                y1-=5
            else:
                y1+=7
        # if keyboard.is_pressed("q"):
        #     break
            
        sleep(0.01)

        for i in all_walls:
            draw_rect(i[0],i[1],wall_width/i[2],wall_height/i[3])
        
        draw_rect(x1,y1,char_width,char_height)                        
    
        glutSwapBuffers() 



glutInit()                                             
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      
glutInitWindowPosition(0, 0)                           
window = glutCreateWindow("Maze_Game")              
glutDisplayFunc(run)                                  
glutIdleFunc(run)   

texture = moderngl.basics().load_texture_2d.texture('data/textures/uv_tex.jpg')
texture.use(0)

glutMainLoop() 


# texture_image = cv2.imread("char.png")
# texture = ctx.texture(texture_image.shape[1::-1], texture_image.shape[2], texture_image)
# texture.use(0)