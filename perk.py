import pygame #Allows pygame modules to be used within perk.py



class Perks(pygame.sprite.Sprite):    #Creates a class to add perks to the game
    

    def __init__(self,x,y,perk_type,animation_list,panel_coin=False): #Passes through arguments that will allow perks to be created
        
        pygame.sprite.Sprite.__init__(self) #Loads in init method from pygame sprite class 
        
        self.perk_type = perk_type #Index 0 will be a coin, and index 1 will be a health potion
        self.animation_list = animation_list #Assigns animation list to animation list passed through
        self.frame_index=0 #Controls what frame of the animation is shown
        self.update_time = pygame.time.get_ticks() #Gets current time        
        self.image = self.animation_list[self.frame_index] #Assigns image based on time
        self.rect = self.image.get_rect() #Creates rectange for perk
        self.rect.center = (x,y) #Positions rectangle
        self.panel_coin=panel_coin #Creates variable for storing the coin at the top of the screen that shouldn't move


    def update(self,camera_movement,player): #Creates function to update perk information
        
        if not self.panel_coin: #Checks that coin moving is not the coin that should stay fixed at the top

            self.rect.x+=camera_movement[0] #Updates the x co-ordinate of perks relative to the screen
            self.rect.y+=camera_movement[1] #Updates the y co-ordinate of perks relative to the screen

        if self.rect.colliderect(player.rect): #Checks if player has walked over perk by checking for collision

            if self.perk_type==0: #Checks if perk is coin
                player.score+=1 #Increases score by 1 for collecting coin
            
            elif self.perk_type == 1: #Checks if perk is potion
                player.health+=10 #Increases player health as reward for collecting potion
                
                if player.health>100: #Checks if the player health has exceeded 100 after collecting the potion
                    player.health=100 #Resets health to 100

            self.kill()  #Gets rid of perk from screen

        animation_cooldown=150 #Sets a cool down so that animations don't run too quickly
        
        self.image=self.animation_list[self.frame_index] #Updates image if frame index is updated

        if pygame.time.get_ticks() - self.update_time > animation_cooldown: #Checks if enough time has passed since last animation
            
            self.frame_index+=1 #Updates frame index for animation
            self.update_time=pygame.time.get_ticks() #Updates the current time
        
        if self.frame_index >= len(self.animation_list): #Checks if animation has finished
            self.frame_index=0 #Resets frame index


    def draw(self,surface): #Creates a function to add perks to the screen
        surface.blit(self.image, self.rect) #Adds perk to screen