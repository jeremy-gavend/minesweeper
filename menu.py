import pygame
from game import Game
from Class_Buttons import Buttons

def start_menu():
    pygame.init()
    screen_size = (1200,900)
    screen = pygame.display.set_mode(screen_size) 
    running = True
    font_buttons = pygame.font.Font(None, 36)
    start_button = Buttons(font_buttons, coords=(200, (screen_size[1]/2)-45), size=(300,90), text="START", label="TouhouSwepper")
    start_button2 = Buttons(font_buttons, coords=(700, (screen_size[1]/2)-45), size=(300,90), text="START", label="MehdSweeper")

    rect = pygame.Rect(start_button.coords[0], start_button.coords[1], start_button.size[0], start_button.size[1])
    rect2 = pygame.Rect(start_button2.coords[0], start_button2.coords[1], start_button2.size[0], start_button2.size[1])

    while running:
        screen_size = (1200,900)
        screen.fill("white")

        text_render = start_button.text_font.render(start_button.text, True, start_button.text_color)
        text_render2 = start_button.text_font.render(start_button.text, True, start_button.text_color)
        
        rect_text = pygame.Rect(start_button.coords[0] + (start_button.size[0] - text_render.get_width()) / 2, start_button.coords[1] + (start_button.size[1] - text_render.get_height()) / 2, start_button.size[0], start_button.size[1])
        rect_text2 = pygame.Rect(start_button2.coords[0] + (start_button2.size[0] - text_render2.get_width()) / 2, start_button2.coords[1] + (start_button2.size[1] - text_render2.get_height()) / 2, start_button2.size[0], start_button2.size[1])
        
        pygame.draw.rect(screen, start_button.color, rect)
        pygame.draw.rect(screen, start_button2.color, rect2)
        
        screen.blit(text_render, rect_text)
        screen.blit(text_render, rect_text2)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    game = Game()
                    game.start()
                if rect2.collidepoint(event.pos):
                    game = Game()
                    game.start()