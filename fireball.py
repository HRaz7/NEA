import pygame #Allows pygame to be used in the file
import constants #Allows arrow.py to use variables from the constants.py folder
import math #Allows the folder to use functions from the math module



class Fireball(pygame.sprite.Sprite): #Creates a class to add fireballs to the game


    def __init__(self,image,x,y,target_x,target_y): # Constructor for image, taking in required variables
        
        pygame.sprite.Sprite.__init__(self) #Inherits sprite class constructor
        
        self.original_image=image #Stores original non-rotated image as a variable
        
        xdist=target_x-x #Finds the distance between enemy and player in x direction
        ydist=-(target_y-y) #Finds the distance between enemy and player in y direction
        self.angle=math.degrees(math.atan2(ydist,xdist)) #Stores angle needed to rotate by as a variable
        
        self.image=pygame.transform.rotate(self.original_image, self.angle - 90)  #Updates the image by rotating it
        self.rect=self.image.get_rect() #Uses the image to create a rectangle
        self.rect.center=(x,y) #Defines centre of fireball image
        
        self.dx=math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED #Fireball speed depends on the angle in which it's aimed at in x plane
        self.dy=-(math.sin(math.radians(self.angle))) * constants.FIREBALL_SPEED #Fireball speed depends on the angle in which it's aimed at in y plane


    def update(self,camera_movement,player): #Creates function to update game with arrow movement

        self.rect.x+=camera_movement[0] + self.dx #Increases the x co-ordinate by the arrow movement in the x plane and the screen movement in the x plane
        self.rect.y+=camera_movement[1]+self.dy #Increases the y co-ordinate by the arrow movement in the y plane and the screen movement in the y plane

        if self.rect.right < 0 or self.rect.left>constants.SCREEN_WIDTH or self.rect.bottom<0 or self.rect.top>constants.SCREEN_HEIGHT: #Checks if arrow has gone off screen
            self.kill() #If it has, the arrow can be deleted as it no longer needs to exist

        if player.rect.colliderect(self.rect) and player.hit==False: #Checks if fireball has hit player and player is available to be hit 
            player.hit=True #Sets player's hit status to true
            player.last_hit=pygame.time.get_ticks() #Updates last hit variable to current time
            player.health-=10 #Damages player with fireball
            self.kill() #Deletes fireball after contact


    def draw(self,surface):  #A method to draw the arrows onto the screen

        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)),self.rect.centery-int(self.image.get_height()/2))) #Draws the image and sprite rectangle onto the screen
