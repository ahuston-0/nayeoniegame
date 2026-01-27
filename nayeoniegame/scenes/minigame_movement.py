"""Movement minigame scene."""

import pygame
from .base import Scene
from .. import config
from ..entities.player import Player


class MovementMinigame(Scene):
    """Free movement minigame - explore the screen."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 32)

        # Create player
        self.player = Player(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to minigame selection
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))

    def update(self, dt):
        """Update game state."""
        # Get key presses
        keys = pygame.key.get_pressed()

        # Update player based on keys
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        self.player.set_direction(dx, dy)

        # Update all sprites
        self.all_sprites.update(dt)

    def render(self, screen):
        """Render the gameplay."""
        screen.fill(config.BLACK)

        # Draw all sprites
        self.all_sprites.draw(screen)

        # Draw title
        title = self.font.render("Minigame: Free Movement", True, config.CYAN)
        screen.blit(title, (10, 10))

        # Draw instructions
        instructions = self.font.render(
            "WASD/Arrows: Move | ESC: Back", True, config.WHITE
        )
        screen.blit(instructions, (10, config.SCREEN_HEIGHT - 40))
