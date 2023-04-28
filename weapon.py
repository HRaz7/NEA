import pygame #Allows pygame to be used in the file
import math #Allows the folder to use functions from the math module
from arrow import Arrow #Allows the class, Arrow, to be used within weapon.py from arrow.py



class Weapon(): #Creates a class to add weapons to the game
    
    def __init__(self, image, arrow_image):  # Constructor for image
        
        self.original_image=image   #Keeps track of the original image (the weapon)
        self.angle=0 #Defines the amount the image rotates by
        self.image=pygame.transform.rotate(self.original_image, self.angle)  #Updates the image by rotating it
       
        self.arrow_image=arrow_image #Arrow image can now be used as a self. variable in the update section
        self.rect=self.image.get_rect() #Creates a rectangle border for the weapon
       
        self.fired=False #Creates a boolean variable to check if the arrow has been fired
        self.last_shot=pygame.time.get_ticks() #Checks how much time has passed since last click


    def update(self,player): #A method to position the weapon so that it is with the character
        
        shot_cooldown=300 #How much time (in milliseconds) the player needs to wait before shooting again
        arrow=None #Ensures no error is caused if program tries to generate variable arrow that hasn't been defined
        
        self.rect.center=player.rect.center #Causes the center of the weapon and character to be the same

        pos=pygame.mouse.get_pos() #Finds position of mouse on screen
        x_dist=pos[0] - self.rect.centerx #Distance between mouse position and bow centre on x plane
        y_dist=-(pos[1] - self.rect.centery) #Distance between mouse position and bow centre on y plane
        
        self.angle=math.degrees(math.atan2(y_dist,x_dist)) #Rotates bow
        

        if pygame.mouse.get_pressed()[0] and self.fired==False and (pygame.time.get_ticks()-self.last_shot) >= shot_cooldown: #Checks if left mous button has been clicked or if arrow has been fired and if enough time has passed since the user's last shot
            
            arrow=Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle) #Creates the object arrow using the class Arrow
            self.fired=True #After it's been fired, self.fired has been set to true
            self.last_shot=pygame.time.get_ticks() #Resets last_shot variable to the latest shot
        
        if pygame.mouse.get_pressed()[0]==False: #Checks if mouse has been released
            self.fired=False #Resets variable back to false
        
        return arrow #Outputs arrow


    def draw(self,surface):  #A method to draw the weapon onto the screen
        
        self.image=pygame.transform.rotate(self.original_image, self.angle)  #Updates the image by rotating it
        
        surface.blit(self.image,((self.rect.centerx - int(self.image.get_width()/2)),self.rect.centery-int(self.image.get_height()/2))) #Draws the image and sprite rectangle onto the screen