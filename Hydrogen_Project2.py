import pygame  # Import the Pygame library for game development
import random  # Import random for generating random numbers
import os      # Import os for file path management

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Pygame
pygame.init()

# Load background music
pygame.mixer.music.load("Background_sound.wav")  # Load your background music file
pygame.mixer.music.set_volume(0.4)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music on a loop (-1 means loop indefinitely)


# Constants for screen dimensions and other parameters
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 475
CAR_WIDTH = 100
CAR_HEIGHT = 50
BACKGROUND_SPEED = 6
COIN_WIDTH = 30
COIN_HEIGHT = 30
FUEL_CELL_WIDTH = 30
FUEL_CELL_HEIGHT = 30
FUEL_STATION_WIDTH = 200
FUEL_STATION_HEIGHT = 200
ROAD_TOP = SCREEN_HEIGHT - 150
ROAD_BOTTOM = SCREEN_HEIGHT - 11
HALF_SCREEN = 450

# Define colors using RGB tuples
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TRANSLUCENT_BLACK = (0, 0, 0, 200)  # Semi-transparent black for the pop-up background

# Function to load images from the "images" directory
def load_image(filename):
    path = os.path.join("images", filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {os.path.abspath(path)}")
    return pygame.image.load(path)

# Load images for coins, fuel cells, fuel stations, and backgrounds
coin_image = pygame.transform.scale(load_image("Coin2.png"), (COIN_WIDTH, COIN_HEIGHT))
fuel_cell_image = pygame.transform.scale(load_image("Fuel_cell.png"), (FUEL_CELL_WIDTH, FUEL_CELL_HEIGHT))
fuel_station_image = pygame.transform.scale(load_image("pump_transparent 1.png"), (FUEL_STATION_WIDTH, FUEL_STATION_HEIGHT))
start_background = load_image("Background2.JPG")

# Level configuration with different parameters for each level
levels = [
    {'name': "EDMONTON", 'coins': 2, 'fuel_cells': 2, 'background': "Background5.JPG", 'car_image': "car_image.png"},
    {'name': "RED DEER", 'coins': 2, 'fuel_cells': 2, 'background': "RedDeer.png", 'car_image': "image.png"},
    {'name': "CALGARY", 'coins': 2, 'fuel_cells': 2, 'background': "Calgary.png", 'car_image': "large_truck.png"},
    {'name': "REVELSTOKE", 'coins': 2, 'fuel_cells': 2, 'background': "Revelstoke.png", 'car_image': "logging_truck.png"},
    {'name': "VANCOUVER", 'coins': 2, 'fuel_cells': 2, 'background': "Vancouver.png", 'car_image': "Boat_image.png"},
]

# Load sound effects for collecting coins and fuel cells
coin_sound = pygame.mixer.Sound("Coin_voice.wav")
fuel_sound = pygame.mixer.Sound("Fuell_Cell_voice.wav")

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hydrogen Project Game")
clock = pygame.time.Clock()

# Class to represent a fuel cell
class FuelCell:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, FUEL_CELL_WIDTH, FUEL_CELL_HEIGHT)

# Class to represent a fuel station
class FuelStation:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, FUEL_STATION_WIDTH, FUEL_STATION_HEIGHT)

    def update(self):
        self.rect.x -= BACKGROUND_SPEED  # Move left with the background speed

# Function to spawn coins at random positions
def spawn_coins(num_coins):
    coin_positions = []
    while len(coin_positions) < num_coins:
        coin_x = random.randint(HALF_SCREEN, SCREEN_WIDTH - COIN_WIDTH)
        coin_y = random.randint(ROAD_TOP + 10, ROAD_BOTTOM - COIN_HEIGHT - 10)
        new_coin = pygame.Rect(coin_x, coin_y, COIN_WIDTH, COIN_HEIGHT)

        # Ensure new coin does not overlap existing coins
        if all(not new_coin.colliderect(existing_coin) for existing_coin in coin_positions):
            coin_positions.append(new_coin)

    return coin_positions

# Function to spawn fuel cells
def spawn_fuel_cells(num_fuel_cells):
    return [FuelCell(random.randint(HALF_SCREEN, SCREEN_WIDTH - FUEL_CELL_WIDTH),
                     random.randint(ROAD_TOP + 10, ROAD_BOTTOM - FUEL_CELL_HEIGHT - 10)) 
            for _ in range(num_fuel_cells)]

