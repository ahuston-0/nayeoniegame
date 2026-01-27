"""Falling circle entity for Color Collector minigame."""

import pygame

from .. import config
from ..assets import get_image


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

        # Create circle surface (try to load asset, otherwise draw procedurally).
        radius = config.CIRCLE_RADIUS
        img = None
        try:
            img = get_image("circle", (radius * 2, radius * 2))
        except Exception:
            img = None

        if img is not None:
            # Ensure we have an alpha-capable surface and attempt to tint it
            try:
                img = img.copy().convert_alpha()
                # Normalize base to white: set any non-transparent pixel to white
                try:
                    w, h = img.get_size()
                    for px in range(w):
                        for py in range(h):
                            r, g, b, a = img.get_at((px, py))
                            if a == 0:
                                continue
                            img.set_at((px, py), (255, 255, 255, a))
                except Exception:
                    # If per-pixel ops fail, continue and attempt tinting anyway
                    pass

                if color is not None:
                    tint = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                    tint.fill((color[0], color[1], color[2], 255))
                    # Multiply the image by the tint so white areas take the tint color
                    img.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            except Exception:
                img = None

        if img is None:
            img = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(img, color, (radius, radius), radius)

        self.image = img

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
