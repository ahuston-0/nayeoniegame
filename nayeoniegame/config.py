"""Game configuration constants."""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Game title
TITLE = "Nayeonie Game"

# Minigame: Color Collector
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 400
CIRCLE_RADIUS = 15
CIRCLE_FALL_SPEED = 150  # Initial speed
CIRCLE_SPAWN_INTERVAL = 1.5  # Seconds between spawns
MAX_LIVES = 3

# Minigame: Maze Runner
# Difficulty is controlled by MAZE_CELL_SIZE:
#   30 = Easy (17x17 grid, ~127 path cells)
#   25 = Medium (21x21 grid, ~199 path cells) - DEFAULT
#   20 = Hard (27x27 grid, ~337 path cells)
MAZE_CELL_SIZE = 25  # Pixel size of each grid cell (smaller = harder maze)
MAZE_GRID_SIZE = 21  # Number of cells in each dimension (must be odd for proper generation)
# Calculated offsets to center the maze
MAZE_OFFSET_X = (800 - MAZE_GRID_SIZE * MAZE_CELL_SIZE) // 2  # Center horizontally
MAZE_OFFSET_Y = 20  # Y offset for maze (starts below timer)
MAZE_PLAYER_SIZE = int(MAZE_CELL_SIZE * 0.8)  # Visual size of player (80% of cell)
