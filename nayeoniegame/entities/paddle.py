"""Paddle entity for Color Collector minigame."""

import pygame

from .. import config


class Paddle(pygame.sprite.Sprite):
    """Horizontal paddle that catches falling objects."""

    def __init__(self, x, y, screen_width=None):
        """Initialize the paddle.

        Args:
            x: Initial x position (center)
            y: Initial y position (bottom)
            screen_width: Width of screen for bounds checking (defaults to config)
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

        # Screen bounds
        self.screen_width = screen_width if screen_width is not None else config.SCREEN_WIDTH

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
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def update(self, dt):
        """Update paddle state.

        Args:
            dt: Time delta in seconds
        """
        # Movement is handled externally via move_left/move_right
        pass
