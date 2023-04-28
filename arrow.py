import pygame #Allows pygame to be used in the file
import constants #Allows arrow.py to use variables from the constants.py folder
import math #Allows the folder to use functions from the math module
import random #Allows the folder to use functions from the random module



class Arrow(pygame.sprite.Sprite): #Creates a class to add arrows to the game

    
    def __init__(self,image,x,y,angle): # Constructor for image, taking in required variables
        
        pygame.sprite.Sprite.__init__(self) #Inherits sprite class constructor
        
        self.original_image=image #Stores original non-rotated image as a variable
        self.angle=angle #Stores angle needed to rotate by as a variable        
        self.image=pygame.transform.rotate(self.original_image, self.angle - 90)  #Updates the image by rotating it
        
        self.rect=self.image.get_rect() #Uses the image to create a rectangle
        self.rect.center=(x,y) #Defines centre of arrow image
        
        self.dx=math.cos(math.radians(self.angle)) * constants.ARROW_SPEED #Arrow speed depends on the angle in which it's aimed at in x plane
        self.dy=-(math.sin(math.radians(self.angle))) * constants.ARROW_SPEED #Arrow speed depends on the angle in which it's aimed at in y plane


    def update(self,camera_movement,wall_tiles,enemy_list): #Creates function to update game with arrow movement
        
        damage=0 #Resets Damage Variable
        damage_pos=None #Resets Damage position variable
        
        self.rect.x+=camera_movement[0] + self.dx #Increases the x co-ordinate by the arrow movement in the x plane and the screen movement in the x plane
        self.rect.y+=camera_movement[1]+self.dy #Increases the y co-ordinate by the arrow movement in the y plane and the screen movement in the y plane

        for wall in wall_tiles: #Iterates through each tile
            
            if wall[1].colliderect(self.rect): #Checks if arrow has collided with wall tile
                self.kill() #Arrow gets deleted

        if self.rect.right < 0 or self.rect.left>constants.SCREEN_WIDTH or self.rect.bottom<0 or self.rect.top>constants.SCREEN_HEIGHT: #Checks if arrow has gone off screen
            self.kill() #If it has, the arrow can be deleted as it no longer needs to exist

        for enemy in enemy_list: #Iterates through each enemy
            
            if enemy.rect.colliderect(self.rect) and enemy.alive: #Checks if there has been a collision between an arrow and an enemy
                
                damage=random.randint(10,20) #Damage varies between 10 and 20 randomly
                damage_pos=enemy.rect #Damage has occured at enemy's position
                enemy.health-=damage #Lowers enemy's health due to damage from arrow
                enemy.hit=True #When player is hit, enemy.hit is set to true so that enemy is stunned
                self.kill()   #Removes arrow from program after it's collided so it doesn't keep moving
                break #Exits loop
        
        return damage, damage_pos #Returns value of damage


    def draw(self,surface):  #A method to draw the arrows onto the screen

        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)),self.rect.centery-int(self.image.get_height()/2))) #Draws the image and sprite rectangle onto the screen
