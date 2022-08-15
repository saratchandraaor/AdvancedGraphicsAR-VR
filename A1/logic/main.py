from time import sleep
import numpy as np
import keyboard

from boiler_plate.draw import DrawTool
from boiler_plate.hud import HUD
from logic.world import World
from logic.player import Player



#### Initializing required variables
lights = 1 #Status of the light

button_width = 25 #Dimensions of the buttons and powerups
button_height = 25


#Fragment shader in the prescence of light
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
#Fragment shader in the abscence of light
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

#Dimensions of the window
window_height = 1000
window_width = 1000
#Dimensions of the Character
char_height = window_height/20
char_width = window_width/20
#Dimensions of the Enemy
enemy_width= char_width/2
enemy_height = char_height/2

#Starting position of the character
char_x = window_width/4
char_y = window_height/4

#Dimensions of the wall
wall_width = window_width/20
wall_height = window_height/20

#create world and drawing objects from the other .py files
world = World(window_width,window_height)
draw_tool = DrawTool(window_width,window_height)

draw_tool.load_texture() #Load the pre-requisites of textures

#Import the required images for textures
m_image,m_img_data = draw_tool.open_image(type='char',path='boiler_plate/data/textures/char_mud.png')
image_w,img_data_w = draw_tool.open_image(type='wall',path='boiler_plate/data/textures/wall2.jpg')
image_m,img_data_m = draw_tool.open_image(type='mud',path='boiler_plate/data/textures/brown_mud.png')
m_image_b,m_img_data_b = draw_tool.open_image(type='button',path='boiler_plate/data/textures/button_mud.png')
m_image_e,m_img_data_e = draw_tool.open_image(type='enemy',path='boiler_plate/data/textures/enemy_mud.png')
m_image_t,m_img_data_t = draw_tool.open_image(type='task',path='boiler_plate/data/textures/task_mud.png')
m_image_p,m_img_data_p = draw_tool.open_image(type='powerup',path='boiler_plate/data/textures/powerup_mud.png')
m_image_pb,m_img_data_pb = draw_tool.open_image(type='pbutton',path='boiler_plate/data/textures/pbutton_mud.png')
m_image_o,m_img_data_o = draw_tool.open_image(type='obstacle',path='boiler_plate/data/textures/obstacle_mud.png')
image_exit,img_data_exit = draw_tool.open_image(type='exit',path='boiler_plate/data/textures/exit.jpg')
image_gameover,img_data_gameover = draw_tool.open_image(type='gameover',path='boiler_plate/data/textures/game_over.jpg')
l_image,l_img_data = draw_tool.open_image(type='char',path='boiler_plate/data/textures/char.png')
l_image_b,l_img_data_b = draw_tool.open_image(type='button',path='boiler_plate/data/textures/button.png')
l_image_e,l_img_data_e = draw_tool.open_image(type='enemy',path='boiler_plate/data/textures/enemy.webp')
l_image_t,l_img_data_t = draw_tool.open_image(type='task',path='boiler_plate/data/textures/task.png')
l_image_p,l_img_data_p = draw_tool.open_image(type='powerup',path='boiler_plate/data/textures/powerup.png')
l_image_pb,l_img_data_pb = draw_tool.open_image(type='pbutton',path='boiler_plate/data/textures/pbutton.png')
l_image_o,l_img_data_o = draw_tool.open_image(type='obstacle',path='boiler_plate/data/textures/obstacle.png')

#Generate the texture points for walls, mud tiles
wall_vertices, wall_coords = world.get_walls(wall_width,wall_height)
mud_vertices, mud_coords = world.get_mud(window_width,window_height)

#Generate the texture points for the game_over card and the background image
gameover_vertices = world.game_over()
bg_vertices = world.game_over()
bg_vertices = np.array(bg_vertices,dtype=np.float32)

player = Player(button_width,button_height,enemy_width,enemy_height)

#Generate the texture points for different objects on the map

exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)

all_object_coords = [i for i in wall_coords] # List that has info about where all the objects are so that new objects can avoid collision
all_object_coords.append(exit_coords)

button_vertices, button_coords = player.get_button(all_object_coords,window_width,window_height)

all_object_coords.append(button_coords)

pbutton_vertices, pbutton_coords = player.get_pbutton(all_object_coords,window_width,window_height)

all_object_coords.append(pbutton_coords)

enemy_vertices, enemy_coords = player.get_enemy(all_object_coords,window_width,window_height)
all_object_coords.append(enemy_coords)

task_vertices, task_coords = player.get_task(all_object_coords,window_width,window_height)
all_object_coords.append(task_coords)

obstacle_coords = [0,0,0]
obstacle_vertices = [0,0,0]