# Function to draw the start menu
def draw_start_menu():
    screen.blit(pygame.transform.scale(start_background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    button_font = pygame.font.Font(None, 48)
    button_text = button_font.render('Start Game', True, WHITE)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
    
    pygame.draw.rect(screen, GREEN, button_rect)  # Draw the button
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))  # Draw button text
    pygame.display.flip()
    
    return button_rect

# Function to draw level selection screen
def draw_level_selection():
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render('Select Level', True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    level_buttons = []
    button_font = pygame.font.Font(None, 36)
    
    for i, level in enumerate(levels):
        button_text = button_font.render(f'Level {i + 1}: {level["name"]}', True, WHITE)
        button_rect = pygame.Rect(100, 100 + i * 60, SCREEN_WIDTH - 200, 50)
        pygame.draw.rect(screen, GREEN, button_rect)  # Draw the level buttons
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))  # Draw button text
        level_buttons.append(button_rect)

    pygame.display.flip()
    return level_buttons

def display_congratulations(level, is_final_level=False):
    font = pygame.font.Font(None, 36)

    # Message to display based on whether it's the final level
    if is_final_level:
        message = """CONGRATULATIONS!
You built 5 Key Hydrogen Fuel stations,
and diployed 5000 Hydrogen Vehicles!

Thank you for playing!"""
    else:
        message = f"""CONGRATULATIONS!
You built a Hydrogen Fuel Station in {level["name"]}!
Giving 1000 Hydrogen Vehicles access.
Upgraded Vehicle for the next level:"""

    box_width = 680
    box_height = 250
    box_padding = 20
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_width // 2, SCREEN_HEIGHT // 2 - box_height // 2, box_width, box_height)

    pygame.draw.rect(screen, BLACK, box_rect)  # Draw the pop-up box
    pygame.draw.rect(screen, TRANSLUCENT_BLACK, box_rect.inflate(10, 10))  # Draw translucent effect

    # Load the next vehicle image if it exists
    next_vehicle_image = None
    if not is_final_level:
        try:
            next_vehicle_image_filename = levels[levels.index(level) + 1]['car_image']
            next_vehicle_image = pygame.transform.scale(load_image(next_vehicle_image_filename), (160, 120))
        except (FileNotFoundError, IndexError) as e:
            print(f"Error: {str(e)}")

    available_height = box_height - 2 * box_padding - (120 if next_vehicle_image else 0)

    # Split the message into lines
    lines = message.split('\n')  # Split by line breaks

    # Render each line of text, ensuring it stays within bounds
    for i, line in enumerate(lines):
        text_surface = font.render(line.strip(), True, WHITE)
        text_rect = text_surface.get_rect(center=(box_rect.centerx, box_rect.centery))
        text_rect.y = box_rect.y + box_padding + i * (font.get_height() + 5)
        if text_rect.y + text_surface.get_height() > box_rect.bottom - box_padding:
            break  # Stop if we exceed the box height
        screen.blit(text_surface, text_rect)

    if next_vehicle_image:
        vehicle_rect = next_vehicle_image.get_rect(center=(box_rect.centerx, box_rect.bottom - 40))
        screen.blit(next_vehicle_image, vehicle_rect)

    pygame.display.flip()  # Update the display
    pygame.time.wait(5000)  # Wait for 5 seconds

    if is_final_level:
        pygame.quit()  # Quit the game if it's the final level
        
