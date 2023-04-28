import pygame #Imports the pygame library allowing me to use its features within my code
import csv #Allows the use and mainpulation of csv files
import sqlite3 #Allows SQL functions to be used within the file
import constants #Allows main.py to use variables from the constants.py folder
from weapon import Weapon #Allows the class, Weapon, to be used within main.py from weapon.py
from perk import Perks  #Allows the class, Perks, to be used within main.py from perk.py
from features import DamageValue,ScreenFade #Allows the DamageValue and ScreenFade class to be used within main.py from features.py
from maps import Maps #Allows the maps class to be used within main.py from maps.py
from button import Button  #Allows the class, Button, to be used within main.py from button.py
from leaderboard import add_user,select_users,create_table #Allows the mentioned functions to be used in the main file from the leaderboard.py file

pygame.init() #Initialises all imported pygame modules, allowing me to have full access to start and run modules


screen=pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)) #Creates game window, every piece of code that "draws" an object will draw it onto this screen 
pygame.display.set_caption("Computer Science NEA") #Names the python project on the screen window
clock=pygame.time.Clock() #The variable clock can be used to keep track of time within the game


move_left=False  #Sets movement logic for left, when the user presses on the appropritate key, this is set to true so the user's position is moved to the left. It is then set back to false so that the user isn't continuously moving left.
move_right=False #Sets movement logic for right, when the user presses on the appropritate key, this is set to true so the user's position is moved to the right. It is then set back to false so that the user isn't continuously moving right.
move_up=False   #Sets movement logic for up, when the user presses on the appropritate key, this is set to true so the user's position is moved to the up. It is then set back to false so that the user isn't continuously moving up.
move_down=False #Sets movement logic for down, when the user presses on the appropritate key, this is set to true so the user's position is moved to the down. It is then set back to false so that the user isn't continuously moving down.


def img_scale(image,scale): #Creating a function to make it easier to scale up objects
    
    w=image.get_width()     #Stores the width of an image as a variable
    h=image.get_height()    #Stores the height of an image as a variable
    return pygame.transform.scale(image, (w*scale,h*scale)) #Uses the pygame scale function to increase the width and height of an image by a scale factor


level=6 #Defines which level is being played
font=pygame.font.Font("assets/fonts/AtariClassic.ttf", 20) #Defines font of text that will appear on screen
menu_font=pygame.font.Font("assets/fonts/AtariClassic.ttf", 12) #Defines font of text for menu that will appear on screen


restart_img=img_scale(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(),constants.BUTTON_SCALE) #Loads restart button image
start_img=img_scale(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(),constants.BUTTON_SCALE) #Loads start button image
exit_img=img_scale(pygame.image.load("assets/images/buttons/button_quit.png").convert_alpha(),constants.BUTTON_SCALE) #Loads exit button image
resume_img=img_scale(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(),constants.BUTTON_SCALE) #Loads resume button image
rules_img=img_scale(pygame.image.load("assets/images/buttons/button_rules.png").convert_alpha(),constants.BUTTON_SCALE) #Loads rules button image
back_img=img_scale(pygame.image.load("assets/images/buttons/button_back.png").convert_alpha(),constants.BUTTON_SCALE) #Loads back button image
leaderboard_img=img_scale(pygame.image.load("assets/images/buttons/button_leaderboard.png").convert_alpha(),constants.BUTTON_SCALE) #Loads leaderboard button image
enter_img=img_scale(pygame.image.load("assets/images/buttons/button_enter.png").convert_alpha(),constants.BUTTON_SCALE) #Loads enter button image


table_leaderboard=img_scale(pygame.image.load("assets/images/other/table.png").convert_alpha(),constants.TABLE_SCALE) #Loads image used for the leaderboard table into the game
title=img_scale(pygame.image.load("assets/images/other/title.png").convert_alpha(),constants.TITLE_SCALE) #Loads title into program


empty_heart=img_scale(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),constants.PERK_SCALE) #Loads in the empty heart image
half_heart=img_scale(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),constants.PERK_SCALE) #Loads in the half full heart image
full_heart=img_scale(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),constants.PERK_SCALE) #Loads in the full heart image


coins=[] #Creates list for coin images

for i in range(4): #Iterates through coin images 
    img=img_scale(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(),constants.PERK_SCALE) #Loads in each coin image
    coins.append(img) #Adds image to coin images list


