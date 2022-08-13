from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
from PIL import Image
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GLUT.fonts
import OpenGL.GLUT as glut
import OpenGL.GLUT.fonts as glf
import OpenGL.GL as gl


if not glfw.init():
    raise Exception("glfw can not be initialized!")
window = glfw.create_window(1000,1000, "Maze_Game", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")


glut.glutInit()


class DrawTool:
    
    def __init__(self,width,height):
        self.window = window
        
        self.width = width
        self.height = height

        glfw.set_window_pos(self.window, 0, 0)
        glfw.set_window_size_callback(self.window, self.window_resize)
        glfw.make_context_current(self.window)

        self.indices = [0,  1,  2,  2,  3,  0]
        self.indices = np.array(self.indices, dtype=np.uint32)

        self.fragment_src_default = """
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

    def drawString(self,string_data):

        width = 1000
        height = 1000
        line_height = 200
        _font =  glf.GLUT_BITMAP_9_BY_15
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glOrtho(0, width, 0, height, -1, 1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor3f(1, 0, 0)

        pos = 20
        gl.glRasterPos2i(10, height - pos)

        for ch in string_data:
            if ch == '\n':
                pos = pos + line_height
                gl.glRasterPos2i(10, height - pos)
            else:
                glut.glutBitmapCharacter(_font, ord(ch))

        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()



    def window_resize(self):
        glViewport(0, 0, self.width, self.height)

    def window_close(self):

        return glfw.window_should_close(self.window)

    def clear(self):

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def swap_buffers(self):

        glfw.swap_buffers(self.window)


    def terminate(self):

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
    
        if type == 'button':
            self.image_b = Image.open(path)
            self.image_b = self.image_b.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_b = self.image_b.convert("RGBA").tobytes()
            return [self.image_b,self.img_data_b]

        if type == 'enemy':
            self.image_e = Image.open(path)
            self.image_e = self.image_e.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_e = self.image_e.convert("RGBA").tobytes()
            return [self.image_e,self.img_data_e]

        if type == 'task':
            self.image_t = Image.open(path)
            self.image_t = self.image_t.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_t = self.image_t.convert("RGBA").tobytes()
            return [self.image_t,self.img_data_t]

        if type == 'obstacle':
            self.image_o = Image.open(path)
            self.image_o = self.image_o.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_o = self.image_o.convert("RGBA").tobytes()
            return [self.image_o,self.img_data_o]

        if type == 'exit':
            self.image_exit = Image.open(path)
            self.image_exit = self.image_exit.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_exit = self.image_exit.convert("RGBA").tobytes()
            return [self.image_exit,self.img_data_exit]

        if type == 'gameover':
            self.image_gameover = Image.open(path)
            self.image_gameover = self.image_gameover.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_gameover = self.image_gameover.convert("RGBA").tobytes()
            return [self.image_gameover,self.img_data_gameover]

        if type == 'powerup':
            self.image_p = Image.open(path)
            self.image_p = self.image_p.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_p = self.image_p.convert("RGBA").tobytes()
            return [self.image_p,self.img_data_p]

        if type == 'pbutton':
            self.image_pb = Image.open(path)
            self.image_pb = self.image_pb.transpose(Image.FLIP_TOP_BOTTOM)
            self.img_data_pb = self.image_pb.convert("RGBA").tobytes()
            return [self.image_pb,self.img_data_pb]




    def load_shader(self,fragment_src):
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
        # self.fragment_src = """
        # # version 330
        # in vec3 v_color;
        # in vec2 v_texture;
        # out vec4 out_color;
        # uniform sampler2D s_texture;
        # void main()
        # {
        #     out_color = texture(s_texture, v_texture)/1; // * vec4(v_color, 1.0f);
        # }
        # """
        self.fragment_src = fragment_src 

        self.shader = compileProgram(compileShader(self.vertex_src, GL_VERTEX_SHADER), compileShader(self.fragment_src, GL_FRAGMENT_SHADER))
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)

        glUseProgram(self.shader)
        rotation_loc = glGetUniformLocation(self.shader, "rotation")
        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, np.identity(4))

    def load_texture(self):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        
    def draw(self,vert, image, img_data):

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
