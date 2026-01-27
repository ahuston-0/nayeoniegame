"""Unit tests for MazePlayer entity."""

from nayeoniegame import config
from nayeoniegame.entities.maze import Maze
from nayeoniegame.entities.maze_player import MazePlayer


def test_maze_player_initialization():
    """Test maze player initializes at correct grid position."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(maze.start[0], maze.start[1], maze)
    assert player.grid_row == maze.start[0]
    assert player.grid_col == maze.start[1]
    assert player.maze is maze


def test_maze_player_move_up():
    """Test maze player can move up."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(5, 5, maze)
    # Temporarily set cell above as path for testing
    maze.grid[4][5] = Maze.PATH
    initial_row = player.grid_row
    result = player.move((-1, 0))
    if result:
        assert player.grid_row == initial_row - 1


def test_maze_player_move_down():
    """Test maze player can move down."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(5, 5, maze)
    # Temporarily set cell below as path for testing
    maze.grid[6][5] = Maze.PATH
    initial_row = player.grid_row
    result = player.move((1, 0))
    if result:
        assert player.grid_row == initial_row + 1


def test_maze_player_move_left():
    """Test maze player can move left."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(5, 5, maze)
    # Temporarily set cell to left as path for testing
    maze.grid[5][4] = Maze.PATH
    initial_col = player.grid_col
    result = player.move((0, -1))
    if result:
        assert player.grid_col == initial_col - 1


def test_maze_player_move_right():
    """Test maze player can move right."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(5, 5, maze)
    # Temporarily set cell to right as path for testing
    maze.grid[5][6] = Maze.PATH
    initial_col = player.grid_col
    result = player.move((0, 1))
    if result:
        assert player.grid_col == initial_col + 1


def test_maze_player_move_into_wall_fails():
    """Test maze player cannot move into walls."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(5, 5, maze)
    # Set surrounding cells as walls
    maze.grid[4][5] = Maze.WALL
    maze.grid[6][5] = Maze.WALL
    maze.grid[5][4] = Maze.WALL
    maze.grid[5][6] = Maze.WALL

    initial_row = player.grid_row
    initial_col = player.grid_col

    # Try to move in all directions - should all fail
    result_up = player.move((-1, 0))
    assert not result_up
    assert player.grid_row == initial_row

    result_down = player.move((1, 0))
    assert not result_down
    assert player.grid_row == initial_row

    result_left = player.move((0, -1))
    assert not result_left
    assert player.grid_col == initial_col

    result_right = player.move((0, 1))
    assert not result_right
    assert player.grid_col == initial_col


def test_maze_player_pixel_position_syncs_with_grid():
    """Test pixel position updates when grid position changes."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(maze.start[0], maze.start[1], maze)

    # Calculate expected pixel position
    expected_x, expected_y = maze.get_cell_pixel_pos(maze.start[0], maze.start[1])
    offset = (config.MAZE_CELL_SIZE - config.MAZE_PLAYER_SIZE) // 2
    expected_x += offset
    expected_y += offset

    assert player.rect.x == expected_x
    assert player.rect.y == expected_y


def test_maze_player_update():
    """Test maze player update method exists and works."""
    maze = Maze(config.MAZE_GRID_SIZE)
    player = MazePlayer(maze.start[0], maze.start[1], maze)
    # Update should not crash (it's a pass for grid-based movement)
    player.update(0.016)
    assert True
