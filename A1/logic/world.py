import numpy as np
from random import randint


class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def generate_walls(self,w_height,w_width):
        l0 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        l01 = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        
        l = [l01,l0]
        l = l[randint(0,1)]
        # l = l0
        wall_coords = []
        for i in range(len(l)):
            for j in range(len(l[i])):
                if l[i][j] == 1:
                    wall_coords.append([self.width*i/20,self.height*j/20,w_width,w_height])
        return wall_coords

    def check_collision(self,wall_coords,char_x,char_y,char_width,char_height,direction):

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
            if direction == 'd':
                if dx>0 and abs(dx)<= (w_width+char_width)/4 +d and abs(dy) <= (w_height+char_height)/2 + 2*d:
                    fl = 1
                    # ret.append('d')
                    return True
                
            
            if direction == 'a':
                if dx<0 and abs(dx)<= (w_width+char_width)/2+d and abs(dy) <= (w_height+char_height)/2+2*d:
                    fl = 1
                    # ret.append('a')
                    return True
            

            if direction == 's':
                if dy<0 and abs(dx)<= (w_width+char_width)/2 +2*d and abs(dy) <= (w_height+char_height)/2+d:
                    fl = 1
                    # ret.append('s')
                    return True
               
            
            if direction == 'w':
                if dy>0 and abs(dx)<= (w_width+char_width)/2 +2*d and abs(dy) <= (w_height+char_height)/4+d:
                    fl = 1
                    # ret.append('w')
                    return True
                

        return False

    def get_walls(self,wall_width,wall_height):
        wall_coords = self.generate_walls(w_width=wall_width,w_height=wall_height)

        wall_v = []

        for i in wall_coords:
            wall_vertices = []
            wall_vertices.append(2*i[0]/self.width-1)
            wall_vertices.append(2*i[1]/self.height-1)
            wall_vertices.append(0)

            wall_vertices.append(1)
            wall_vertices.append(0)
            wall_vertices.append(0)

            wall_vertices.append(0)
            wall_vertices.append(0)
        ##
            wall_vertices.append((2*i[0]+2*i[2])/self.width-1)
            wall_vertices.append(2*i[1]/self.height-1)
            wall_vertices.append(0)

            wall_vertices.append(0)
            wall_vertices.append(1)
            wall_vertices.append(0)

            wall_vertices.append(1)
            wall_vertices.append(0)
        ##
            wall_vertices.append((2*i[0]+2*i[2])/self.width-1)
            wall_vertices.append((2*i[1]+2*i[3])/self.height-1)
            wall_vertices.append(0)

            wall_vertices.append(0)
            wall_vertices.append(0)
            wall_vertices.append(1)

            wall_vertices.append(1)
            wall_vertices.append(1)
        ##
            wall_vertices.append(2*i[0]/self.width-1)
            wall_vertices.append((2*i[1]+2*i[3])/self.height-1)
            wall_vertices.append(0)

            wall_vertices.append(1)
            wall_vertices.append(1)
            wall_vertices.append(1)

            wall_vertices.append(0)
            wall_vertices.append(1)

            wall_v.append(wall_vertices)

        wall_vertices = wall_v

        wall_vertices = [np.array(i,dtype=np.float32) for i in wall_vertices]

        return wall_vertices,wall_coords

    def get_mud(self):

        mud_vertices = [-1, -1,  0.5,  1.0, 0.0, 0.0,  0.0, 0.0,
                    1, -1,  0.5,  0.0, 1.0, 0.0,  1.0, 0.0,
                    1,  1,  0.5,  0.0, 0.0, 1.0,  1.0, 1.0,
                    -1,  1,  0.5,  1.0, 1.0, 1.0,  0.0, 1.0]

        mud_vertices = np.array(mud_vertices,dtype=np.float32)

        return mud_vertices

    def illumination(self, char_x, char_y, objects):
        pass