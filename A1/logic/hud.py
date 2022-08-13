import OpenGL.GL as gl
import OpenGL.GLUT as glut
from OpenGL.GL import *
import OpenGL.GLUT.fonts as glf
from OpenGL.GLU import *

glut.glutInit()

def drawString(string_data):

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


while True:
    drawString("Hello")