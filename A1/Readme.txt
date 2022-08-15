Install the dependencies from dependencies/requirements.txt (as sudo)

Run the game from the /.../2021122002/ directory by running " sudo python3 -m logic.main "

How to play the game & game rules:

    On the top left corner there is a HUD box which displays the player stats like score,health,tasks done and time left.
    Once the time left hits zero, the game is over.

    Once the game starts, the player(RED) will be put in a random map with different objects spawned at random locations.
    Whether you get a simple maze with a few number of walls or a complex one depends on your luck!
    You can move the player around by using the WASD keys

    There is also an imposter who tries to get to you. In order to vapourise the imposter, find a red button on the map
    and get to it. If the imposter catches you, you lose.

    The main tasks of the level is to collect 2 items (apples laying on the map). The second one appears after the first
    one is collected.
    If both of them are collected, the player can exit by going through an exit logo that appears on the map.

    Avoid cactuses at all costs!! Coming in contact with a cactus decreases both you health and score. 
    If your health drops to zero, you lose.

    You can interact with a green button lying on the map in order to release gold coins.
    Collecting these coins increases your score.

    Press 'l' to toggle the lights. Once the lights are toggled, you can only see objects till a distance
    and without a wall in the middle.
    The enemy moves slower than you in the dark.


Bugs that can be encountered:
    Even though most of the game is implemented at my level best, there are a few bugs one might encounter
    in some special cases.
    --> When dark mode is turned on and the player gets too close to a wall or at a corner of a wall, we might see
            some amount of light slippoing to the other side of the wall.
    --> When the player is in contact with a wall, they might not be able to move to the sides also.

    I beleive these are minor bugs which can be removed if a little more time is put. Please evaluate accordingly.
    