health_potion=img_scale(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),constants.POTION_SCALE)#Loads potion image
perk_images=[] #Creates empty list to store perk images such as coins and potions
perk_images.append(coins) #Adds all coin images to perk list
perk_images.append(health_potion) #Adds potion image to perk list


bow_image=img_scale(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(),constants.WEAPON_SCALE) #Loads in the bow image
arrow_image=img_scale(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(),constants.WEAPON_SCALE) #Loads in the arrow image
fireball_image=img_scale(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),constants.FIREBALL_SCALE) #Loads in the fireball image


tile_list=[] #Creates an empty list that will contain each tile image
for i in range(18): #Iterates through each tile image
    
    tile_image=pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha() #Loads in tile images
    tile_image=pygame.transform.scale(tile_image,(constants.TILE_SIZE,constants.TILE_SIZE)) #Scales tile images
    tile_list.append(tile_image) #Adds current tile image to the tile list


sprite_animations=[]   #Creates a list that will contain the animations of all sprites
sprite_types=["elf","imp","skeleton","goblin","muddy","tiny_zombie","big_demon"] #Creates a list of all sprites
animation_types=["idle","run"] #Creates a list showing the two different parts of the animations

for sprite in sprite_types: #Iterates through each sprite in the sprite types list
    animation_list=[] #Creates an animation list for each individual sprite

    for animation in animation_types: #Iterates through each animation type to have an idle list and running list
        temp_list=[] #Creates a temporary list to seperate the idle animations and the run animations
        
        for i in range(4): #Iterates through each sprite image
        
            img=pygame.image.load(f"assets/images/characters/{sprite}/{animation}/{i}.png").convert_alpha()  #Stores sprite image into variable
            img=img_scale(img,constants.SCALE) #Calls the function of img_scale to scale up the sprite image
            temp_list.append(img) #Adds image to temporary list 
        
        animation_list.append(temp_list) #Adds temporary list to the animation list for both idle and run animations
    
    sprite_animations.append(animation_list) #Adds animation lists of idle and run animations for each sprite


