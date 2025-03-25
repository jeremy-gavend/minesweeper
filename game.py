import random
import pygame
from Class_Buttons import Buttons, Tiles, Background, Messages

class Game:
    def __init__(self):
        # Variable for main loop
        self.running = True
        self.game_state = "start"
        self.timer = 0
        self.tiles_remaining = 0
        self.result = ""
        self.tile_size = 20

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

        self.font_buttons = pygame.font.Font(None, 27)
        self.font_numbers = pygame.font.Font(None, 18)
        self.font_messages = pygame.font.Font(None, 27)

        pygame.display.set_caption("Touhou Sweeper")

        # UI Elements
        ## Start screen
        self.start_button = Buttons((self.screen_size[0]/2+9, self.screen_size[1]/2+9), (100,30), "START", self.font_buttons)

        self.difficulty_buttons = {
            "easy": Buttons((self.screen_size[0]/4-50, self.screen_size[1]/4-15), (100,30), "EASY", self.font_buttons, "green"),
            "normal": Buttons((self.screen_size[0]/3-50, self.screen_size[1]/4-15), (100,30), "NORMAL", self.font_buttons),
            "difficult": Buttons((self.screen_size[0]/2-50, self.screen_size[1]/4-15), (100,30), "DIFFICULT", self.font_buttons, "red")
        }
        
        self.info_message = Messages((10, 50), (100, 30), "", self.font_messages)

        ## Game screen
        self.header_messages = {
            "timer": Messages((10, 50), (100, 30), "", self.font_messages),
            "mines": Messages((self.screen_size[0]-100, 50), (100, 30), "", self.font_messages)
        }

        self.grid_background = Background((10,100), "./RectangleSettings.png")
        
        self.tiles_buttons = []        

        ## End screen
        self.back_button = Buttons((self.screen_size[0]/2-50, self.screen_size[1]/2-15), (100,30), "BACK", self.font_buttons,)

        self.end_message = {
            "result": Messages((self.screen_size[0]/3-50, self.screen_size[1]/2-15), (100, 30), "", self.font_messages),
            "end_timer": Messages((10, 50), (100, 30), f"TIME: ", self.font_messages)
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

            pygame.display.flip()

    def check_tiles_remaining(self):
        if not self.tiles_remaining:
            self.result = "win"
            self.game_state = "end"

    def timer_tick(self):
        if self.clock.get_fps() % 60 == 0:
            self.timer += 1

    def difficulty(self, index):
        match index:
            case "easy": 
                return 10, 10, 10
            case "normal":
                return 20, 15, 50
            case "difficult":
                return 20, 20, 99
            
        self.info_message.text = f"Changed difficulty to {index}"
        print(self.info_message.text)

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
                row.append(Tiles((10,100), (self.tile_size, self.tile_size), "0", self.font_numbers))
        return grid

    def place_mines(self, first_tile_coord):
        random_coords = []

        while len(random_coords) < self.total_mines:
            for i in range(self.total_mines - len(random_coords)):
                x = random.randint(0, self.grid_height)
                y = random.randint(0, self.grid_width)
                random_coords.append((x,y))

                # Remove duplicates
                random_coords = set(random_coords)

                # Remove a bomb in the tile played, if any
                try:
                    random_coords.remove(first_tile_coord)
                except:
                    continue

        for coords in random_coords:
            self.grid[coords[0]][coords[1]] = 9

    def show_numbers(self):
        for index_row, row in enumerate(self.grid):
            for index_tile, tile in enumerate(row):
                if tile == 9:
                    continue
                
                number = 0
                for offset_y in range(-1,1):
                    for offset_x in range(-1,1):
                        try: # From top left to bottom right, row by row
                            if self.grid[index_row + offset_y][index_tile + offset_x] == 9:
                                number += 1
                        except:
                            print("Tile is out of bound, skipping")
                            continue
                row[index_tile] = number


                # try:    # Up
                #     if row[index_tile - 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Down
                #     if row[index_tile + 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Left
                #     if self.grid[index_row - 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Right
                #     if self.grid[index_row + 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Up-left
                #     if self.grid[index_row - 1][index_tile - 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Up-right
                #     if self.grid[index_row - 1][index_tile + 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Down-left
                #     if self.grid[index_row + 1][index_tile - 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                # try: # Down-right
                #     if self.grid[index_row + 1][index_tile + 1] == 9:
                #         number += 1
                # except:
                #     print("Tile is out of bound, skipping")
                
    def reveal_next_tile(self, button, index_row, index_button):
        button.visible = True
        self.tiles_remaining -= 1
        self.check_tiles_remaining()
        if button.text == "0":                
            for offset_y in range(-1,1):
                for offset_x in range(-1,1):
                    new_index_row = index_row + offset_y
                    new_index_button = index_button + offset_x
                    try: # From top left to bottom right, row by row
                        self.reveal_next_tile(self.grid[new_index_row][new_index_button])
                    except:
                        print("Tile is out of bound, skipping")
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
                    message.text = f"TIMER: {self.timer}"
                case 'mines':
                    message.text = f"MINES: {self.total_mines}"

            message.draw(self)

        # Display the playable grid
        for row in self.tiles_buttons:
            for tile in row:
                tile.draw(self)

        self.timer_tick()
        
    def end_screen(self):
        #Still display the grid, but is not interactable
        for row in self.tiles_buttons:
            for tile in row:
                tile.draw(self)

        for index, message in self.end_message.items():
            match index:
                case "result":
                    if self.result == "win":
                        message.text = "YOU WIN! Congrats. Heh."
                    else:
                        message.text = "YOU LOSE! You're so bad. Ha!"
                case "end_timer":
                    message.text = f"FINAL TIME: {self.timer}"
            message.draw(self)

    def event(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.rect.collidepoint(event.pos):                
                        self.game_init()
                        self.grid = self.create_grid()
                        self.tiles_buttons = self.create_tiles()
                        self.screen_size = (300 + self.tile_size * self.grid_width, 100 + self.tile_size * self.grid_height)
                        self.screen = pygame.display.set_mode(self.screen_size)
                        self.game_state = "game"
                    for index, button in self.difficulty_buttons.items():
                        if button.rect.collidepoint(event.pos):
                            self.grid_height, self.grid_width, self.total_mines = self.difficulty(index)
                            
            if self.game_state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for index_row, rows in enumerate(self.tiles_buttons):
                        for index_button, button in enumerate(rows):
                            if self.start_button.rect.collidepoint(event.pos):
                                if not self.mine_placed:
                                    self.place_mines(button.coords)
                                    for rows in self.tiles_buttons:
                                        for button in rows:
                                            button.text = str(self.grid[button.coords[0]][button.coords[1]])
                                    self.mine_placed = True
                                if button.text == "9":
                                    # TODO add visible effect without self.visible
                                    self.visible = True
                                    self.game_state = "end"
                                    self.result = "lose"
                                    break
                                self.reveal_next_tile(button, index_row, index_button)
                                

            if self.game_state == "end":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.rect.collidepoint(event.pos):
                        self.game_state = "start"

    # TODO add background in button
    # TODO add flags and ?, making an exception in reveal_next_tile + add a property to Tile()