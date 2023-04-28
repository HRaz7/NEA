import pygame   #Allows pygame to be used in file
import time #Allows functions of time to be used in the file



class Button(): #Creates a class to add buttons to the game
    
    
    def __init__(self,x,y,image): #Creates a method for initalising buttons
        
        self.image=image #Creates variable to store button image
        self.rect=self.image.get_rect() #Creates variable to store button image rectangle
        self.rect.topleft=(x,y) #Creates variable to store co-ordinates of rect


    def draw(self,surface): #Creates a method for drawing buttons onto screen
        
        clicked=False #Variable for deciding whether button has been pressed
        pos=pygame.mouse.get_pos() #Creates variable for storing position of mouse on screen
        
        if self.rect.collidepoint(pos): #Checks if mouse is hovering above button
            
            if pygame.mouse.get_pressed()[0]: #Checks if left mouse button has been clicked while mouse is hovering over button
                time.sleep(0.2) #Pauses game for fraction of a second so mouse click isn't registered twice.
                clicked=True #Sets clicked to true meaning button has been pressed

        surface.blit(self.image,self.rect) #Draws image and its rectangle onto screen
        
        return clicked #Returns whether button has been pressed or not