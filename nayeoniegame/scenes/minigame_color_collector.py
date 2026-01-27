"""Color Collector minigame scene."""

import random

import pygame

from .. import config
from ..entities.falling_circle import FallingCircle
from ..entities.paddle import Paddle
from .base import Scene


class ColorCollectorMinigame(Scene):
    """Catch falling colored circles with a paddle."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 32)
        self.large_font = pygame.font.SysFont(None, 64)

        # Game state
        self.score = 0
        self.lives = config.MAX_LIVES
        self.game_over = False
        self.spawn_timer = 0

        # Colors to choose from for circles
        self.colors = [
            config.RED,
            config.GREEN,
            config.BLUE,
            config.YELLOW,
            config.MAGENTA,
            config.CYAN,
        ]

        # Create paddle
        self.paddle = Paddle(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 70)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.paddle)

        self.falling_circles = pygame.sprite.Group()

    def _spawn_circle(self):
        """Spawn a new falling circle at random position."""
        x = random.randint(config.CIRCLE_RADIUS, config.SCREEN_WIDTH - config.CIRCLE_RADIUS)
        y = -config.CIRCLE_RADIUS
        color = random.choice(self.colors)
        circle = FallingCircle(x, y, color)
        self.falling_circles.add(circle)
        self.all_sprites.add(circle)

    def _handle_catch(self):
        """Handle catching a circle (increase score)."""
        self.score += 10

    def _handle_miss(self):
        """Handle missing a circle (decrease lives)."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to minigame selection
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))
            elif event.key == pygame.K_RETURN and self.game_over:
                # Restart game or return to selection
                from .minigame_selection import MinigameSelectionScene

                self.game.change_scene(MinigameSelectionScene(self.game))

    def update(self, dt):
        """Update game state."""
        if self.game_over:
            return

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move_left(dt)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move_right(dt)

        # Spawn circles
        self.spawn_timer += dt
        if self.spawn_timer >= config.CIRCLE_SPAWN_INTERVAL:
            self._spawn_circle()
            self.spawn_timer = 0

        # Update all sprites
        self.all_sprites.update(dt)

        # Check for collisions
        hits = pygame.sprite.spritecollide(self.paddle, self.falling_circles, True)
        for _hit in hits:
            self._handle_catch()

        # Remove off-screen circles and count misses
        for circle in list(self.falling_circles):
            if circle.is_off_screen():
                self._handle_miss()
                circle.kill()

    def render(self, screen):
        """Render the minigame."""
        screen.fill(config.BLACK)

        # Draw all sprites
        self.all_sprites.draw(screen)

        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, config.WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, config.WHITE)
        screen.blit(lives_text, (10, 50))

        # Draw instructions
        instructions = self.font.render("A/D or Arrows: Move | ESC: Back", True, config.WHITE)
        screen.blit(instructions, (10, config.SCREEN_HEIGHT - 40))

        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(config.BLACK)
            screen.blit(overlay, (0, 0))

            game_over_text = self.large_font.render("GAME OVER", True, config.RED)
            game_over_rect = game_over_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 50)
            )
            screen.blit(game_over_text, game_over_rect)

            final_score_text = self.font.render(f"Final Score: {self.score}", True, config.WHITE)
            final_score_rect = final_score_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20)
            )
            screen.blit(final_score_text, final_score_rect)

            continue_text = self.font.render("Press ENTER to continue", True, config.WHITE)
            continue_rect = continue_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 70)
            )
            screen.blit(continue_text, continue_rect)
