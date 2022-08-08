from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame import image
class Player:
    def __init__(self,all_walls):
        self.all_walls = all_walls
        pass
    def player_control(self,p_x,p_y):
        pass
    def load_texture(self,img_location):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)

        im = image.load(img_location).convert()
        im_w,im_h = im.get_rect().size
        im_data = im.tostring()
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA, im_w, im_h, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.texture)

        
