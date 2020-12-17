import pgzrun
from random import *  # import all functions from library

#define screen
WIDTH = 1000
HEIGHT = 600
score_board_height = 60  # change to height of scoreboard

# count score
score = 0  # start off with zero points

# sprite speeds
JUNK_SPEED = 5
SATELLITE_SPEED = 5
DEBRIS_SPEED = 5
LASER_SPEED = -5

BACKGROUND_IMG = "background"  # change to your file name
PLAYER_IMG = "player_ship"  # change to your file name
JUNK_IMG = "space_junk"  # change to your file name
SATELLITE_IMG = "satellite"  # change to your file name
DEBRIS_IMG = "tesla_roadster" # change to your file name
LASER_IMG = "laser_red"

# Background music
sounds.background_music.play(-1)

#INITIALIZE SPRITES
# sprite_name = Actor("file_name", rect_pos = (x, y))
player = Actor(PLAYER_IMG)
player.midright = (WIDTH - 10, HEIGHT/2)  # rect_position = (x, y)

# initialize junks
junks = [] # created a list to store our junks 

for i in range(5):  # make 5 junks
    junk = Actor(JUNK_IMG)
    x_pos = randint(-500, -50)
    y_pos = randint(score_board_height, HEIGHT - junk.height)
    junk.pos = (x_pos, y_pos)  # rect_position = (x, y)
    junks.append(junk)  # add each junk to our list

# initialize satellite sprite
satellite = Actor(SATELLITE_IMG)
x_sat = randint(-500, -50)
y_sat = randint(score_board_height, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)  # initial rect position

# initialize debris sprite
debris = Actor(DEBRIS_IMG)
x_deb = randint(-500, -50)
y_deb = randint(score_board_height, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb)  # initial rect position

# initalize lasers
lasers = []


#MAIN GAME LOOP___________________________________________
def update():  # main update function
    if score >= 0:
        updatePlayer()  # calling our player update function
        updateJunk()  # calling junk update function 
        updateSatellite()  # call satellite update function 
        updateDebris() # call debris update function
        updateLasers()
    
def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    player.draw()  # draw player sprite on screen
    satellite.draw()
    debris.draw()
    for junk in junks:  # for each junk in our list
        junk.draw()  # draw junk sprite on screen
    for laser in lasers:
        laser.draw()
    if score < 0:
        game_over_text = "GAME OVER"
        screen.draw.text(game_over_text, center=(WIDTH/2, HEIGHT/2), fontsize=70, color="red", ocolor="white", owidth=0.5)

        sounds.background_music.stop()
    # show text on screen
    show_score = "Score: " + str(score)  # remember to convert score to a string
    screen.draw.text(show_score, topleft=(750, 15), fontsize=35, color="white")
    # rect_position = (x, y)


#UPDATE SPRITES________________
def updatePlayer():
    # check for keyboard inputs
    if keyboard.w == 1:
        player.y += -5  # moving up is negative y-direction
    elif keyboard.s == 1:
        player.y += 5  # moving down is positive y-direction
    # prevent player from moving off screen - add boundaries
    if player.top < score_board_height:
        player.top = score_board_height
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT

    # check for spacebar to create laser
    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def updateJunk():
    global score
    for junk in junks:  # for each junk in our list
        junk.x += JUNK_SPEED
            
        collision = player.colliderect(junk)  # declare collision variable

        if junk.left > WIDTH or collision == 1:  # make junk reappear if move off screen
            x_pos = randint(-500, -50) # start off screen
            y_pos = randint(score_board_height, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1: # if collisions occurs 
            score += 1  # this is the same score = score + 1
            sounds.collect_pep.play()

def updateSatellite():
    global score
    satellite.x += SATELLITE_SPEED  # (1) update position

    collision = player.colliderect(satellite)
    if satellite.left > WIDTH or collision == 1:  # (2) check if offscreen and collisions
        x_sat = randint(-500, - 50)
        y_sat = randint(score_board_height, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:  # (3) update score
        score += -10  # decreasing the score if satellite collides
        sounds.explosion.play()

def updateDebris():
    global score
    debris.x += DEBRIS_SPEED  # (1) update position

    collision = player.colliderect(debris)
    if debris.left > WIDTH or collision == 1:  # (2) check if offscreen and collisions
        x_deb = randint(-500, - 50)
        y_deb = randint(score_board_height, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:  # (3) update score
        score += -20  # decreasing the score if debris collides

def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        # if laser goes off screen
        if laser.right < 0:
            lasers.remove(laser)
        # check for collisions
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = randint(-500, - 50)
            y_sat = randint(score_board_height, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -10
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = randint(-500, -50)
            y_deb = randint(score_board_height, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += -20
        for junk in junks:  # for each junk in the list
            if junk.colliderect(laser) == 1:
                lasers.remove(laser)
                x_pos = randint(-500, -50) # start off screen
                y_pos = randint(score_board_height, HEIGHT - junk.height)
                junk.topleft = (x_pos, y_pos)
                score += 5


player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
    
pgzrun.go()  # function that runs our game loop

