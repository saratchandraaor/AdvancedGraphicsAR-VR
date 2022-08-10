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

class DrawTool:
    
    def __init__(self,width,height):
        print("init")
        self.window = window
        
        self.width = width
        self.height = height

        glfw.set_window_pos(self.window, 0, 0)
        glfw.set_window_size_callback(self.window, self.window_resize)
        glfw.make_context_current(self.window)

        self.indices = [0,  1,  2,  2,  3,  0]
        self.indices = np.array(self.indices, dtype=np.uint32)

    def window_resize(self):
        print("resize")
        glViewport(0, 0, self.width, self.height)

    def window_close(self):
        print("close")

        return glfw.window_should_close(self.window)

    def clear(self):
        print("close")

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def swap_buffers(self):
        print("swap")

        glfw.swap_buffers(self.window)


    def terminate(self):
        print("terminate")

        glfw.terminate()

    def open_image(self,type,path):
        if type == 'char':
            self.image = Image.open(path)
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data = self.image.convert("RGBA").tobytes()
            return [self.image,self.img_data]
        if type == 'wall':
            self.image_w = Image.open(path)
            self.image_w = self.image_w.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_w = self.image_w.convert("RGBA").tobytes()
            return [self.image_w,self.img_data_w]
        
        if type == 'mud':
            self.image_m = Image.open(path)
            self.image_m = self.image_m.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_m = self.image_m.convert("RGBA").tobytes()
            return [self.image_m,self.img_data_m]
    
    def load_shader(self):
        self.vertex_src = """
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
        ##chande out_color for illumination
        self.fragment_src = """
        # version 330
        in vec3 v_color;
        in vec2 v_texture;
        out vec4 out_color;
        uniform sampler2D s_texture;
        void main()
        {
            out_color = texture(s_texture, v_texture)/1; // * vec4(v_color, 1.0f);
        }
        """

        self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)

        glUseProgram(self.shader)
        rotation_loc = glGetUniformLocation(self.shader, "rotation")
        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, np.identity(4))
    
    def draw(self,vert, image, img_data):
        print("draw")

        glBufferData(GL_ARRAY_BUFFER, vert.nbytes, vert, GL_STATIC_DRAW)

        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
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
        
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
