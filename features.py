import pygame #Imports the pygame library allowing me to use its features within my code
import constants #Allows features.py to use variables from the constants.py folder



class DamageValue(pygame.sprite.Sprite): #Creates class for dealing with damage text
    

    def __init__(self,x,y,damage,colour,font): #Initialises function for damage text
        
        pygame.sprite.Sprite.__init__(self) #Loads in init method from pygame sprite class 
        self.image=font.render(damage,True,colour) #Passes in varaibles to define what is being displayed as well as its colour
        self.rect=self.image.get_rect() #Creates rectangle for text to be in
        self.rect.center=(x,y) #Variable for center of text
        self.counter = 0 #Creates counter for how long damage text has appeared for


    def update(self): #Creates function to update position of damage text
        
        self.rect.y-=2 #Moves damage text up after being outputted
        self.counter+=1 #Increments counter
        
        if self.counter > 30: #Checks if counter has been more than 3 seconds
            self.kill() #Gets rid of damage text



class ScreenFade(): #Creates class for creating a screen fade inbetween levels

    def __init__(self,category,colour,speed,screen): #Creates initiallising function for the screen fade

        self.category=category #Assigns category of fade to a fade variable, 1=intro fade, 2=death fade
        self.colour=colour #Assigns colour of the fade to a colour variable
        self.speed=speed #Assigns speed of the fade to a speed variable
        self.screen=screen #Assigns screen that the fade is drawn on to a variable
        self.fade_counter=0 #Assigns a variable to keep track of where the fade should be at a certain point in the direction


    def fade(self): #Creates function to perform the action of the fade
        
        fade_completed=False #Initially sets the fade to not completed
        self.fade_counter+=self.speed #Adds speed to the fade counter so the black rectangle can move across the screen
        
        if self.category==1: #Checks if it is the intro fade
            
            pygame.draw.rect(self.screen,self.colour,(0-self.fade_counter,0,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT)) #Draws rectangle on the left side moving left, initially covering half the screen
            pygame.draw.rect(self.screen,self.colour, (constants.SCREEN_WIDTH//2+self.fade_counter,0,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)) #Draws rectangle on the right side moving right, initially covering half the screen
            pygame.draw.rect(self.screen,self.colour,(0,0-self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT//2)) #Draws rectangle on the top side moving up, initially covering half the screen
            pygame.draw.rect(self.screen,self.colour,(0,constants.SCREEN_HEIGHT//2+self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT)) #Draws rectangle on the bottom side moving down, initially covering half the screen

        elif self.category==2: #Checks if fade called is a death fade
            pygame.draw.rect(self.screen,self.colour,(0,0,constants.SCREEN_WIDTH,0+self.fade_counter)) #Draws rectangle falling from top of screen
            
        if self.fade_counter>=constants.SCREEN_WIDTH:   #Checks if the black rectangle has passed across the screen
            fade_completed=True #The fade has been completed so variable is set to true

        return fade_completed #Returns whether the fade has been completed or not