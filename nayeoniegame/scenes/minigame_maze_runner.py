"""Maze Runner minigame scene."""

import pygame

from .. import config
from ..assets import get_image
from ..entities.maze import Maze
from ..entities.maze_player import MazePlayer
from .base import Scene


class MazeRunnerMinigame(Scene):
    """Navigate through a procedurally generated maze."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 32)
        self.large_font = pygame.font.SysFont(None, 64)

        # Game state
        self.elapsed_time = 0.0
        self.game_won = False

        # Get maze cell size from settings
        cell_size = game.settings_manager.get_maze_cell_size()

        # Calculate grid size based on cell size to fit the screen
        max_dimension = 525  # pixels available for maze
        grid_size = max_dimension // cell_size
        if grid_size % 2 == 0:
            grid_size += 1  # Ensure odd for proper generation

        # Create maze and player with dynamic cell size
        self.maze = Maze(grid_size, cell_size)
        # Set screen offset for proper centering
        self.maze.set_screen_offset(game.screen.get_width())
        self.player = MazePlayer(self.maze.start[0], self.maze.start[1], self.maze)
        self.cell_size = cell_size
        self.grid_size = grid_size

        # Load tile images (fallback to placeholders provided by get_image)
        self.wall_surface = get_image("maze_wall", (self.cell_size, self.cell_size))
        self.floor_surface = get_image("maze_floor", (self.cell_size, self.cell_size))

        # Sprite group for rendering
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def handle_event(self, event):
        """Handle arrow key input and ESC."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to minigame selection
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))
            elif event.key == pygame.K_RETURN and self.game_won:
                # Return to selection after win
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))
            elif not self.game_won:
                # Handle arrow keys for movement
                direction = None
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = (-1, 0)  # Up
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = (1, 0)  # Down
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = (0, -1)  # Left
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = (0, 1)  # Right

                if direction:
                    self.player.move(direction)

    def update(self, dt):
        """Update timer and check win condition."""
        if not self.game_won:
            self.elapsed_time += dt

            # Check if player reached goal
            if (
                self.player.grid_row == self.maze.goal[0]
                and self.player.grid_col == self.maze.goal[1]
            ):
                self.game_won = True

        self.all_sprites.update(dt)

    def render(self, screen):
        """Render maze, player, HUD, and win screen."""
        screen.fill(config.BLACK)

        # Draw maze
        self._draw_maze(screen)

        # Draw goal
        self._draw_goal(screen)

        # Draw player
        self.all_sprites.draw(screen)

        # Draw HUD
        time_text = self.font.render(f"Time: {self.elapsed_time:.1f}s", True, config.WHITE)
        screen.blit(time_text, (10, 10))

        # Draw instructions
        instructions = self.font.render("Arrows/WASD: Move | ESC: Back", True, config.WHITE)
        screen.blit(instructions, (10, config.SCREEN_HEIGHT - 40))

        # Draw win screen
        if self.game_won:
            self._draw_win_screen(screen)

    def _draw_maze(self, screen):
        """Draw all maze cells."""
        for row in range(self.maze.size):
            for col in range(self.maze.size):
                x, y = self.maze.get_cell_pixel_pos(row, col)
                if self.maze.grid[row][col] == Maze.WALL:
                    # Draw wall using image if available
                    if self.wall_surface:
                        screen.blit(self.wall_surface, (x, y))
                    else:
                        pygame.draw.rect(
                            screen, config.WHITE, (x, y, self.cell_size, self.cell_size)
                        )
                else:
                    # Draw floor/path using image if available
                    if self.floor_surface:
                        screen.blit(self.floor_surface, (x, y))
                    else:
                        pygame.draw.rect(
                            screen, (40, 40, 40), (x, y, self.cell_size, self.cell_size)
                        )
                        pygame.draw.rect(
                            screen, (60, 60, 60), (x, y, self.cell_size, self.cell_size), 1
                        )

    def _draw_goal(self, screen):
        """Draw goal marker."""
        x, y = self.maze.get_cell_pixel_pos(self.maze.goal[0], self.maze.goal[1])
        player_size = int(self.cell_size * 0.8)
        offset = (self.cell_size - player_size) // 2
        pygame.draw.rect(
            screen,
            config.YELLOW,
            (x + offset, y + offset, player_size, player_size),
        )

    def _draw_win_screen(self, screen):
        """Draw win overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(config.BLACK)
        screen.blit(overlay, (0, 0))

        # Win message
        win_text = self.large_font.render("YOU WIN!", True, config.GREEN)
        win_rect = win_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)
        )
        screen.blit(win_text, win_rect)

        # Time display
        time_text = self.font.render(f"Time: {self.elapsed_time:.1f}s", True, config.WHITE)
        time_rect = time_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20)
        )
        screen.blit(time_text, time_rect)

        # Continue instruction
        continue_text = self.font.render("Press ENTER to continue", True, config.WHITE)
        continue_rect = continue_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 70)
        )
        screen.blit(continue_text, continue_rect)
