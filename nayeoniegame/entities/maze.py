"""Maze entity for Maze Runner minigame."""

import random

from .. import config


class Maze:
    """Grid-based maze with recursive backtracking generation."""

    WALL = 1
    PATH = 0

    def __init__(self, size, cell_size=None):
        """Initialize maze with given size (size x size grid).

        Args:
            size: Number of cells in each dimension (should be odd for best results)
            cell_size: Size of each cell in pixels (if None, uses config.MAZE_CELL_SIZE)
        """
        # Ensure size is odd for proper maze generation
        if size % 2 == 0:
            size += 1

        self.size = size
        self.grid = [[self.WALL for _ in range(size)] for _ in range(size)]
        self.start = (1, 1)  # Top-left area
        self.goal = (size - 2, size - 2)  # Bottom-right area

        # Store cell size for rendering
        if cell_size is None:
            self.cell_size = config.MAZE_CELL_SIZE
        else:
            self.cell_size = cell_size

        # Calculate and store offset (will be set by scene)
        self.offset_x = 0
        self.offset_y = config.MAZE_OFFSET_Y

        self._generate()

    def _generate(self):
        """Generate maze using recursive backtracking (DFS).

        Creates a perfect maze (exactly one path between any two points).
        Uses a grid where odd coordinates are paths, creating walls between them.
        """
        # Start from starting position
        stack = [self.start]
        visited = set()
        visited.add(self.start)
        self.grid[self.start[0]][self.start[1]] = self.PATH

        # Directions: up, down, left, right (moving 2 cells at a time)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            current = stack[-1]
            row, col = current

            # Get unvisited neighbors (2 cells away)
            neighbors = []
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Check if neighbor is valid and unvisited
                if (
                    0 < new_row < self.size - 1
                    and 0 < new_col < self.size - 1
                    and (new_row, new_col) not in visited
                ):
                    neighbors.append((new_row, new_col, dr, dc))

            if neighbors:
                # Choose random unvisited neighbor
                next_cell = random.choice(neighbors)
                next_row, next_col, dr, dc = next_cell

                # Carve path through the wall between current and next cell
                wall_row = row + dr // 2
                wall_col = col + dc // 2
                self.grid[wall_row][wall_col] = self.PATH

                # Carve path at the next cell
                self.grid[next_row][next_col] = self.PATH

                # Mark as visited and add to stack
                visited.add((next_row, next_col))
                stack.append((next_row, next_col))
            else:
                # Backtrack
                stack.pop()

        # Ensure goal is a path
        self.grid[self.goal[0]][self.goal[1]] = self.PATH

    def is_valid_move(self, row, col):
        """Check if position is valid (in bounds and not a wall).

        Args:
            row: Row coordinate
            col: Column coordinate

        Returns:
            bool: True if position is valid and passable, False otherwise
        """
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        return self.grid[row][col] == self.PATH

    def set_screen_offset(self, screen_width):
        """Calculate and set the X offset to center the maze on screen.

        Args:
            screen_width: Width of the screen in pixels
        """
        maze_width = self.size * self.cell_size
        self.offset_x = (screen_width - maze_width) // 2

    def get_cell_pixel_pos(self, row, col):
        """Convert grid position to pixel position for rendering.

        Args:
            row: Row coordinate in grid
            col: Column coordinate in grid

        Returns:
            tuple: (x, y) pixel coordinates
        """
        x = self.offset_x + col * self.cell_size
        y = self.offset_y + row * self.cell_size
        return (x, y)
