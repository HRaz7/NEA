import pygame #Allows pygame to be used in file
import math #Allows math operations to be taken out 
import constants #Allows variables from constants to be used
from fireball import Fireball #Allows variables from fireball.py to be used



class Character():  #Creates a class to add character to the game
    

    def __init__(self,x,y,health,sprite_animations,char_type,boss,size):  # Defines initalising funtion for characters
       
        self.boss=boss #If enemy is boss it is given the boss argument

        self.rect=pygame.Rect(0,0,constants.TILE_SIZE*size,constants.TILE_SIZE*size) #Creates rectangle for hit box of characters
        self.rect.center=(x,y) #Additional variable to store rectangle's centre
       
        self.alive=True #Each sprite is alive to begin with
        self.health=health #Creates variable to store the amount of health points that a sprite has
        self.score=0 #Creates Variable for the users score, initally started at 0
        self.flip=False #Creates logic for whether the character should turn around when changing direction. This is initially set to false as the character does not need to be flipped around straight away
        self.running=False  #Player starts off as idle
        
        self.char_type=char_type #Determines which sprite is being chosen, 0 for player, 1 for enemy
        self.animation_list=sprite_animations[char_type] #Creates variable to store animation list for specific character
        self.frame_index=0 #Controls what frame of the animation is shown
        self.action = 0 #When 0 it's idle, when it's 1 it's running
        self.image=self.animation_list[self.action][self.frame_index] #Specifies which image is going to be animated from a specific sub-list

        self.hit=False #Creates varaible to set whether player has been attacked, initially set to False
        self.last_hit=pygame.time.get_ticks() #Creates variable to store how long it's been since last hit
        self.last_attack=pygame.time.get_ticks() #Creates variable to store how long it's been since last attack
        self.stunned=False #Creates variable to represent whether enemy is stunned or not

        self.update_time=pygame.time.get_ticks() #Allows us to see how much time has passed since the last frame and therefore when we need to move onto the next frame


    def move(self,dx,dy,wall_tiles,exit_tile=None):  #Defines function to move character
    
        camera_movement=[0,0] #Sets inital x and y co-ordinates for screen movement relative to the character
        level_complete=False #Level hasn't been completed initially
        self.running=False #Begins with the assumption that the player is not running

        if dx!=0 or dy!=0: #Checks if player is moving
            self.running=True #If he is, then he is running
        
        if dx<0:    #Checks if the direction that the character is moving is negative (moving to the left)
            self.flip=True  #If the condition is true, the character will be flipped to face the negative direction
        
        if dx>0:    #Checks if the direction that the character is moving in is positive (moving to the right)
            self.flip=False  #If the condition is true, the character will be flipped to face the original direction (right)              
        
        if dx!=0 and dy!=0: #Checks if player is moving diagonally
            dx=dx*(math.sqrt(2)/2)  #Sets the movement speed so that moving diagonally doesn't move you twice the normal movement speed
            dy=dy*(math.sqrt(2)/2)  #Sets the movement speed so that moving diagonally doesn't move you twice the normal movement speed
        
        self.rect.x+=dx #Moves the character across the screen by the set amount along the x plane
        
        for wall in wall_tiles: #Iterates through each wall tile
            
            if wall[1].colliderect(self.rect): #Checks if player's rectangle has met tile rectangle
                
                if dx>0: #Checks if collision was on the left side of the tile
                    self.rect.right=wall[1].left #Places character's rectangle on the left of the tile's rectangle
                
                if dx<0: #Checks if collision was on the right side of the tile
                    self.rect.left=wall[1].right #Places character's rectangle on the right of the tile's rectangle
        
        self.rect.y+=dy #Moves the character across the screen by the set amount along the y plane
        
        for wall in wall_tiles: #Iterates through each wall tile
            
            if wall[1].colliderect(self.rect): #Checks if player's rectangle has met tile rectangle
                
                if dy>0: #Checks if collision was on the top side of the tile
                    self.rect.bottom=wall[1].top #Places character's rectangle on the top of the tile's rectangle
                
                if dy<0: #Checks if collision was on the right side of the tile
                    self.rect.top=wall[1].bottom #Places character's rectangle on the bottom of the tile's rectangle

        if self.char_type==0: #Checks if sprite that the camera will follow is the character and not an enemy
        
            if exit_tile[1].colliderect(self.rect): #Checks if player has collided with exit tile
                level_complete=True #Sets level to complete             
                #exit_dist=math.sqrt(((self.rect.centerx-exit_tile[1].centerx)**2)+((self.rect.centery-exit_tile[1].centery)**2)) 
                #Calculates distance from tile
                #if exit_dist<20: #Checks if player is close enough to exit tile to complete level
                    #level_complete=True #Sets level to complete            
            

            if self.rect.right>(constants.SCREEN_WIDTH - constants.SCROLL_THRESH): #Checks if player has moved to the right edge of the screen
                
                camera_movement[0]=constants.SCREEN_WIDTH - constants.SCROLL_THRESH-self.rect.right #Updates x co-ordinate of the screen movement varaible to be relative to how far right the character has gone
                self.rect.right=constants.SCREEN_WIDTH - constants.SCROLL_THRESH #Fixes character's position temporarily so that the character doesn't run off the right edge of the screen

            if self.rect.left<constants.SCROLL_THRESH: #Checks if player has moved to the left edge of the screen
                
                camera_movement[0]=constants.SCROLL_THRESH-self.rect.left #Updates x co-ordinate of the screen movement varaible to be relative to how far left the character has gone
                self.rect.left=constants.SCROLL_THRESH #Fixes character's position temporarily so that the character doesn't run off the left edge of the screen

            if self.rect.bottom>(constants.SCREEN_HEIGHT - constants.SCROLL_THRESH): #Checks if player has moved to the bottom edge of the screen
                
                camera_movement[1]=constants.SCREEN_HEIGHT - constants.SCROLL_THRESH-self.rect.bottom #Updates y co-ordinate of the screen movement varaible to be relative to how far down the character has gone
                self.rect.bottom=constants.SCREEN_HEIGHT - constants.SCROLL_THRESH #Fixes character's position temporarily so that the character doesn't run off the bottom edge of the screen

            if self.rect.top<constants.SCROLL_THRESH: #Checks if player has moved to the top edge of the screen
                
                camera_movement[1]=constants.SCROLL_THRESH-self.rect.top #Updates y co-ordinate of the screen movement varaible to be relative to how far up the character has gone
                self.rect.top=constants.SCROLL_THRESH #Fixes character's position temporarily so that the character doesn't run off the top edge of the screen

        return camera_movement,level_complete #Returns camera movement value and whether the level has been completed to main file


    def update(self): #Defines a function that updates sprite details

        if self.health<=0: #Checks if player's health is negative
            self.health=0 #Sets health to 0 if true
            self.alive=False #Player has died so self.alive is now false
            return self.alive
        
        hit_cooldown=1000 #Sets cooldown time of 1 second
        
        if self.char_type==0: #Only applies to character not enemy
            
            if self.hit==True and (pygame.time.get_ticks() - self.last_hit)>hit_cooldown: #Checks if player has been hit and if enough time has passed since last hit
                self.hit=False #Sets hit variable back to false so player can take damage again

        if self.running == True:    #Checks if sprite is running
            self.update_action(1)   # Changes the animation index to the running animation
        
        else: #If player is not running
            self.update_action(0)   # Changes the animation index to the idle animation

        animation_cooldown=70 #Controls the speed of the animation
        self.image=self.animation_list[self.action][self.frame_index] #Uses latest image from particular sub list
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown: #Checks if enough time has passed since the last update
            self.frame_index += 1 #Moves onto the next frame
            self.update_time =  pygame.time.get_ticks() #Updates to current time 
        
        if self.frame_index >= len(self.animation_list[self.action]): #Checks if all images have been gone through
            self.frame_index=0 #Resets frame index


    def ai(self,player,wall_tiles,camera_movement,fireball_image): #Creates function to keep enemies position unchanged by camera movement
        
        fireball=None #Creates initial variable fireball so it can be returned in all scenarios
        stun_cooldown=150 #Sets a timer for how long enemies should be stunned for
        
        ai_dx=0 #Creates variable for ai movement in the x plane
        ai_dy=0 #Creates variable for ai movement in the y plane

        self.rect.x+=camera_movement[0] #Repositions enemy's x co-ordinate relative to screen
        self.rect.y+=camera_movement[1] #Repositions enemy's y co-ordinate relative to screen

        visibility_line=((self.rect.centerx,self.rect.centery),(player.rect.centerx,player.rect.centery)) #Variable that creates a line between the player and enemy
        
        clipped_line=() #Initialises the clipped line variable to prevent errors so it always exists

        for wall in wall_tiles: #Iterates through each tile
            if wall[1].clipline(visibility_line): #Checks if the visibility lien is blocked by a wall tile
                clipped_line=wall[1].clipline(visibility_line) #Returns line if there is a collision with wall tile

        dist=math.sqrt(((self.rect.centerx-player.rect.centerx)**2)+((self.rect.centery-player.rect.centery)**2)) #Calculates distance away from player

        if not clipped_line and dist>constants.RANGE: #Checks if distance away from player is greater than range and if player is in view of enemy
            
            if self.rect.centerx>player.rect.centerx: #Checks if enemy is to the right of the player
                ai_dx=-constants.ENEMY_SPEED #Moves enemy towards player
            if self.rect.centerx<player.rect.centerx: #Checks if enemy is to the left of the player
                ai_dx=constants.ENEMY_SPEED  #Moves enemy towards player
            if self.rect.centery>player.rect.centery: #Checks if enemy is below the player
                ai_dy=-constants.ENEMY_SPEED #Moves enemy towards player
            if self.rect.centery<player.rect.centery: #Checks if enemy is above the player
                ai_dy=constants.ENEMY_SPEED  #Moves enemy towards player        

        if self.alive: #Only runs the following lines if enemy is not dead

            if not self.stunned: #Checks that enemy is not stunned and can move
                
                self.move(ai_dx,ai_dy,wall_tiles) #Calls the move method to update AI's position
                if dist<constants.ATTACK_RANGE and player.hit==False: #Checks if player is in range to be attacked and if he's not already been hit
                    player.health-=10 #Decreases player health by 10
                    player.hit=True #Player has been hit so variable is set to true
                    player.last_hit=pygame.time.get_ticks() #Resets last time player was hit to current time
                
                fireball_cooldown=1000 #Sets a timer for how much time should be between fireball attacks
                if self.boss: #Checks that the enemy is a boss enemy
                    if dist<400: #Checks that the player and enemy are close enough
                        if (pygame.time.get_ticks() - self.last_attack)>=fireball_cooldown: #Checks if enough time has passed since the last fireball
                            fireball=Fireball(fireball_image,self.rect.centerx,self.rect.centery,player.rect.centerx,player.rect.centery) #Calls fireball function from fireball.py to load fireball
                            self.last_attack=pygame.time.get_ticks() #Resets latest attack to current event

            if self.hit==True: #Checks if enemy has been hit
                    self.hit=False #Resets enemy's status back to not hit
                    self.last_hit=pygame.time.get_ticks() #Updates time of last hit
                    self.stunned=True #Changes enemy's status to stunned
                    self.running=False #Stops enemy running when it is stunned
                    self.update_action(0) #Changes enemy animation to idle

            if (pygame.time.get_ticks() - self.last_hit)>stun_cooldown: #Checks if the stun cooldown period has ended
                    self.stunned=False #Resets enemy's status back to not stunned

        return fireball #Returns the fireball created to where it is called so it can be drawn


    def update_action(self,new_action): #Defines a function to update the action
        
        if new_action != self.action: #Checks if new action is different to previous one
            self.action=new_action #Updates animation settings
            self.frame_index=0 #Resets frame index
            self.update_time=pygame.time.get_ticks() #Sets the time variable to the current time


    def draw(self,surface): # A function is created to draw the image previously defined images onto the screen
        
        flipped_image=pygame.transform.flip(self.image, self.flip, False) #Draws the character onto the screen flipped. self.flip has been put as an argument in the transform.flip section as it will decide whether the variable needs to be flipped or not
        
        if self.char_type==0:
            surface.blit(flipped_image,(self.rect.x,self.rect.y-constants.SCALE * constants.OFFSET))  #Adds the sprite onto the screen
        
        else:
            surface.blit(flipped_image,self.rect)  #Adds the sprite onto the screen