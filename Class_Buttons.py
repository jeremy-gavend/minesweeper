import pygame

class Buttons:
    def __init__(self, text_font, color = 'gray', text_color = 'black', **kwargs):
        self.__dict__.update(kwargs)
        
        self.color = color
        self.text_font = text_font
        self.text_color = text_color
        
    def draw(self, game, **kwargs):
        self.__dict__.update(kwargs)

        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])
        pygame.draw.rect(game.screen, self.color, self.rect)
        
        self.text_render = self.text_font.render(self.text, True, self.text_color)
        self.rect_text = pygame.Rect(self.coords[0] + (self.size[0] - self.text_render.get_width()) / 2, self.coords[1] + (self.size[1] - self.text_render.get_height()) / 2, self.size[0], self.size[1])
        game.screen.blit(self.text_render, self.rect_text)


# class Buttons:
#     def __init__(self, coords, size, text, text_font, text_color = 'black'):
#         self.coords = coords
#         self.size = size
#         self.text = text

#         self.text_render = text_font.render(self.text, True, text_color)

#     def draw(self, game):
#         self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])

#         pygame.draw.rect(game.screen, "gray", self.rect)
#         game.screen.blit(self.text_render, self.rect)


class Tiles(Buttons):
    def __init__(self, text_font, text_color = "green", **kwargs):
        super().__init__(text_font, text_color, **kwargs)
        self.__dict__.update(kwargs)

        self.flag_image_path = ''
        self.mark_image_path = ''
        self.color = "gray"
        self.state = None

    def draw(self, game, **kwargs):
        self.__dict__.update(kwargs)

        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])
        pygame.draw.rect(game.screen, self.color, self.rect)
            
        match self.state:
            case "visible":
                self.color = "lightgray"
                self.text_render = self.text_font.render(self.text, True, self.text_color)
                self.rect_text = pygame.Rect(self.coords[0] + (self.size[0] - self.text_render.get_width()) / 2, self.coords[1] + (self.size[1] - self.text_render.get_height()) / 2, self.size[0], self.size[1])
                game.screen.blit(self.text_render, self.rect_text)
        
            case "flag":
                self.color = "red"
                if self.flag_image_path:
                    img = pygame.image.load(self.flag_image_path)
                    img_render = pygame.transform.scale(img, self.size)
                    game.screen.blit(img_render, self.rect)
                    
            case "?":
                self.color = "green"
                if self.mark_image_path:
                    img = pygame.image.load(self.mark_image_path)
                    img_render = pygame.transform.scale(img, self.size)
                    game.screen.blit(img_render, self.rect)
            case _:
                self.color = "gray"

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
    def __init__(self, size, text_font, color = 'black', set_timeout = False, **kwargs):
        self.__dict__.update(kwargs)

        self.size = size
        self.text_font = text_font
        
        self.color = color
        
        self.set_timeout = set_timeout
        self.timeout = 0
        self.previous_text = ''


    def draw(self, game, **kwargs):
        self.__dict__.update(kwargs)

        # Make message disappear after set frames
        if not self.text or self.text != self.previous_text:
            self.timeout = 200
            self.previous_text = self.text
        if self.timeout == 0:
            self.text = ''
            
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.size[0], self.size[1])

        if self.timeout > 0:
            self.text_render = self.text_font.render(self.text, True, self.color)
            game.screen.blit(self.text_render, self.rect)
        
        if self.set_timeout:
            self.timeout -= 1                
            