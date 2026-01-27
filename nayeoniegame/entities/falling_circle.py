"""Falling circle entity for Color Collector minigame."""

import pygame

from .. import config


class FallingCircle(pygame.sprite.Sprite):
    """A circle that falls from the top of the screen."""

    def __init__(self, x, y, color, speed=None):
        """Initialize the falling circle.

        Args:
            x: Initial x position (center)
            y: Initial y position (center)
            color: RGB tuple for circle color
            speed: Fall speed (pixels/second), defaults to config value
        """
        super().__init__()

        # Create circle surface
        radius = config.CIRCLE_RADIUS
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        # Position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Movement
        self.speed = speed if speed is not None else config.CIRCLE_FALL_SPEED
        self.color = color

    def update(self, dt):
        """Update circle position.

        Args:
            dt: Time delta in seconds
        """
        self.rect.y += self.speed * dt

    def is_off_screen(self, screen_height=None):
        """Check if circle has fallen off the bottom of the screen.

        Args:
            screen_height: Height of screen (defaults to config)

        Returns:
            bool: True if off screen
        """
        height = screen_height if screen_height is not None else config.SCREEN_HEIGHT
        return self.rect.top > height
