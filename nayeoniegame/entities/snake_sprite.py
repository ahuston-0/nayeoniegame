"""Rendering helper for the Snake entity.

Separates drawing from game logic so the scene can remain a thin coordinator.
"""

import pygame

from .. import config


class SnakeSprite:
    """Lightweight renderer for a `Snake` entity.

    Usage:
        sprite = SnakeSprite(snake_entity, cell_size, top_offset)
        sprite.draw(screen)
    """

    def __init__(
        self,
        snake_entity,
        cell_size: int,
        top_offset: int,
        colors: dict | None = None,
        left_offset: int = 0,
    ):
        self.snake = snake_entity
        self.cell_size = cell_size
        self.top_offset = top_offset
        self.left_offset = left_offset
        self.colors = colors or {
            "head": config.CYAN,
            "body": config.GREEN,
            "food": config.YELLOW,
            "food_border": config.RED,
            "cell_border": (40, 40, 40),
            "bg": (24, 24, 24),
        }

    def draw(self, screen: pygame.Surface) -> None:
        """Draw food and snake segments onto `screen`."""
        # Draw food (if present)
        if getattr(self.snake, "food", None) is not None:
            fc, fr = self.snake.food
            food_rect = pygame.Rect(
                self.left_offset + fc * self.cell_size,
                fr * self.cell_size + self.top_offset,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(screen, self.colors["food"], food_rect)
            pygame.draw.rect(screen, self.colors["food_border"], food_rect, 2)

        # Draw snake segments
        for i, (c, r) in enumerate(self.snake.segments):
            rect = pygame.Rect(
                self.left_offset + c * self.cell_size,
                r * self.cell_size + self.top_offset,
                self.cell_size,
                self.cell_size,
            )
            color = self.colors["head"] if i == 0 else self.colors["body"]
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, self.colors["cell_border"], rect, 1)
