import numpy as np
import keyboard

# from boiler_plate.draw import DrawTool
from draw import DrawTool
from world import World


window_height = 1000
window_width = 1000

char_height = window_height/20
char_width = window_width/20

char_x = window_width/2
char_y = window_height/2

vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 1.0 ,
             (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  0.0, 0.0,
             (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0, 1.0, 0.0, 
             2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0, 1.0, 1.0]

wall_width = window_width/20
wall_height = window_height/20

world = World(window_width,window_height)
draw_tool = DrawTool(window_width,window_height)
draw_tool.load_shader()

image,img_data = draw_tool.open_image(type='char',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/char.png')
image_w,img_data_w = draw_tool.open_image(type='wall',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/wall2.jpg')
image_m,img_data_m = draw_tool.open_image(type='mud',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/mud3.jpg')

wall_vertices, wall_coords = world.get_walls(wall_width,wall_height)
mud_vertices = world.get_mud()

print(len(wall_coords))

while not draw_tool.window_close():
    draw_tool.clear()

    # Keyboard_control
    # cc = world.check_collision(wall_coords,char_x,char_y,char_width,char_height)
    sp = 10
    if keyboard.is_pressed("d"):
        if not world.check_collision(wall_coords,char_x,char_y,char_width,char_height,'d'):
            char_x+=sp
        else:
            char_x-=0
            pass
    if keyboard.is_pressed("a"):
        if not world.check_collision(wall_coords,char_x,char_y,char_width,char_height,'a'):
            char_x-=sp
        else:
            char_x+=0
            pass

    if keyboard.is_pressed("w"):
        # if not 'w' in cc:
        if not world.check_collision(wall_coords,char_x,char_y,char_width,char_height,'w'):
            char_y+=sp       
        else:
            char_y-=0
            pass

    if keyboard.is_pressed("s"):
        if not world.check_collision(wall_coords,char_x,char_y,char_width,char_height,'s'):
            char_y-=sp
        else:
            char_y+=0
            pass


    vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
             (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
             (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
             2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]
    
    vertices = np.array(vertices,dtype=np.float32)
    for i in wall_vertices:
        draw_tool.draw(vert= i,image=image_w,img_data=img_data_w)
    

    draw_tool.draw(mud_vertices,image_m,img_data_m)

    draw_tool.draw(vertices, image, img_data)


    draw_tool.swap_buffers()

draw_tool.terminate()