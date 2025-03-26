import pygame

class Buttons:
    def __init__(self, coords, size, text, text_font, text_color = 'black'):
        self.coords = coords
        self.size = size
        self.text = text

        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.text_render = text_font.render(self.text, True, text_color)

    def draw(self, game):
        pygame.draw.rect(game.screen, "gray", self.rect)
        game.screen.blit(self.text_render, self.rect)


class Tiles(Buttons):
    def __init__(self, coords, size, text, text_font, text_color='black'):
        super().__init__(coords, size, text, text_font, text_color)
        self.active = False

    def draw(self, game):
        pygame.draw.rect(game.screen, "gray", self.rect)
        if self.active:
            game.screen.blit(self.text_render, self.rect)
        

    

class Background:
    def __init__(self, coords, img_link):
        self.coords = coords
        self.size = (0, 0)
        self.img_link = img_link

        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])
        self.img = pygame.image.load(img_link)
            
    def draw(self, game, size):
        self.size = size
        self.img_render = pygame.transform.scale(self.img, self.size)
        game.screen.blit(self.img_render, self.rect)

class Messages:
    def __init__(self, coords, size, text, text_font, color = 'black', set_timeout = False):
        self.coords = coords
        self.size = size
        self.text = text
        self.text_font = text_font
        
        self.color = color
        
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])

        self.set_timeout = set_timeout
        self.timeout = 0

    def draw(self, game):
        # Make message disappear after set frames
        if not self.text or self.text != self.previous_text:
            self.timeout = 200
            self.previous_text = self.text
        if self.timeout == 0:
            self.text = ''

        if self.timeout > 0:
            self.text_render = self.text_font.render(self.text, True, self.color)
            game.screen.blit(self.text_render, self.rect)
        
        if self.set_timeout:
            self.timeout -= 1                
            