powerup_coords = [0,0,0]
powerup_vertices = [0,0,0]

for i in range(3):
    obstacle_vertices[i], obstacle_coords = player.get_obstacle(all_object_coords,window_width,window_height,i)
all_object_coords.append(obstacle_coords)

for i in range(3):
    powerup_vertices[i], powerup_coords = player.get_powerup(all_object_coords,window_width,window_height,i)
all_object_coords.append(powerup_coords)

enemy_vertices = np.array(enemy_vertices,dtype=np.float32)
task_vertices = np.array(task_vertices,dtype=np.float32)
obstacle_vertices = [np.array(i,dtype=np.float32) for i in obstacle_vertices]
powerup_vertices = [np.array(i,dtype=np.float32) for i in powerup_vertices]

hud = HUD()

#The maximum time in which the player must complete the given tasks
max_time = 60

while not draw_tool.window_close():

    draw_tool.load_shader(fragment_src)
    draw_tool.clear()

    if not player.exit:

        #See if time_left == 0. If it is, exit. Display HUD simultaneously.
        player.exit = hud.display(player.score,player.health,player.tasks_done,player.tasks_total,max_time,player.exit,player.caught,player.exited_maze,lights)

        # Keyboard_control
        cc = world.check_collision(wall_coords,char_x,char_y,char_width,char_height)
        if lights == 0:
            sp = 20 #Increase speed in the abscence of light to compensate the drop in fps
        else:
            sp = 10
        if keyboard.is_pressed("d"):
            if not 'd' in cc:
                char_x+=sp
                if lights==0:
                    player.score+=2
            elif not 'a' in cc:
                char_x-=sp*1.2
        if keyboard.is_pressed("a"):
            if not 'a' in cc:
                char_x-=sp
                if lights==0:
                    player.score+=2
            elif not 'd' in cc:
                char_x+=sp*1.2

        if keyboard.is_pressed("w"):
            if not 'w' in cc:
                char_y+=sp   
                if lights==0:
                    player.score+=2   
            elif not 's' in cc:
                char_y-=sp*1.2

        if keyboard.is_pressed("s"):
            if not 's' in cc:
                char_y-=sp
                if lights==0:
                    player.score+=2
            elif not 'w' in cc:
                char_y+=sp*1.2
        
        if keyboard.is_pressed("l"):
            lights = 1-lights
            sleep(0.2)

    if player.exit:
        exit = hud.display(player.score,player.health,player.tasks_done,player.tasks_total,max_time,player.exit,player.caught,player.exited_maze,lights)
    
    #Define the image's vertices (for the texture) for the player
    vertices = [2*char_x/window_width-1, 2*char_y/window_height-1,  0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
            (2*char_x+char_width)/window_width-1, 2*char_y/window_height-1,  0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
            (2*char_x+char_width)/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
            2*char_x/window_width-1,  (2*char_y+char_height)/window_height-1,  0.0,  1.0, 1.0, 1.0,  0.0, 1.0]
    vertices = np.array(vertices,dtype=np.float32)


    #Check if the player has interacted with different objects on the map.
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

    #Keep updating the enemy's position according to the path algorithm
    enemy_vertices,enemy_coords =player.enemy_movement(char_x,char_y,enemy_width,enemy_height,lights,wall_coords)
    
    if lights == 0: #When lights are turned off

        image,img_data = m_image,m_img_data 
        image_b,img_data_b = m_image_b,m_img_data_b 
        image_e,img_data_e = m_image_e,m_img_data_e  
        image_t,img_data_t = m_image_t,m_img_data_t 
        image_p,img_data_p = m_image_p,m_img_data_p  
        image_pb,img_data_pb = m_image_pb,m_img_data_pb  
        image_o,img_data_o = m_image_o,m_img_data_o  

        #The radius of the player's light source
        radius_of_illumination = 200

        draw_tool.load_shader(fragment_src)

        if player.exit: #If the game is over, display the gmae_over card
            draw_tool.load_shader(fragment_src)
            draw_tool.draw(gameover_vertices,image_gameover,img_data_gameover)

        else:
            #Display different objects on the map after checking their status (whether to display or not)
            draw_tool.draw(vertices, image, img_data)
            
            if player.tasks_done == 2:
                if abs(exit_coords[0] - char_x+ exit_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(exit_coords[1] - char_y+ exit_coords[3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,exit_coords[0],exit_coords[1],wall_coords):
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)

            if abs(task_coords[0] - char_x+ task_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(task_coords[1] - char_y+ task_coords[3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,task_coords[0],task_coords[1],wall_coords):
                draw_tool.load_shader(fragment_src)
            else:
                draw_tool.load_shader(fragment_src_dark)

            if player.task_state:
                draw_tool.draw(task_vertices,image_t,img_data_t)
            
            if not player.task_state:
                task_vertices, task_coords = player.get_task(all_object_coords,window_width,window_height)
                task_vertices = np.array(task_vertices,dtype=np.float32)

            if not player.task_state and player.tasks_done<2:
                player.task_state = True
                draw_tool.draw(task_vertices,image_t,img_data_t)

            if player.tasks_done >= 2:
                exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)


            for i in range(3):
                if player.obstacle_state[i]:
                    if abs(obstacle_coords[i][0] - char_x+ obstacle_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(obstacle_coords[i][1] - char_y+ obstacle_coords[i][3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,obstacle_coords[i][0],obstacle_coords[i][1],wall_coords):
                        draw_tool.load_shader(fragment_src)
                    else:
                        draw_tool.load_shader(fragment_src_dark)
                    draw_tool.draw(obstacle_vertices[i],image_o,img_data_o)

            for i in range(3):
                if player.powerup_state[i]:
                    if abs(powerup_coords[i][0] - char_x+ powerup_coords[i][2]/2 - char_width/2) <= radius_of_illumination and abs(powerup_coords[i][1] - char_y+ powerup_coords[i][3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,powerup_coords[i][0],powerup_coords[i][1],wall_coords):
                        draw_tool.load_shader(fragment_src)
                    else:
                        draw_tool.load_shader(fragment_src_dark)
                    draw_tool.draw(powerup_vertices[i],image_p,img_data_p)

            if player.enemy_state:
                if abs(button_coords[0] - char_x+ button_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(button_coords[1] - char_y+ button_coords[3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,button_coords[0],button_coords[1],wall_coords):
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(button_vertices, image_b, img_data_b)
                

            if player.pbutton_state:
                if abs(pbutton_coords[0] - char_x+ pbutton_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(pbutton_coords[1] - char_y+ pbutton_coords[3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,pbutton_coords[0],pbutton_coords[1],wall_coords):
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(pbutton_vertices, image_pb, img_data_pb)
            
            if player.enemy_state:
                if abs(enemy_coords[0] - char_x+ enemy_coords[2]/2 - char_width/2) <= radius_of_illumination and abs(enemy_coords[1] - char_y+ enemy_coords[3]/2 - char_height/2) <= radius_of_illumination and not world.check_walls_lights_off(char_x,char_y,enemy_coords[0],enemy_coords[1],wall_coords):
                    draw_tool.load_shader(fragment_src)
                else:
                    draw_tool.load_shader(fragment_src_dark)
                draw_tool.draw(enemy_vertices,image_e,img_data_e)

            for i in range(len(wall_vertices)):
                if abs(wall_coords[i][0] - char_x+ wall_coords[i][2]/2 - char_width/2) <= radius_of_illumination*0.9 and abs(wall_coords[i][1] - char_y+ wall_coords[i][3]/2 - char_height/2) <= radius_of_illumination*0.9:
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
            

    else:#If the lights are turned off

        image,img_data = l_image,l_img_data 
        image_b,img_data_b = l_image_b,l_img_data_b 
        image_e,img_data_e = l_image_e,l_img_data_e  
        image_t,img_data_t = l_image_t,l_img_data_t 
        image_p,img_data_p = l_image_p,l_img_data_p  
        image_pb,img_data_pb = l_image_pb,l_img_data_pb  
        image_o,img_data_o = l_image_o,l_img_data_o  

        if player.exit:
            gameover_vertices = np.array(gameover_vertices,dtype=np.float32)
            draw_tool.load_shader(fragment_src)
            draw_tool.draw(gameover_vertices,image_gameover,img_data_gameover)

        else:
            #Display different objects on the map after checking their status (whether to display or not)

            draw_tool.draw(bg_vertices, image_m, img_data_m)
            
            if player.enemy_state:
                draw_tool.draw(button_vertices, image_b, img_data_b)
                draw_tool.draw(enemy_vertices,image_e,img_data_e)


            if player.pbutton_state:
                draw_tool.draw(pbutton_vertices, image_pb, img_data_pb)

            draw_tool.load_shader(fragment_src)

            draw_tool.draw(vertices, image, img_data)

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
                task_vertices, task_coords = player.get_task(all_object_coords,window_width,window_height)
                task_vertices = np.array(task_vertices,dtype=np.float32)
                
            if not player.task_state and player.tasks_done<2:
                player.task_state = True
                draw_tool.draw(task_vertices,image_t,img_data_t)

            if player.tasks_done >= 2:
                exit_vertices,exit_coords = world.create_exit(wall_width,wall_height)
                draw_tool.draw(exit_vertices,image_exit,img_data_exit)


    draw_tool.swap_buffers()

#Exit the code
hud.quit()
draw_tool.terminate()