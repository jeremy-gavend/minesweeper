import random
import pygame
from Class_Buttons import Buttons, Tiles, Background, Messages

class Game:
    def __init__(self):
        # Variable for main loop
        self.running = True
        self.game_state = "start"
        self.timer = 0
        self.counter = 0
        self.tiles_remaining = 0
        self.result = ""
        self.tile_size = 40
        self.number_colors = ["gray", "blue", "green", "yellow", "orange", "red", "magenta", "indigo", "black"]

        # Variables for launching the game
        self.grid_height = 0
        self.grid_width = 0
        self.total_mines = 0

        self.grid = self.create_grid()
        self.mine_placed = False

        # Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_size = (1200,900)
        self.screen = pygame.display.set_mode(self.screen_size) 

        self.font_buttons = pygame.font.Font(None, 36)
        self.font_numbers = pygame.font.Font(None, 20)
        self.font_messages = pygame.font.Font(None, 36)

        pygame.display.set_caption("Touhou Sweeper")

        # UI Elements
        ## Start screen
        self.start_button = Buttons(self.font_buttons, coords=((self.screen_size[0]/2)-150, (self.screen_size[1]/2)-45), size=(300,90), text="START")

        self.difficulty_buttons = {
            "easy": Buttons(self.font_buttons, coords=(200, self.screen_size[1]-50), size=(150,45), text="EASY", text_color ="green"),
            "normal": Buttons(self.font_buttons, coords=(400, self.screen_size[1]-50), size=(150,45), text="NORMAL"),
            "difficult": Buttons(self.font_buttons, coords=(600, self.screen_size[1]-50), size=(150,45), text="DIFFICULT", text_color="red")
        }
        
        self.info_message = Messages((100, 30), self.font_messages, set_timeout=True, coords=(10, 50), text='')

        ## Game screen
        self.header_messages = {
            "timer": Messages((100, 30), self.font_messages, coords=(10, 50)),
            "mines": Messages((100, 30), self.font_messages)
        }

        self.grid_background = Background((10,100), "./RectangleSettings.png")
        
        self.tiles_buttons = []        

        ## End screen
        self.back_button = Buttons(self.font_buttons, text="BACK", size=(100,30))

        self.end_message = {
            "result": Messages((100, 30), self.font_messages),
            "end_timer": Messages((10, 50), self.font_messages, coords=(self.screen_size[0]/3-50, 30+self.screen_size[1]/2-15), text=f"TIME: ")
        }       

    def start(self):
        while self.running:
            self.screen.fill("white")
            self.event()

            match self.game_state:
                case 'start':
                    self.start_screen()
                case 'game':
                    self.game_screen()
                case 'end':
                    self.end_screen()

            self.clock.tick(60)
            self.counter += 1
            pygame.display.flip()

    def check_tiles_remaining(self):
        print(f"Remaining:{self.tiles_remaining}")
        if not self.tiles_remaining:
            self.result = "win"
            self.game_state = "end"

    def timer_tick(self):
        if self.counter % 60 == 0:
            self.timer += 1

    def difficulty(self, index):
        self.info_message.text = f"Changed difficulty to {index}"
        
        match index:
            case "easy": 
                return 10, 10, 10
            case "normal":
                return 20, 15, 50
            case "difficult":
                return 20, 20, 99
            
    def game_init(self):
        self.mine_placed = False
        self.timer = 0
        self.result = ""
        self.tiles_remaining = (self.grid_height * self.grid_width) - self.total_mines

    def create_grid(self):
        grid = []
        for i in range(self.grid_height):
            row = []
            for j in range(self.grid_width):
                row.append(0)
            grid.append(row)
        return grid

    def create_tiles(self):
        grid = []
        for i in range(self.grid_height):
            row = []
            for j in range(self.grid_width):
                row.append(Tiles(self.font_numbers, coords=(self.screen_size[0]/4+(self.tile_size+1)*j,100+(self.tile_size+1)*i), size=(self.tile_size, self.tile_size), text="0"))
            grid.append(row)
        return grid

    def place_mines(self, first_tile_coord):
        random_coords = set([])

        while len(random_coords) < self.total_mines:
            for i in range(self.total_mines - len(random_coords)):
                x = random.randint(0, self.grid_height-1)
                y = random.randint(0, self.grid_width-1)

                # Remove a bomb in the tile played, if any
                try:
                    random_coords.add((x,y))
                    random_coords.remove(first_tile_coord)
                except:
                    continue
        print(random_coords)

        for coords in random_coords:
            self.grid[coords[0]][coords[1]] = 9

    def set_numbers(self):
        for index_row, row in enumerate(self.grid):
            for index_tile, tile in enumerate(row):
                if tile == 9:
                    continue
                
                number = 0
                for offset_y in range(-1,2):
                    for offset_x in range(-1,2):
                        if index_row + offset_y < 0 or index_tile + offset_x < 0:
                            continue
                        print(f"y={index_row + offset_y}, x={index_tile + offset_x}")
                        try: # From top left to bottom right, row by row
                            if self.grid[index_row + offset_y][index_tile + offset_x] == 9:
                                number += 1
                        except:
                            print("Numbers: Tile is out of bound, skipping")
                            continue
                self.grid[index_row][index_tile] = number

    def show_numbers(self):
        for index_y, rows in enumerate(self.tiles_buttons):
            for index_x, button in enumerate(rows):
                button.text = str(self.grid[index_y][index_x])
                for i in range(9):
                    if button.text == str(i):
                        button.text_color = self.number_colors[i]
                
    def reveal_next_tile(self, button, index_row, index_button):
        if not button.state:
            button.state = "visible"
            self.tiles_remaining -= 1
            if button.text == "0":
                for offset_y in range(-1,2):
                    for offset_x in range(-1,2):
                        if index_row + offset_y < 0 or index_button + offset_x < 0:
                            continue
                        new_index_row = index_row + offset_y
                        new_index_button = index_button + offset_x
                        try: # From top left to bottom right, row by row                        
                            self.reveal_next_tile(self.tiles_buttons[new_index_row][new_index_button], new_index_row, new_index_button)
                        except IndexError:
                            print("Reveal: Tile is out of bound, skipping")
                            continue

    def start_screen(self):
        # Draw "START" button
        self.start_button.draw(self)
        
        # Draw all difficulty buttons
        for button in self.difficulty_buttons.values():
            button.draw(self)

        self.info_message.draw(self)

    def game_screen(self):
        # Draw all the header messages (timer and bombs)
        self.grid_background.draw(self, (self.screen_size[0]-10, self.screen_size[1]-100))

        for index, message in self.header_messages.items():
            match index:
                case "timer":
                    message.draw(self, text = f"TIMER: {self.timer}")
                case "mines":
                    message.draw(self, coords=(self.screen_size[0]-150, 50), text = f"MINES: {self.total_mines}")

            message.draw(self)
        
        self.back_button.draw(self, coords=(self.screen_size[0]/2-50, 10))

        # Display the playable grid
        for row in self.tiles_buttons:
            for tile in row:
                tile.draw(self)

        self.timer_tick()
        
    def end_screen(self):
        #Still display the grid, but is not interactable
        
        self.back_button.draw(self, coords=(self.screen_size[0]/2-50, 10))

        for row in self.tiles_buttons:
            for tile in row:
                tile.draw(self)

        for index, message in self.end_message.items():
            match index:
                case "result":
                    if self.result == "win":
                        message.draw(self, coords=(self.screen_size[0]/3-50, self.screen_size[1]/2-15), text="YOU WIN! Congrats. Heh.")
                    else:
                        message.draw(self, coords=(self.screen_size[0]/3-50, self.screen_size[1]/2-15), text="YOU LOSE! You're so bad. Ha!")
                case "end_timer":
                    message.draw(self, text=f"FINAL TIME: {self.timer}")

    def event(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.rect.collidepoint(event.pos):                
                        self.game_init()
                        self.grid = self.create_grid()
                        self.screen_size = (310 + (self.tile_size+1) * self.grid_width, 110 + (self.tile_size+1) * self.grid_height)
                        self.tiles_buttons = self.create_tiles()
                        self.screen = pygame.display.set_mode(self.screen_size)
                        self.game_state = "game"
                    for index, button in self.difficulty_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            self.grid_height, self.grid_width, self.total_mines = self.difficulty(index)
                            
            elif self.game_state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index_row, rows in enumerate(self.tiles_buttons):
                        for index_button, button in enumerate(rows):
                            if button.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    if not button.state:
                                        if not self.mine_placed:
                                            self.place_mines((index_button, index_row))
                                            self.set_numbers()
                                            self.show_numbers()
                                            self.mine_placed = True
                                        if button.text == "9":
                                            # TODO add visible effect without self.visible (for bomb image)
                                            button.state = "visible"
                                            self.game_state = "end"
                                            self.result = "lose"
                                            break
                                        self.reveal_next_tile(button, index_row, index_button)
                                        self.check_tiles_remaining()
                                if event.button == 3:
                                    match button.state:
                                        case None:
                                            button.state = "flag"
                                        case "flag":
                                            button.state = "?"
                                        case "?":
                                            button.state = None
                    if self.back_button.rect.collidepoint(event.pos):
                        self.screen = pygame.display.set_mode((1200, 900))
                        self.game_state = "start"
                        
            elif self.game_state == "end":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.rect.collidepoint(event.pos):
                        self.screen = pygame.display.set_mode((1200, 900))
                        self.game_state = "start"

    # TODO add background in button
    # TODO add flags and ?, making an exception in reveal_next_tile + add a property to Tile()