def display_leaderboard(leaderboard_page,menu_page): #Creates function to draw users and their scores onto the page
    
    try: #Attempts to display table

        screen.blit(table_leaderboard,(constants.SCREEN_WIDTH//2 - 210,50)) #Draws table image onto screen
        table=select_users() #Sets variable to the users and scores returned from the leaderboard function
        users_list=[] #Creates a list to store all usernames
        scores_list=[] #Creates a list to store all scores

        for i in range(0,len(table)): #Iterates through each item in table
            users_list.append(table[i][0]) #Adds each username to username list
            scores_list.append(table[i][1]) #Adds each score to scores list

        for i in range(0,len(scores_list)): #Iterates through each item in score list 
            scores_list[i]=str(scores_list[i]) #Converts score to string form

        for i in range(0,len(users_list)): #Iterates through each list
            draw_text(users_list[i],font,constants.WHITE,220,100+(42*i)) #Calls draw text function to draw usernames in each row of leaderboard table
            draw_text(scores_list[i],font,constants.WHITE,460,100+(42*i)) #Calls draw text function to draw scores in each row of leaderboard table
            
    except sqlite3.OperationalError: #Checks if leaderboard table hasn't been created yet

        screen.fill(constants.CRIMSON) #Fills the screen with crimson colour
        draw_text("No Scores Have Been Saved Yet",menu_font,constants.WHITE,10,50) #Calls draw text function to draw given text

    if back_button.draw(screen): #Draws back button and checks if its has been pressed
        leaderboard_page=False #Leaderboard page should no longer be displayed
        menu_page=True #Returns back to menu page

    return leaderboard_page,menu_page #Returns variables that determine which page should be shown
        

def draw_text(text,font,text_col,x,y): #Creates function for drawing text onto screen
    img=font.render(text,True,text_col) #Creates an image variable holding properties of the text
    screen.blit(img,(x,y)) #Draw text onto screen at specified position


def panel(): #Creates function for displaying game info
    
    pygame.draw.rect(screen,constants.GREY,(0,0,constants.SCREEN_WIDTH,50)) #Creates panel at the top where information will be drawn
    pygame.draw.line(screen,constants.WHITE,(0,50),(constants.SCREEN_WIDTH,50)) #Draws a line towards the top of the screen to seperate information from game
    
    half_heart_drawn=False #Variable used as condition so that only 1 half heart could be drawn
    
    for i in range(5): #5 heart images will be drawn
        
        if player.health >= ((i+1) * 20): #Checks if hearts should be full heart
            screen.blit(full_heart,(10 + i*50, 0)) #Draws heart onto screen
        
        elif (player.health % 20)>0 and half_heart_drawn==False: #Checks if there's a remainder of health (so if a half heart needs to be drawn) and that a half heart isn't already on the screen
           
            screen.blit(half_heart,(10 + i*50, 0)) #Draws heart onto screen
            half_heart_drawn=True #Sets variable to true as it has been drawn
        
        else: #If no health is left over
            screen.blit(empty_heart, (10+i*50,0)) #Draws empty heart
    

    draw_text("LEVEL:" + str(level),font,constants.WHITE,constants.SCREEN_WIDTH/2,15) #Calls draw text function to draw given text 
    draw_text(f"X: {player.score}",font,constants.WHITE,constants.SCREEN_WIDTH-150,15) #Calls draw text function to draw given text onto screen


def display_rules(rules,menu):
    
    draw_text("Use WASD to move. Click to shoot",menu_font,constants.WHITE,10,20) #Calls draw text function to draw given text
    draw_text("Press the escape key to pause the game",menu_font,constants.WHITE,10,60) #Calls draw text function to draw given text
    draw_text("Your character has 100 health",menu_font,constants.WHITE,10,100) #Calls draw text function to draw given text
    draw_text("Enemies have either 60 or 200 health",menu_font,constants.WHITE,10,140)#Calls draw text function to draw given text
    draw_text("Arrows deals damage from 10 to 20",menu_font,constants.WHITE,10,180)#Calls draw text function to draw given text
    draw_text("Killing enemies gains you 2 coins",menu_font,constants.WHITE,10,220)#Calls draw text function to draw given text
    draw_text("If you die you lose 5 to 10 coins from at the start of the level",menu_font,constants.WHITE,10,260)#Calls draw text function to draw given text
    draw_text("To complete the level, find the ladder in each map",menu_font,constants.WHITE,10,300)#Calls draw text function to draw given text
    draw_text("There are 6 levels in total",menu_font,constants.WHITE,10,340)#Calls draw text function to draw given text
    draw_text("The top 5 scores are on the leaderboard",menu_font,constants.WHITE,10,380)#Calls draw text function to draw given text
    draw_text("Good luck!!!",font,constants.WHITE,300,420)#Calls draw text function to draw given text

    if back_button.draw(screen): #Checks if back button has been pressed
        rules=False #Rules page should no longer be displayed
        menu=True #Returns back to menu page
    
    return rules,menu #Returns values of rules and menu so the correct pages are displayed


def new_level(): #Creates function for loading new level
    
    damage_value_group.empty() #Resets damage text group for new level
    perk_group.empty()  #Resets perk group for new level
    arrow_group.empty() #Resets arrow group for new level
    fireball_group.empty()  #Resets fireball group for new level

    map_data=[] #Create empty list for new level
    for row in range(constants.ROWS): #Iterates through each row to add columns of empty space
        
        r=[-1]*constants.COLS #Creates a list with 150 "-1"s to represent an empty space
        map_data.append(r) #Adds the created rows to the data list

    with open(f"levels/level{level}_data.csv",newline="") as csvfile: #Opens file containing level information as a csv
        reader=csv.reader(csvfile,delimiter=",") #Defines how data should be seperated (by a comma)
        
        for x, row in enumerate(reader): #Iterates through each of the rows, keeping track of how many iterations have taken place
            
            for y, tile in enumerate(row): #Iterates through each tile in each row, keeping track of how many iterations have taken place
                map_data[x][y]=int(tile) #Assigns each co-ordinate of map to a tile integer   

    return map_data #Returns the map created


damage_value_group=pygame.sprite.Group() #Creates damage value group
arrow_group=pygame.sprite.Group() #Creates arrow group
perk_group=pygame.sprite.Group() #Creates perk group
fireball_group=pygame.sprite.Group() #Creates group for fireballs
score_coin = Perks(constants.SCREEN_WIDTH-175,23,0,coins,True) #Adds a coin at top of the screen to show how many coins have been collected
perk_group.add(score_coin) #Adds the score coin to the perk group

map_data=new_level() #Calls function to create map for first level and recieves the map on variable
maps=Maps() #Creates an object of the class named maps for the level
maps.process_data(map_data,tile_list,perk_images,sprite_animations) #Calls function to process the tile data
player=maps.player #Sets player variable equal to the player object created on the player spawn tile
enemy_list=maps.character_list #Extracts enemies from maps data
bow=Weapon(bow_image, arrow_image) #Uses the weapon class to create an object named bow

for perk in maps.perk_list: #Iterates through each perk in the perk list
    perk_group.add(perk) #Adds perk to perk group


intro_fade=ScreenFade(1,constants.BLACK,4,screen) #Creates object of screenfade class for an intro fade
death_fade=ScreenFade(2,constants.CRIMSON,4,screen) #Creates object of screenfade class for a death fade

start_button=Button(constants.SCREEN_WIDTH//2 - 200,250,start_img) #Calls button class to create a new button object
rules_button=Button(constants.SCREEN_WIDTH//2,350,rules_img) #Calls button class to create a new button object
exit_button=Button(constants.SCREEN_WIDTH//2 ,250,exit_img) #Calls button class to create a new button object
resume_button=Button(constants.SCREEN_WIDTH//2 - 200,250,resume_img) #Calls button class to create a new button object
restart_button=Button(constants.SCREEN_WIDTH//2 - 90,constants.SCREEN_HEIGHT//2 - 50,restart_img) #Calls button class to create a new button object
back_button=Button(constants.SCREEN_WIDTH//2 - 90,constants.SCREEN_HEIGHT - 120,back_img) #Calls button class to create a new button object
leaderboard_button=Button(constants.SCREEN_WIDTH//2 - 200,350,leaderboard_img) #Calls button class to create a new button object
enter_button=Button(325,345,enter_img) #Calls button class to create a new button object

temp_score=0 #Creates variable to store initial score when game hasn't started
username='' #Creates variable to store what user has entered for their username, initially blank
start_game=False #Game shouldn't start immediately
start_intro=False #Initially doesn't start intro fade
menu=True #Sets a variable defining whether the game menu is displayed, which it should be initially
rules=False #Sets a variable defining whether the rules page is displayed or not
leaderboard=False #Sets a variable defining whether the leaderboard page is displayed or not
pause_game=False #Game shouldn't be paused immediately
pause_menu=True #Sets a variable defining whether the pause menu is displayed
game_finished=False #Sets a variable defining whether the game has been completed or not
run=True #Sets variable for game loop to true
while run: #Creates Game Loop which allows game to be continously run without being exited out for no reason. If the user closes the window, the game then breaks out of the loop and quits the program
    
    clock.tick(constants.FPS) #Updates the clock according to the FPS

    if start_game==False: #Checks that game hasn't started yet
        screen.fill(constants.CRIMSON) #Fills screen with menu colour

        if menu==True: #Checks if menu is currently the page that should be displayed

            screen.blit(title,(constants.SCREEN_WIDTH//2 - 340,-250)) #Draws title onto screen

            if start_button.draw(screen): # Draws start button and checks if it has been pressed
                menu=False #Menu isn't displayed
                start_game=True #Game should start
                start_intro=True #Starts game intro
                
            if rules_button.draw(screen): # Draws rules button and checks if it has been pressed
                rules=True #Sets variable to true to show rules
                menu=False #Exits menu and shows rules

            if exit_button.draw(screen): # Draws exit button and checks if it has been pressed
                run=False  #Quits the game
            
            if leaderboard_button.draw(screen): # Draws leaderboard button and checks if it has been pressed
                leaderboard=True #Sets variable to true to show leaderboard
                menu=False #Exits menu and shows leaderboard


        elif menu==False and rules==True: #Checks if rules page should be displayed  
            rules,menu=display_rules(rules,menu) #Calls function to display rules onto screen and stores variables returned


        elif menu==False and leaderboard==True: #Checks if leaderboard page should be displayed
            leaderboard,menu=display_leaderboard(leaderboard,menu) #Calls display_leaderboard function to draw usernames and scores onto screen


    elif game_finished==False and start_game==True: #When game hasn't finished but has been started:
    
        if pause_game==True:  #Checks if game has been paused
            screen.fill(constants.CRIMSON) #Fills screen with menu colour
            
            if pause_menu==True: #Checks if pause menu command has been pressed
                
                if resume_button.draw(screen): #Draws resume button and checks if it has been pressed
                    pause_game=False #Sets game to unpaused

                if rules_button.draw(screen): #Draws rules button and checks if it has been pressed
                    rules=True #Takes user to rules page
                    pause_menu=False #pause menu is no longer displayed

                if exit_button.draw(screen): #Draws exit button and checks if it has been pressed
                    run=False #Quits game
            
                if leaderboard_button.draw(screen): #Draws leaderboard button and checks if it has been pressed
                    leaderboard=True #Sets variable to true to show leaderboard page
                    pause_menu=False #Exits menu and shows leaderboard page


            elif pause_menu==False and rules==True: #Checks if rule page should be displayed
                rules,pause_menu=display_rules(rules,menu) #Calls function to display rules onto screen and stores variables returned


            elif pause_menu==False and leaderboard==True: #Checks if leaderboard page should be displayed
                leaderboard,pause_menu=display_leaderboard(leaderboard,pause_menu)#Calls display_leaderboard function to draw usernames and scores onto screen
                

        elif pause_game==False: #When game is unpaused 
            
            screen.fill(constants.L_RED) #Fills the screen with the previously defined colour, light red.

            if player.alive: #Checks if player is alive

                dx=0    #Sets a variable defining how much the x co-ordinate changes by (initially not moving)
                dy=0    #Sets a variable defining how much the y co-ordinate changes by (initially not moving)
                

                if move_right==True:    #Checks whether the user has initiated the procedure to move right
                    dx=constants.SPEED  #dx is set to the speed that the character is allowed to move at to move the character in the positive x direction
                
                if move_left==True:  #Checks whether the user has initiated the procedure to move left 
                    dx=-constants.SPEED #dx is set to the speed that the character is allowed to move at to move the character in the negative x direction
                
                if move_up==True:    #Checks whether the user has initiated the procedure to move up
                    dy=-constants.SPEED #dy is set to the speed that the character is allowed to move at to move the character in the negative y direction (Because y co-ordinate is set to 0 at the top of the screen and increases in value as you move down)
                
                if move_down==True: #Checks whether the user has initiated the procedure to move down
                    dy=constants.SPEED   #dy is set to the speed that the character is allowed to move at to move the character in the positive y direction (Because y co-ordinate is set to 0 at the top of the screen and increases in value as you move down)


                camera_movement,level_complete=player.move(dx,dy,maps.wall_tiles,maps.exit_tile) #Moves the player accross the screen according to the previously defined variables. Recieves where screen should move and whether the level has been completed
                maps.update(camera_movement) #Updates the position of the maps based on the player

                
                for enemy in enemy_list: #Iterates through each enemy
                    
                    fireball=enemy.ai(player,maps.wall_tiles,camera_movement,fireball_image) #Calls the ai function to move enemies, and recieves the fireball created if it was a boss enemy
                    
                    if fireball: #Checks if fireball has been created
                        fireball_group.add(fireball) #Adds fireball to fireball group
                    
                    if enemy.alive: #Checks if enemy is alive
                        health=enemy.update() #Updates enemy with co-ordinates, and recieves enemy's health
                        if health==0: #If enemy health is 0
                            player.score+=2 #Increases player's score by 2
                            enemy_list.remove(enemy) #Remove enemy from screen
            
                player.update() #Updates player details
                arrow=bow.update(player)#Updates bow details according to player's position and recieves arrow created in weapon class

                if arrow: #Checks if arrow has been returned
                    arrow_group.add(arrow) #Arrow is added to arrow group
                
                for arrow in arrow_group: #Iterates through each arrow in group
                    
                    damage, damage_pos = arrow.update(camera_movement,maps.wall_tiles,enemy_list) #Updates details of arrow based on position and collision with walls and enemies. Recieves damage dealt and position of damage text
                    
                    if damage: #Checks if damage is not 0
                        
                        damage_value=DamageValue(damage_pos.centerx, damage_pos.y, str(damage), constants.RED, font) #Creates object of damageValue class, specifying which position the text should appear
                        damage_value_group.add(damage_value) #Updates group with latest damage_value
                

                damage_value_group.update() #Updates damage value group details
                fireball_group.update(camera_movement,player)#Updates fireball group details
                perk_group.update(camera_movement,player) #Updates perk group details

            maps.draw(screen) #Calls draw function for tiles
            player.draw(screen) #Draws player onto the screen 
            bow.draw(screen) #Draws bow onto the screen

            for enemy in enemy_list: #Iterates through enemy list
                enemy.draw(screen)   #Draws enemy onto screen

            for arrow in arrow_group: #Iterates through each arrow inputted
                arrow.draw(screen) #Draws arrow onto screen
            
            for fireball in fireball_group: #Iterates through each fireball
                fireball.draw(screen) #Draws fireball onto screen

            damage_value_group.draw(screen) #Draws damage value group onto screen
            perk_group.draw(screen) #Draws perk group onto screen
            panel() #Calls function to draw panel onto screen
            score_coin.draw(screen) #Draws panel coin onto screen


            if level_complete==True and level!=6: #Checks if  current level has been completed and that it is not the final level
                
                
                start_intro=True #Prompts program to start the screen fade when a new level has been entered
                level+=1 #Increases level by 1
                map_data=new_level() #Resets level after player died       
                maps=Maps() #Creates object of the Maps class so that a new map is created
                maps.process_data(map_data,tile_list,perk_images,sprite_animations) #Calls function to process the data passed as an argument
                temp_hp=player.health   #Creates variable to store player's current health
                temp_score=player.score #Creates variable to store player's current score
                player=maps.player #Creates player in new level
                player.health=temp_hp #Assigns player's new health to original hp
                player.score=temp_score #Assigns player's new score to original score
                enemy_list=maps.character_list #Updates enemy list with enemy list for the map
                score_coin = Perks(constants.SCREEN_WIDTH-175,23,0,coins,True) #Adds a coin at top of the screen to show how many coins have been collected
                perk_group.add(score_coin) #Adds the score coin to the perk group

                for perk in maps.perk_list: #Iterates through each perk in the perk list
                    perk_group.add(perk) #Adds perk to perk group


            elif level_complete==True and level==6: #Checks if final level has been completed
                game_finished=True #Game has been completed


            if start_intro==True: #Checks if the intro fade has been started 
                
                if intro_fade.fade(): #Calls fade method and checks if it is done
                    start_intro=False #Fade has been completed so intro fade shouldn't be started
                    intro_fade.fade_counter=0 #Resets fade counter


            if player.alive==False: #Checks if player has died
                
                if death_fade.fade(): #Checks if death fade has been completed
                    
                    if restart_button.draw(screen): #Draws restart button and checks if it has been pressed
                        
                        death_fade.fade_counter=0 #Resets fade counter
                        start_intro=True #Runs intro before restarting level
                        map_data=new_level() #Resets level after player died       
                        maps=Maps() #Creates object of the Maps class so that a new map is created
                        maps.process_data(map_data,tile_list,perk_images,sprite_animations) #Calls function to process the data passed as an argument for the map
                        player=maps.player #Creates player in new level
                       
                        if level<4:
                            if temp_score-5>=0: #Checks if score will still be positive if 5 is taken away
                                player.score=temp_score-5 #Assigns the score as old score minus 5
                            
                            else: #Checks if negative score would be shown
                                player.score=0 #Resets score to 0
                        if level>=4:
                            if temp_score-10>=0: #Checks if score will still be positive if 10 is taken away
                                player.score=temp_score-10 #Assigns the score as old score minus 10
                            
                            else: #Checks if negative score would be shown
                                player.score=0 #Resets score to 0       

                        temp_score=player.score #Assigns temp_score back to the player's score at the start of the level after restarting
                        enemy_list=maps.character_list #Updates enemy list
                        score_coin = Perks(constants.SCREEN_WIDTH-175,23,0,coins,True) #Adds a coin at top of the screen to show how many coins have been collected
                        perk_group.add(score_coin) #Adds the score coin to the perk group
                        
                        for perk in maps.perk_list: #Iterates through each perk in the perk list
                            perk_group.add(perk) #Adds perk to perk group


    elif game_finished==True: #Checks if game has finished
        
        if death_fade.fade(): #Checks if fade has been completed
            input_rect=pygame.Rect(325,245,200,32) #Creates rectangle for user to enter username into
            for event in pygame.event.get(): #Cycles through events to see if an action has been completed
                
                if event.type==pygame.KEYDOWN: #Checks if any key has been pressed
                    
                    if event.key == pygame.K_BACKSPACE: #Checks if backspace has been pressed
                        username=username[:-1] #Deletes last character
                    
                    else: #Checks if any other key has been pressed
                        username+=event.unicode #Adds character on end of string

            screen.fill(constants.CRIMSON) #Fills screen with crimson colour
            draw_text("Congratulations!",font,constants.WHITE,10,50) #Writes text onto screen
            draw_text(f"You finished with a score of {player.score}",font,constants.WHITE,10,150) #Displays user score onto screen
            draw_text("Enter username: ",font,constants.WHITE,10,250) #Writes text onto screen
            pygame.draw.rect(screen,constants.WHITE,input_rect,2) #Draws the previously defined rectangle onto screen
            text_surface=font.render(username,True,constants.WHITE) #Creates variable to store user input
            screen.blit(text_surface,(input_rect.x + 5,input_rect.y + 5)) #Draws entered characters onto screen
            input_rect.w=max(200,text_surface.get_width()+10) #Adjusts size of text box to fit input
            
            if enter_button.draw(screen): #Checks if enter button has been pressed
                death_fade.fade_counter=0 #Resets fade counter
                try: #Attempts to execute following code:
                    create_table() #Creates new table if it doesn't exist
                
                except sqlite3.OperationalError: #Checks if table is already created
                    pass #Table does not get created 
                
                add_user(username,player.score) #Adds user and their score to a database
                level=1 #Resets level to 1
                map_data=new_level() #Resets levels after player completes game       
                maps=Maps() #Creates object of the Maps class so that a new map is created
                maps.process_data(map_data,tile_list,perk_images,sprite_animations) #Calls function to process the data passed as an argument
                player=maps.player #Creates player in new level
                player.score=0 #Assigns player's new score to 0
                enemy_list=maps.character_list #Updates enemy list
                score_coin = Perks(constants.SCREEN_WIDTH-175,23,0,coins,True) #Adds a coin at top of the screen to show how many coins have been collected
                perk_group.add(score_coin) #Adds the score coin to the perk group
                
                for perk in maps.perk_list: #Iterates through each perk in the perk list
                    perk_group.add(perk) #Adds perk to perk group
                
                    game_finished=False #Game has been reset so 
                start_game=False #User should not be sent straight into level 1
                menu=True #User should be sent to main menu


    for event in pygame.event.get():  #A loop to continously look for any events that have been picked up
        
        if event.type==pygame.QUIT: #Checking if the user has tried to exit the game loop, meaning they want to close the game
            run=False  #Breaks out of the game loop

        if event.type==pygame.KEYDOWN:  #Checks if any keys have been pressed to initiate an action in the game
            
            if event.key==pygame.K_a:   #Checks if the "a" key has been pressed
                move_left=True  #If it has, the movement logic has been set to true to move the character to the left
            
            if event.key==pygame.K_d:   #Checks if the "d" key has been pressed
                move_right=True #If it has, the movement logic has been set to true to move the character to the right
            
            if event.key==pygame.K_w:   #Checks if the "w" key has been pressed
                move_up=True    #If it has, the movement logic has been set to true to move the character up
            
            if event.key==pygame.K_s:   #Checks if the "s" key has been pressed
                move_down=True  #If it has, the movement logic has been set to true to move the character down

            if event.key==pygame.K_ESCAPE: #Checks if escape key has been pressed
                pause_game=True #Sets game to paused

        if event.type==pygame.KEYUP:    #Checks if any keys have been released
            
            if event.key==pygame.K_a:   #Checks if the "a" key has been released
                move_left=False #If it has, the movement logic has been set to false to stop moving the character to the left
            
            if event.key==pygame.K_d:   #Checks if the "d" key has been released
                move_right=False #If it has, the movement logic has been set to false to stop moving the character to the right
            
            if event.key==pygame.K_w:  #Checks if the "w" key has been released
                move_up=False   #If it has, the movement logic has been set to false to stop moving the character up
            
            if event.key==pygame.K_s:   #Checks if the "s" key has been released
                move_down=False #If it has, the movement logic has been set to false to stop moving the character down


    pygame.display.update() #Updates screen with the previousy defined objects 


pygame.quit() #After the game loop has been exited, this is carried out to exit the game