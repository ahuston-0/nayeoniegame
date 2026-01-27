"""Main menu scene."""

import pygame

from .. import config
from .base import Scene


class MainMenuScene(Scene):
    """Main menu scene with start button."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "Quit"]

        # Get dynamic screen dimensions
        self.screen_width = game.screen.get_width()
        self.screen_height = game.screen.get_height()

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()

    def _select_option(self):
        """Handle option selection."""
        if self.selected_option == 0:  # Start Game
            from .minigame_selection import MinigameSelectionScene

            self.game.change_scene(MinigameSelectionScene(self.game))
        elif self.selected_option == 1:  # Settings
            from .settings import SettingsScene

            self.game.change_scene(SettingsScene(self.game))
        elif self.selected_option == 2:  # Quit
            self.game.quit()

    def update(self, dt):
        """Update menu state."""
        pass  # No updates needed for static menu

    def render(self, screen):
        """Render the main menu."""
        screen.fill(config.BLACK)

        # Draw title
        title_text = self.font.render(config.TITLE, True, config.CYAN)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Draw menu options
        for i, option in enumerate(self.options):
            color = config.YELLOW if i == self.selected_option else config.WHITE
            text = self.small_font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, 300 + i * 60))
            screen.blit(text, text_rect)

        # Draw instructions
        instructions = self.small_font.render(
            "Use UP/DOWN arrows and ENTER to select", True, config.WHITE
        )
        instructions_rect = instructions.get_rect(center=(self.screen_width // 2, 500))
        screen.blit(instructions, instructions_rect)
