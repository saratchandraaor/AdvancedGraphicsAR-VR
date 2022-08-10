from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
from PIL import Image


# glfw.init()
if not glfw.init():
    raise Exception("glfw can not be initialized!")
window = glfw.create_window(1000,1000, "Maze_Game", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")


print("init")
window = window

width = 1000
height = 1000



indices = [0,  1,  2,  2,  3,  0]
indices = np.array(indices, dtype=np.uint32)

def window_resize():
    print("resize")
    glViewport(0, 0, width, height)

def window_close():
    print("close")

    return glfw.window_should_close(window)

def clear():
    print("close")

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

def swap_buffers():
    print("swap")

    glfw.swap_buffers(window)


def terminate():
    print("terminate")

    glfw.terminate()

def open_image(type,path):
    if type == 'char':
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        return [image,img_data]
    if type == 'wall':
        image_w = Image.open(path)
        image_w = image_w.transpose(Image.FLIP_TOP_BOTTOM)
        img_data_w = image_w.convert("RGBA").tobytes()
        return [image_w,img_data_w]
    
    if type == 'mud':
        image_m = Image.open(path)
        image_m = image_m.transpose(Image.FLIP_TOP_BOTTOM)
        img_data_m = image_m.convert("RGBA").tobytes()
        return [image_m,img_data_m]

def load_shader():
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

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)

    glUseProgram(shader)
    rotation_loc = glGetUniformLocation(shader, "rotation")
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, np.identity(4))

def draw(vert, image, img_data):
    print("draw")

    glBufferData(GL_ARRAY_BUFFER, vert.nbytes, vert, GL_STATIC_DRAW)

    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(12))
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, vert.itemsize * 8, ctypes.c_void_p(24))
    

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    
    glfw.poll_events()
    
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

glfw.set_window_pos(window, 0, 0)
glfw.set_window_size_callback(window, window_resize)
glfw.make_context_current(window)