"""Player entity."""

import pygame

from .. import config


class Player(pygame.sprite.Sprite):
    """Player character sprite."""

    def __init__(self, x, y, screen_width=None, screen_height=None):
        super().__init__()

        # Create sprite surface (a simple circle)
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, config.CYAN, (20, 20), 20)

        # Position
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Movement
        self.speed = 200  # pixels per second
        self.dx = 0
        self.dy = 0

        # Screen bounds
        self.screen_width = screen_width if screen_width is not None else config.SCREEN_WIDTH
        self.screen_height = screen_height if screen_height is not None else config.SCREEN_HEIGHT

    def set_direction(self, dx, dy):
        """Set movement direction.

        Args:
            dx: Horizontal direction (-1, 0, or 1)
            dy: Vertical direction (-1, 0, or 1)
        """
        self.dx = dx
        self.dy = dy

    def update(self, dt):
        """Update player position.

        Args:
            dt: Time delta in seconds
        """
        # Normalize diagonal movement
        if self.dx != 0 and self.dy != 0:
            self.dx *= 0.7071  # 1/sqrt(2)
            self.dy *= 0.7071

        # Update position
        self.rect.x += self.dx * self.speed * dt
        self.rect.y += self.dy * self.speed * dt

        # Keep player on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))
