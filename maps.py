import constants #Allows varaibles from the constants.py file to be used in maps.py
from character import Character #Allows the Character class from character.py to be used in maps.py
from perk import Perks #Allows the Perks class from perk.py to be used in maps.py


class Maps(): #Creates class for tiles
    
    def __init__(self): #Constructor for tiles
        
        self.maps_tiles=[] #Creates a list for mapping tiles to grid squares
        self.wall_tiles=[] #Creates a list to seperate wall tiles from floor and other tiles
        self.exit_tile=None #Since there will be one tile to exit the level, a variable is created to represent it. Before it is found, it is set to "None"
        self.perk_list=[] #List that will store all perks to be added onto the map
        self.character_list=[] #Creates empty list to store all characters (including enemies)
        self.player=None #Since there will be one tile that the character spawns on, a variable is created to represent it. Before it is found, it is set to "None"


    def process_data(self, data, tile_list, perk_images, sprite_animations): #Creates function for processing tile data
        
        self.level_lenth=len(data) #The length of the data must be stored so that the processing can automated
        
        for y, row in enumerate(data): #Iterates through each value in the level data file, sets the value of the iteration as an y co-ordinate
            
            for x, tile in enumerate(row): #Iterates through each perk in the sub list(row) in the list data, sets the value of the iteration as an x co-ordinate
                
                image=tile_list[tile] #Assigns image to each perk in sublist
                image_rect=image.get_rect() #Sets rectangle of tile to variable

                image_x=x*constants.TILE_SIZE #Scales x co-ordinate by the tile size 
                image_y=y*constants.TILE_SIZE #Scales y co-ordinate by the tile size 

                image_rect.center=(image_x,image_y) #Uses x and y to store the co-ordinates of an images' center
                tile_data=[image,image_rect,image_x,image_y] #Sets information of tile to a variable in a list
                

                if tile==7: #Checks if tile is wall tile
                    self.wall_tiles.append(tile_data) #Adds wall tile to wall tile list
                
                elif tile==8: #Checks if tile is exit tile
                    self.exit_tile=tile_data #Sets the current tile as the exit tile
                
                elif tile==9: #Checks if tile is a coin tile
                    
                    coin=Perks(image_x,image_y,0,perk_images[0]) #Creates coin using image constructor which is placed on map
                    self.perk_list.append(coin) #Adds coin to perk list
                    tile_data[0]=tile_list[0] #Replaces the floor of coin tiles to the basic floor tile
                
                elif tile==10: #Checks if tile is a potion tile
                    
                    potion=Perks(image_x,image_y,1,[perk_images[1]]) #Creates coin using image constructor which is placed on map
                    self.perk_list.append(potion) #Adds coin to perk list
                    tile_data[0]=tile_list[0] #Replaces the floor of coin tiles with the basic floor tile
                
                elif tile==11: #Checks if tile is for the player to spawn on
                    
                    player=Character(image_x,image_y,100,sprite_animations,0,False,0.75)#Uses character class to create object.Loads images from "sprite_animations" list
                    self.player=player #Sets self.player to the player that was just created
                    tile_data[0]=tile_list[0] #Replaces floor beneath character with floor tile

                elif tile>=12 and tile<=16: #Checks if tile is for common enemy to spawn on
                    
                    enemy=Character(image_x,image_y,60,sprite_animations,tile-11,False,1) #Uses class to create enemy object
                    self.character_list.append(enemy) #Adds enemy to the character list created
                    tile_data[0]=tile_list[0] #Replaces floor beneath enemy with floor tile

                elif tile==17: #Checks if tile is for boss to spawn on
                    
                    enemy=Character(image_x,image_y,200,sprite_animations,6,True,2) #Uses class to create enemy object
                    self.character_list.append(enemy) #Adds enemy to the character list created
                    tile_data[0]=tile_list[0] #Replaces floor beneath enemy with floor tile

                if tile>=0: #Checks if the current perk is not empty space
                    self.maps_tiles.append(tile_data) #Adds image data to main tiles list


    def update(self,camera_movement): #Creates function to update position of tiles on screen so that the it moves relative to the character
        
        for tile in self.maps_tiles: #Iterates through each tile
            
            tile[2]+=camera_movement[0] #Updates the tile's x co-ordinate by adding the current x co-ordinate of the screen
            tile[3]+=camera_movement[1] #Updates the tile's y co-ordinate by adding the current y co-ordinate of the screen
            tile[1].center=(tile[2],tile[3]) #Updates the position of the rectangle of the tile's center

    
    def draw(self,surface): #Creates a function to draw tiles onto screen
        
        for tile in self.maps_tiles: #Iterates through each tile in the main list
            surface.blit(tile[0],tile[1]) #Draws tile and tile rectange which are at index 0 and 1 respectively