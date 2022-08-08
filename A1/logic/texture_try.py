from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
import pyrr
from PIL import Image
from time import sleep
from OpenGL.GLUT import *
from OpenGL.GLU import *
import keyboard
from random import randint



VAO = glGenVertexArrays(1)
glBindVertexArray(VAO)


l = -0.5
h = 0.5

vertices = [l, l,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
             h, l,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
             h,  h,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
            l,  h,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]

indices = [0,  1,  2,  2,  3,  0,
           4,  5,  6,  6,  7,  4,
           8,  9, 10, 10, 11,  8,
          12, 13, 14, 14, 15, 12,
          16, 17, 18, 18, 19, 16,
          20, 21, 22, 22, 23, 20]


vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
layout(location = 2) in vec2 a_texture;
uniform mat4 rotation;
out vec3 v_color;
out vec2 v_texture;
void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
    v_texture = a_texture;
    
    //v_texture = 1 - a_texture;                      // Flips the texture vertically and horizontally
    //v_texture = vec2(a_texture.s, 1 - a_texture.t); // Flips the texture vertically
}
"""

fragment_src = """
# version 330
in vec3 v_color;
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture); // * vec4(v_color, 1.0f);
}
"""


vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))





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



VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))

glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(24))

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)



image = Image.open("/home/ysk/Documents/SMAI ASSIGNMENT_1/A1/logic/rect.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rotation_loc = glGetUniformLocation(shader, "rotation")


if not glfw.init():
    raise Exception("glfw can not be initialized!")


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


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
    
    print(all_walls)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        glLoadIdentity()                                   
        refresh2d(width, height)                     
    
        ############ Keyboard control
        cc = check_collision()

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



        vertices = [l, l,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
                h, l,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
                h,  h,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
                l,  h,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]


        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
            
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(24))

        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, np.identity(4))

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

        h -= 0.05
        l+=0.05

        sleep(0.05) 



glutInit()                                             
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      
glutInitWindowPosition(0, 0)                           
# window = glutCreateWindow("Maze_Game") 
window = glfw.create_window(1000,1000, "My OpenGL window", None, None)

# if not window:
#     glfw.terminate()
#     raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 0, 0)
glfw.set_window_size_callback(window, window_resize)
glfw.make_context_current(window)

glutDisplayFunc(run)                                  
glutIdleFunc(run)   


glutMainLoop()     

glfw.terminate()