# Main function to run the game for a specific level
def main(level_index):
    level = levels[level_index]
    car_x = 0 + CAR_WIDTH
    car_y = ROAD_TOP + 10

    level_background = pygame.transform.scale(load_image(level['background']), (SCREEN_WIDTH, SCREEN_HEIGHT))
    car_image = pygame.transform.scale(load_image(level['car_image']), (CAR_WIDTH, CAR_HEIGHT))

    score = 0
    fuel_collected = 0
    coins = spawn_coins(level['coins'])  # Spawn coins for the level
    fuel_cells = spawn_fuel_cells(level['fuel_cells'])  # Spawn fuel cells for the level
    fuel_station = None  # Initialize fuel station as None

    background_x = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game if the window is closed

        background_x -= BACKGROUND_SPEED  # Move the background
        if background_x <= -SCREEN_WIDTH:
            background_x = 0

        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= 5  # Move car left
        if keys[pygame.K_RIGHT] and car_x < SCREEN_WIDTH - CAR_WIDTH:
            car_x += 5  # Move car right
        if keys[pygame.K_UP] and car_y > ROAD_TOP + 10:
            car_y -= 5  # Move car up
        if keys[pygame.K_DOWN] and car_y < ROAD_BOTTOM - CAR_HEIGHT:
            car_y += 5  # Move car down

        # Draw the background and car
        screen.blit(level_background, (background_x, 0))
        screen.blit(level_background, (background_x + SCREEN_WIDTH, 0))
        screen.blit(car_image, (car_x, car_y))
        car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)  # Create a rectangle for the car

        # Update and draw coins
        for i in range(len(coins) - 1, -1, -1):
            coin = coins[i]
            screen.blit(coin_image, coin.topleft)  # Draw the coin
            if car_rect.colliderect(coin):  # Check if the car collects the coin
                score += 1
                coin_sound.play()  # Play sound for collecting a coin
                coins.pop(i)  # Remove the collected coin
                # Spawn a new coin at a random position
                new_coin = pygame.Rect(random.randint(HALF_SCREEN, SCREEN_WIDTH - COIN_WIDTH),
                                        random.randint(ROAD_TOP + 10, ROAD_BOTTOM - COIN_HEIGHT - 10),
                                        COIN_WIDTH, COIN_HEIGHT)
                coins.append(new_coin)

        # Update and draw fuel cells
        for i in range(len(fuel_cells) - 1, -1, -1):
            fuel_cell = fuel_cells[i]
            screen.blit(fuel_cell_image, fuel_cell.rect.topleft)  # Draw the fuel cell
            if car_rect.colliderect(fuel_cell.rect):  # Check if the car collects the fuel cell
                fuel_collected += 1
                fuel_sound.play()  # Play sound for collecting a fuel cell
                fuel_cells.pop(i)  # Remove the collected fuel cell
                # Spawn a new fuel cell at a random position
                new_fuel_cell = FuelCell(random.randint(HALF_SCREEN, SCREEN_WIDTH - FUEL_CELL_WIDTH),
                                          random.randint(ROAD_TOP + 10, ROAD_BOTTOM - FUEL_CELL_HEIGHT - 10))
                fuel_cells.append(new_fuel_cell)

        # Spawn fuel station logic
        if fuel_collected % 5 == 0 and fuel_collected > 0 and fuel_station is None:
            fuel_station = FuelStation(SCREEN_WIDTH - 100, ROAD_TOP - 150)  # Create a new fuel station

        if fuel_station:
            fuel_station.update()  # Update the fuel station position
            screen.blit(fuel_station_image, fuel_station.rect.topleft)  # Draw the fuel station

            # Check if the fuel station has moved off-screen
            if fuel_station.rect.x < -FUEL_STATION_WIDTH:
                # Display the congratulations pop-up
                if level['name'] == "VANCOUVER":
                    display_congratulations(level, is_final_level=True)  # Final level message
                else:
                    display_congratulations(level)  # Regular level message
                # Start the next level if available
                if level_index + 1 < len(levels):
                    main(level_index + 1)
                return

        # Draw score and level information
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        fuel_text = font.render(f'Fuel Cells Collected: {fuel_collected}', True, BLACK)
        level_text = font.render(f'Level: {level["name"]}', True, BLACK)

        screen.blit(score_text, (10, 10))  # Draw the score
        screen.blit(fuel_text, (10, 50))  # Draw the fuel cells collected
        screen.blit(level_text, (10, 90))  # Draw the current level name

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Limit the frame rate to 30 FPS
        
# Function to run the game loop
def game_loop():
    start_menu = True
    while start_menu:
        button_rect = draw_start_menu()  # Draw the start menu
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_menu = False  # Exit the game if the window is closed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    start_menu = False  # Start the game if the button is clicked
                    level_selection()

    pygame.quit()  # Quit Pygame

# Function to handle level selection
def level_selection():
    level_buttons = draw_level_selection()  # Draw the level selection screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit if the window is closed
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button_rect in enumerate(level_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        main(i)  # Start the selected level

# Start the game
if __name__ == "__main__":
    game_loop()