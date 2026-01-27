"""Snake minigame scene (classic Snake).

Simple grid-based implementation integrated with the Scene pattern used across
the project. Uses arrow keys / WASD to change direction, ESC to return to the
minigame selection, and ENTER to restart after game over.
"""

import pygame

from .. import config
from ..entities.snake import Snake
from ..entities.snake_sprite import SnakeSprite
from .base import Scene


class SnakeMinigame(Scene):
    """Classic Snake minigame."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 64)

        # Grid settings (visual tweaks)
        # Slightly larger cells improve visibility on typical screens
        self.cell_size = 24
        self.top_offset = 60

        # Fit the maximum whole columns for the given cell size and center the field
        self.cols = config.SCREEN_WIDTH // self.cell_size
        total_field_width = self.cols * self.cell_size
        # Use integer centering so left/right margins are equal
        self.left_offset = (config.SCREEN_WIDTH - total_field_width) // 2

        self.rows = (config.SCREEN_HEIGHT - self.top_offset) // self.cell_size

        # Game state
        # Use a Snake entity to manage logic; scene exposes convenient properties
        self.snake_entity = Snake(self.cols, self.rows)

        # Movement timer (configured via SettingsManager)
        try:
            self.move_interval = float(game.settings_manager.get_snake_move_interval())
        except Exception:
            self.move_interval = 0.12
        self.time_acc = 0.0

    # Properties to keep backwards-compatible access used in tests
    @property
    def snake(self):
        return self.snake_entity.segments

    @snake.setter
    def snake(self, value):
        self.snake_entity.segments = value

    @property
    def direction(self):
        return self.snake_entity.direction

    @direction.setter
    def direction(self, value):
        self.snake_entity.direction = value

    @property
    def food(self):
        return self.snake_entity.food

    @food.setter
    def food(self, value):
        self.snake_entity.food = value

    @property
    def score(self):
        return self.snake_entity.score

    @score.setter
    def score(self, value):
        self.snake_entity.score = value

    @property
    def game_over(self):
        return self.snake_entity.game_over

    @game_over.setter
    def game_over(self, value):
        self.snake_entity.game_over = value

    def reset(self):
        """Reset or start a new game via the entity."""
        self.snake_entity.reset()

    def spawn_food(self):
        self.snake_entity.spawn_food()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))
            elif event.key == pygame.K_RETURN and self.game_over:
                self.reset()
            elif not self.game_over:
                # Direction controls (prevent immediate reverse)
                if event.key in (pygame.K_UP, pygame.K_w):
                    if self.direction != (0, 1):
                        self.direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.direction != (0, -1):
                        self.direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.direction != (1, 0):
                        self.direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.direction != (-1, 0):
                        self.direction = (1, 0)

    def update(self, dt):
        if self.game_over:
            return

        self.time_acc += dt
        if self.time_acc >= self.move_interval:
            self.time_acc -= self.move_interval
            self.snake_entity.step()

    # Movement and collision logic handled by `Snake` entity

    def render(self, screen):
        screen.fill(config.BLACK)

        # Draw grid background (subtle)
        bg_color = (24, 24, 24)
        cell_border = (40, 40, 40)
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    self.left_offset + c * self.cell_size,
                    r * self.cell_size + self.top_offset,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, bg_color, rect)
                pygame.draw.rect(screen, cell_border, rect, 1)

        # Delegate drawing of snake and food to SnakeSprite
        if not hasattr(self, "snake_sprite"):
            self.snake_sprite = SnakeSprite(
                self.snake_entity, self.cell_size, self.top_offset, left_offset=self.left_offset
            )

        self.snake_sprite.draw(screen)

        # HUD
        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        screen.blit(score_text, (10, 10))

        instr = self.font.render("Arrows/WASD: Move | ESC: Back", True, config.WHITE)
        screen.blit(instr, (config.SCREEN_WIDTH - 360, 10))

        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            overlay.set_alpha(160)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            go_text = self.large_font.render("GAME OVER", True, config.RED)
            go_rect = go_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 20)
            )
            screen.blit(go_text, go_rect)

            cont = self.font.render("Press ENTER to restart or ESC to return", True, config.WHITE)
            cont_rect = cont.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 40)
            )
            screen.blit(cont, cont_rect)
