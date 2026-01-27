"""Paddle entity for Color Collector minigame."""

import pygame
from .. import config


class Paddle(pygame.sprite.Sprite):
    """Horizontal paddle that catches falling objects."""

    def __init__(self, x, y):
        """Initialize the paddle.

        Args:
            x: Initial x position (center)
            y: Initial y position (bottom)
        """
        super().__init__()

        # Create paddle surface
        self.image = pygame.Surface((config.PADDLE_WIDTH, config.PADDLE_HEIGHT))
        self.image.fill(config.WHITE)

        # Position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Movement speed
        self.speed = config.PADDLE_SPEED

    def move_left(self, dt):
        """Move paddle left.

        Args:
            dt: Time delta in seconds
        """
        self.rect.x -= self.speed * dt
        # Clamp to screen bounds
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self, dt):
        """Move paddle right.

        Args:
            dt: Time delta in seconds
        """
        self.rect.x += self.speed * dt
        # Clamp to screen bounds
        if self.rect.right > config.SCREEN_WIDTH:
            self.rect.right = config.SCREEN_WIDTH

    def update(self, dt):
        """Update paddle state.

        Args:
            dt: Time delta in seconds
        """
        # Movement is handled externally via move_left/move_right
        pass
