"""Unit tests for Maze entity."""

from collections import deque

from nayeoniegame import config
from nayeoniegame.entities.maze import Maze


def test_maze_initialization():
    """Test maze initializes correctly."""
    maze = Maze(config.MAZE_GRID_SIZE)
    assert maze.size == config.MAZE_GRID_SIZE
    assert len(maze.grid) == config.MAZE_GRID_SIZE
    assert len(maze.grid[0]) == config.MAZE_GRID_SIZE


def test_maze_start_is_path():
    """Test start position is a path."""
    maze = Maze(config.MAZE_GRID_SIZE)
    assert maze.grid[maze.start[0]][maze.start[1]] == Maze.PATH


def test_maze_goal_is_path():
    """Test goal position is a path."""
    maze = Maze(config.MAZE_GRID_SIZE)
    assert maze.grid[maze.goal[0]][maze.goal[1]] == Maze.PATH


def test_maze_has_walls_and_paths():
    """Test maze has both walls and paths."""
    maze = Maze(config.MAZE_GRID_SIZE)
    has_wall = False
    has_path = False

    for row in maze.grid:
        for cell in row:
            if cell == Maze.WALL:
                has_wall = True
            elif cell == Maze.PATH:
                has_path = True

    assert has_wall, "Maze should have at least one wall"
    assert has_path, "Maze should have at least one path"


def test_maze_is_valid_move_wall():
    """Test is_valid_move returns False for walls."""
    maze = Maze(config.MAZE_GRID_SIZE)
    # Borders are always walls
    assert not maze.is_valid_move(0, 0)


def test_maze_is_valid_move_path():
    """Test is_valid_move returns True for paths."""
    maze = Maze(config.MAZE_GRID_SIZE)
    # Start position should always be a valid move
    assert maze.is_valid_move(maze.start[0], maze.start[1])


def test_maze_is_valid_move_out_of_bounds():
    """Test is_valid_move returns False for out of bounds."""
    maze = Maze(config.MAZE_GRID_SIZE)
    assert not maze.is_valid_move(-1, 0)
    assert not maze.is_valid_move(0, -1)
    assert not maze.is_valid_move(maze.size, 0)
    assert not maze.is_valid_move(0, maze.size)


def test_maze_solvability():
    """Test generated maze is solvable (path exists from start to goal)."""
    maze = Maze(config.MAZE_GRID_SIZE)

    # Use BFS to find path from start to goal
    queue = deque([maze.start])
    visited = {maze.start}

    while queue:
        current = queue.popleft()
        if current == maze.goal:
            # Found path!
            assert True
            return

        # Check all four directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (current[0] + dr, current[1] + dc)
            if next_pos not in visited and maze.is_valid_move(next_pos[0], next_pos[1]):
                visited.add(next_pos)
                queue.append(next_pos)

    # If we get here, no path was found
    raise AssertionError("No path from start to goal")


def test_maze_get_cell_pixel_pos():
    """Test get_cell_pixel_pos converts grid to pixel coordinates."""
    maze = Maze(config.MAZE_GRID_SIZE)
    # Set screen offset for 800px wide screen
    maze.set_screen_offset(800)

    x, y = maze.get_cell_pixel_pos(0, 0)
    # Calculate expected offset: (800 - 21*25) / 2 = 137.5 -> 137
    expected_offset = (800 - config.MAZE_GRID_SIZE * maze.cell_size) // 2
    assert x == expected_offset
    assert y == config.MAZE_OFFSET_Y

    x, y = maze.get_cell_pixel_pos(1, 1)
    assert x == expected_offset + maze.cell_size
    assert y == config.MAZE_OFFSET_Y + config.MAZE_CELL_SIZE
