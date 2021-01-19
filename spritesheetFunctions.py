################################
#~~~ Created By: Eric Morse ~~~#
################################
import pygame

class SpriteSheet():
    def __init__(self, spriteSheet):
        # Load the sprite sheet.
        self.spriteSheet = pygame.image.load(spriteSheet).convert()


    def getSprite(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.spriteSheet, (0, 0), (x, y, width, height))
        # Return the image
        return image
