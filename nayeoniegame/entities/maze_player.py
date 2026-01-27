"""Maze player entity for Maze Runner minigame."""

import pygame

from .. import config


class MazePlayer(pygame.sprite.Sprite):
    """Player entity that moves in discrete grid cells."""

    def __init__(self, grid_row, grid_col, maze):
        """Initialize maze player at grid position.

        Args:
            grid_row: Starting row in grid
            grid_col: Starting column in grid
            maze: Maze instance for movement validation
        """
        super().__init__()
        self.grid_row = grid_row
        self.grid_col = grid_col
        self.maze = maze

        # Calculate player size as 80% of cell size
        self.player_size = int(maze.cell_size * 0.8)

        # Visual representation
        self.image = pygame.Surface((self.player_size, self.player_size))
        self.image.fill(config.CYAN)
        self.rect = self.image.get_rect()
        self._update_pixel_position()

    def _update_pixel_position(self):
        """Sync pixel position with grid position."""
        x, y = self.maze.get_cell_pixel_pos(self.grid_row, self.grid_col)
        # Center player in cell
        offset = (self.maze.cell_size - self.player_size) // 2
        self.rect.x = x + offset
        self.rect.y = y + offset

    def move(self, direction):
        """Attempt to move in direction if valid.

        Args:
            direction: Tuple (row_delta, col_delta) like (-1, 0) for up

        Returns:
            bool: True if move was successful, False if blocked by wall
        """
        new_row = self.grid_row + direction[0]
        new_col = self.grid_col + direction[1]

        if self.maze.is_valid_move(new_row, new_col):
            self.grid_row = new_row
            self.grid_col = new_col
            self._update_pixel_position()
            return True
        return False

    def update(self, dt):
        """Update called by sprite group.

        Args:
            dt: Time delta in seconds (unused for grid-based movement)
        """
        pass
