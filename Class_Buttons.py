import pygame

class Buttons:
    def __init__(self, coords, size, text, text_font, text_color = 'black', link_to = ''):
        self.coords = coords
        self.size = size
        self.text = text
        self.link_to = link_to

        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.text_render = text_font.render(self.text, True, text_color)

    def draw(self, game):
        game.screen.blit(self.text_render, self.rect)

class Tiles(Buttons):
    def __init__(self, coords, size, text, text_font, text_color='black', link_to=''):
        super().__init__(coords, size, text, text_font, text_color, link_to)
        self.active = False

    def draw(self, game):
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
    def __init__(self, coords, size, text, text_font, color = 'black'):
        self.coords = coords
        self.size = size
        self.variable = ''
        self.text = text
        self.text_font = text_font
        
        self.color = color
        
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])

    def draw(self, game):
        self.final_text = self.text + self.variable
        
        self.text_render = self.text_font.render(self.final_text, True, self.color)
        game.screen.blit(self.text_render, self.rect)