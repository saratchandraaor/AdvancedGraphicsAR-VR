from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
import pyrr
from PIL import Image
from time import sleep, process_time
import keyboard


from maps import generate_walls

window_height = 1000
window_width = 1000

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

def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def draw(vert, indices, image, img_data):
    dd = process_time()
    # vert = np.array(vert, dtype=np.float32)
    
    # shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    # VBO = glGenBuffers(1)
    # glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vert.nbytes, vert, GL_STATIC_DRAW)
    # EBO = glGenBuffers(1)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(24))
    

    

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    rotation_loc = glGetUniformLocation(shader, "rotation")

    glfw.poll_events()
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, np.identity(4))
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)



def check_collision():
    kk = process_time()
    global wall_coords
    global char_x
    global char_y
    global char_height
    global char_width

    fl = 0

    for i in wall_coords:

        wx1 = i[0]
        wy1 = i[1]

        w_width = i[2]
        w_height = i[3]

        px1 = char_x
        py1 = char_y

        wx = wx1+w_width/2
        wy = wy1+w_height/2

        px = px1+char_width/2
        py = py1+char_height/2

        dx = wx-px
        dy = wy-py
        
        ret = []

        if dx>0 and abs(dx)<= (w_width+char_width)/2 and abs(dy) <= (w_height+char_height)/2:
            fl = 1
            ret.append('d')
        
        if dx<=0 and abs(dx)<= (w_width+char_width)/2 and abs(dy) <= (w_height+char_height)/2:
            fl = 1
            ret.append('a')

        if dy<=0 and abs(dx)<= (w_width+char_width)/2 and abs(dy) <= (w_height+char_height)/2:
            fl = 1
            ret.append('s')
        
        if dy>0 and abs(dx)<= (w_width+char_width)/2 and abs(dy) <= (w_height+char_height)/2:
            fl = 1
            ret.append('w')
        if fl == 1:
            break

    return ret

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(window_width,window_height, "Maze_Game", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 0, 0)
glfw.set_window_size_callback(window, window_resize)
glfw.make_context_current(window)


char_height = window_height/15
char_width = window_width/15

char_x = window_width/2
char_y = window_height/2

vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 1.0 ,
             (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  0.0, 0.0,
             (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0, 1.0, 0.0, 
             2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0, 1.0, 1.0]

indices = [0,  1,  2,  2,  3,  0]

indices = np.array(indices, dtype=np.uint32)

image = Image.open("/home/ysk/Documents/SMAI ASSIGNMENT_1/A1/logic/char.png")
image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()

image_w = Image.open("/home/ysk/Documents/SMAI ASSIGNMENT_1/A1/logic/wall.JPG")
image_w = image_w.transpose(Image.FLIP_TOP_BOTTOM)
img_data_w = image_w.convert("RGBA").tobytes()

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


wall_coords= []
wall_width = window_width/20
wall_height = window_height/20

# wall_coords.append([500,500,100,100])

wall_coords = generate_walls(width=window_width,height=window_height,w_width=wall_width,w_height=wall_height)

wall_v = []

for i in wall_coords:
    wall_vertices = []
    wall_vertices.append(2*i[0]/window_width-1)
    wall_vertices.append(2*i[1]/window_height-1)
    wall_vertices.append(0)

    wall_vertices.append(1)
    wall_vertices.append(0)
    wall_vertices.append(0)

    wall_vertices.append(0)
    wall_vertices.append(0)
##
    wall_vertices.append((2*i[0]+2*i[2])/window_width-1)
    wall_vertices.append(2*i[1]/window_height-1)
    wall_vertices.append(0)

    wall_vertices.append(0)
    wall_vertices.append(1)
    wall_vertices.append(0)

    wall_vertices.append(1)
    wall_vertices.append(0)
##
    wall_vertices.append((2*i[0]+2*i[2])/window_width-1)
    wall_vertices.append((2*i[1]+2*i[3])/window_height-1)
    wall_vertices.append(0)

    wall_vertices.append(0)
    wall_vertices.append(0)
    wall_vertices.append(1)

    wall_vertices.append(1)
    wall_vertices.append(1)
##
    wall_vertices.append(2*i[0]/window_width-1)
    wall_vertices.append((2*i[1]+2*i[3])/window_height-1)
    wall_vertices.append(0)

    wall_vertices.append(1)
    wall_vertices.append(1)
    wall_vertices.append(1)

    wall_vertices.append(0)
    wall_vertices.append(1)

    wall_v.append(wall_vertices)

wall_vertices = wall_v


# wall_vertices = np.array(wall_vertices, dtype=np.float32)

# image = image.transpose(Image.FLIP_TOP_BOTTOM)
img_data = image.convert("RGBA").tobytes()

wall_vertices = [np.array(i,dtype=np.float32) for i in wall_vertices]


shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)


while not glfw.window_should_close(window):
        
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
             (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
             (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
             2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]
    
    vertices = np.array(vertices,dtype=np.float32)
    draw(vertices,indices, image, img_data)

    for i in wall_vertices:
        draw(vert= i,indices=indices,image=image_w,img_data=img_data_w)

#Keyboard_control
    cc = check_collision()
    sp = 20
    if keyboard.is_pressed("d"):
        if not 'd' in cc:
            char_x+=sp
        else:
            char_x-=sp*1.2
    if keyboard.is_pressed("a"):
        if not 'a' in cc:
            char_x-=sp
        else:
            char_x+=sp*1.2

    if keyboard.is_pressed("w"):
        if not 'w' in cc:
            char_y+=sp       
        else:
            char_y-=sp*1.2

    if keyboard.is_pressed("s"):
        if not 's' in cc:
            char_y-=sp
        else:
            char_y+=sp*1.2

    # wall_vertices = np.array(wall_vertices,dtype=np.float32)
    # draw(wall_vertices,indices,image_w,img_data_w)
 
    glfw.swap_buffers(window)

glfw.terminate()