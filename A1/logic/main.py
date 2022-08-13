from time import sleep
import numpy as np
import keyboard

from boiler_plate.draw import DrawTool
# from hud import HUD
from logic.world import World
from logic.player import Player
lights = 1

button_width = 20
button_height = 20

fragment_src = """
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

fragment_src_dark = """
        # version 330
        in vec3 v_color;
        in vec2 v_texture;
        out vec4 out_color;
        uniform sampler2D s_texture;
        void main()
        {
            out_color = texture(s_texture, v_texture)/5; // * vec4(v_color, 1.0f);
        }
        """

window_height = 1000
window_width = 1000

char_height = window_height/20
char_width = window_width/20

enemy_width= char_width/2
enemy_height = char_height/2

char_x = window_width/2
char_y = window_height/2

enemy_x = window_width/3
enemy_y = window_height/3

vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 1.0 ,
             (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  0.0, 0.0,
             (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0, 1.0, 0.0, 
             2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0, 1.0, 1.0]

wall_width = window_width/20
wall_height = window_height/20

world = World(window_width,window_height)
draw_tool = DrawTool(window_width,window_height)
draw_tool.load_texture()
draw_tool.load_shader(fragment_src)

image,img_data = draw_tool.open_image(type='char',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/char.png')
image_w,img_data_w = draw_tool.open_image(type='wall',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/wall2.jpg')
image_m,img_data_m = draw_tool.open_image(type='mud',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/mud2.jpg')
image_b,img_data_b = draw_tool.open_image(type='button',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/button.png')
image_e,img_data_e = draw_tool.open_image(type='enemy',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/enemy.png')
image_t,img_data_t = draw_tool.open_image(type='task',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/task.png')
image_p,img_data_p = draw_tool.open_image(type='powerup',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/powerup.png')
image_pb,img_data_pb = draw_tool.open_image(type='pbutton',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/pbutton.png')
image_o,img_data_o = draw_tool.open_image(type='obstacle',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/obstacle.png')
image_exit,img_data_exit = draw_tool.open_image(type='exit',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/exit.jpg')
image_gameover,img_data_gameover = draw_tool.open_image(type='gameover',path='/home/ysk/Documents/AG/A1/boiler_plate/data/textures/game_over.jpg')


wall_vertices, wall_coords = world.get_walls(wall_width,wall_height)
mud_vertices, mud_coords = world.get_mud(window_width,window_height)


gameover_vertices = world.game_over()
bg_vertices = world.game_over()

bg_vertices = np.array(bg_vertices,dtype=np.float32)


player = Player(button_width,button_height,enemy_width,enemy_height)

button_vertices, button_coords = player.get_button(wall_coords,window_width,window_height)
pbutton_vertices, pbutton_coords = player.get_pbutton(wall_coords,window_width,window_height)

##Edit from here

enemy_vertices, enemy_coords = player.get_enemy(wall_coords,window_width,window_height)
task_vertices, task_coords = player.get_task(wall_coords,window_width,window_height)

obstacle_coords = [0,0,0]
obstacle_vertices = [0,0,0]

powerup_coords = [0,0,0]
powerup_vertices = [0,0,0]

for i in range(3):
    obstacle_vertices[i], obstacle_coords = player.get_obstacle(wall_coords,window_width,window_height,i)

for i in range(3):
    powerup_vertices[i], powerup_coords = player.get_powerup(wall_coords,window_width,window_height,i)


enemy_vertices = np.array(enemy_vertices,dtype=np.float32)
task_vertices = np.array(task_vertices,dtype=np.float32)
obstacle_vertices = [np.array(i,dtype=np.float32) for i in obstacle_vertices]
exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)
powerup_vertices = [np.array(i,dtype=np.float32) for i in powerup_vertices]


# hud = HUD()

while not draw_tool.window_close():

    draw_tool.load_shader(fragment_src)
    draw_tool.clear()

    print(player.get_player_stats())

    # draw_tool.render_text()

    # draw_tool.raster()

    # Keyboard_control
    # cc = world.check_collision(wall_coords,char_x,char_y,char_width,char_height)
    sp = 20
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
    
    if keyboard.is_pressed("l"):
        lights = 1-lights
        sleep(0.2)

    vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
            (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
            (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
            2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]
    vertices = np.array(vertices,dtype=np.float32)

    player.check_button_status(char_x,char_y,char_width,char_height,button_coords)
    player.check_task_status(char_x,char_y,char_width,char_height,task_coords)
   
    for i in range(3):
        player.check_obstacle_status(char_x,char_y,char_width,char_height,obstacle_coords,i)
   
    for i in range(3):
        player.check_powerup_status(char_x,char_y,char_width,char_height,powerup_coords,i)
   

    player.check_exit_status(char_x,char_y,char_width,char_height,exit_coords,player.tasks_done)
    player.check_enemy_status(char_x,char_y,char_width,char_height,enemy_coords)
    player.check_health_status()
    player.check_pbutton_status(char_x,char_y,char_width,char_height,pbutton_coords)

    # enemy_coords = player.enemy_movement(char_x,char_y,enemy_coords)
    
    # draw_tool.clear()
    # hud.draw(window_width,window_height)
    
    if lights == 0:

        radius_of_illumination = 200

        draw_tool.load_shader(fragment_src)

        if player.exit:
            gameover_vertices = np.array(gameover_vertices,dtype=np.float32)
            draw_tool.load_shader(fragment_src)
            draw_tool.draw(gameover_vertices,image_gameover,img_data_gameover)

        else:
            draw_tool.draw(vertices, image, img_data)
            
            if player.tasks_done == 2:
                if abs(exit_coords[0] - char_x+ exit_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(exit_coords[1] - char_y+ exit_coords[3]/2 - char_height/2) <= radius_of_illumination:
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)

            if abs(task_coords[0] - char_x+ task_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(task_coords[1] - char_y+ task_coords[3]/2 - char_height/2) <= radius_of_illumination:
                draw_tool.load_shader(fragment_src)
            else:
                draw_tool.load_shader(fragment_src_dark)

            if player.task_state:
                draw_tool.draw(task_vertices,image_t,img_data_t)
            
            if not player.task_state:
                task_vertices, task_coords = player.get_task(wall_coords,window_width,window_height)
                task_vertices = np.array(task_vertices,dtype=np.float32)
                

            if not player.task_state and player.tasks_done<2:
                player.task_state = True
                draw_tool.draw(task_vertices,image_t,img_data_t)

            if player.tasks_done >= 2:
                exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)


            for i in range(3):
                if player.obstacle_state[i]:
                    if abs(obstacle_coords[i][0] - char_x+ obstacle_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(obstacle_coords[i][1] - char_y+ obstacle_coords[i][3]/2 - char_height/2) <= radius_of_illumination:
                        draw_tool.load_shader(fragment_src)
                    else:
                        draw_tool.load_shader(fragment_src_dark)
                    draw_tool.draw(obstacle_vertices[i],image_o,img_data_o)

            for i in range(3):
                if player.powerup_state[i]:
                    if abs(powerup_coords[i][0] - char_x+ powerup_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(powerup_coords[i][1] - char_y+ powerup_coords[i][3]/2 - char_height/2) <= radius_of_illumination:
                        draw_tool.load_shader(fragment_src)
                    else:
                        draw_tool.load_shader(fragment_src_dark)
                    draw_tool.draw(powerup_vertices[i],image_p,img_data_p)



            if player.enemy_state:
                if abs(button_coords[0] - char_x+ button_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(button_coords[1] - char_y+ button_coords[3]/2 - char_height/2) <= radius_of_illumination:
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(button_vertices, image_b, img_data_b)
                

            if player.pbutton_state:
                if abs(pbutton_coords[0] - char_x+ pbutton_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(pbutton_coords[1] - char_y+ pbutton_coords[3]/2 - char_height/2) <= radius_of_illumination:
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(pbutton_vertices, image_pb, img_data_pb)
            
            if player.enemy_state:
                if abs(enemy_coords[0] - char_x+ enemy_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(enemy_coords[1] - char_y+ enemy_coords[3]/2 - char_height/2) <= radius_of_illumination:
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                enemy_vertices,enemy_coords =player.enemy_movement(char_x,char_y)
                print("ENEMY")
                draw_tool.draw(enemy_vertices,image_e,img_data_e)

            for i in range(len(wall_vertices)):
                if abs(wall_coords[i][0] - char_x+ wall_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(wall_coords[i][1] - char_y+ wall_coords[i][3]/2 - char_height/2) <= radius_of_illumination:
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(vert= wall_vertices[i],image=image_w,img_data=img_data_w)
            

            for i in range(len(mud_vertices)):
                if abs(mud_coords[i][0] - char_x + mud_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(mud_coords[i][1] - char_y + mud_coords[i][3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,mud_coords[i][0],mud_coords[i][1],wall_coords):
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(vert= mud_vertices[i],image=image_m,img_data=img_data_m)

    else:

        if player.exit:
            gameover_vertices = np.array(gameover_vertices,dtype=np.float32)
            draw_tool.load_shader(fragment_src)
            draw_tool.draw(gameover_vertices,image_gameover,img_data_gameover)

        else:
            draw_tool.draw(bg_vertices, image_m, img_data_m)
            
            if player.enemy_state:
                draw_tool.draw(button_vertices, image_b, img_data_b)
                enemy_vertices,enemy_coords =player.enemy_movement(char_x,char_y)
                print("ENEMY")
                draw_tool.draw(enemy_vertices,image_e,img_data_e)


            if player.pbutton_state:
                draw_tool.draw(pbutton_vertices, image_pb, img_data_pb)

            draw_tool.load_shader(fragment_src)

            for i in range(len(wall_vertices)):
                draw_tool.draw(vert= wall_vertices[i],image=image_w,img_data=img_data_w)
    

            for i in range(3):
                if player.obstacle_state[i]:
                    draw_tool.draw(obstacle_vertices[i],image_o,img_data_o)

            for i in range(3):
                if player.powerup_state[i]:
                    draw_tool.draw(powerup_vertices[i],image_p,img_data_p)



            if player.task_state:
                draw_tool.draw(task_vertices,image_t,img_data_t)
            
            if not player.task_state:
                task_vertices, task_coords = player.get_task(wall_coords,window_width,window_height)
                task_vertices = np.array(task_vertices,dtype=np.float32)
                

            if not player.task_state and player.tasks_done<2:
                player.task_state = True
                draw_tool.draw(task_vertices,image_t,img_data_t)

            if player.tasks_done >= 2:
                exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)


            draw_tool.draw(vertices, image, img_data)

            # for i in range(len(mud_vertices)):
            #     draw_tool.load_shader(fragment_src)
            #     draw_tool.draw(vert= mud_vertices[i],image=image_m,img_data=img_data_m)
            
        
    draw_tool.drawString("HELLO")


    draw_tool.swap_buffers()

draw_tool.terminate()