"""Minigame selection menu scene."""

import pygame

from .. import config
from .base import Scene


class MinigameSelectionScene(Scene):
    """Menu for selecting which minigame to play.

    This scene provides a modular way to add new minigames.
    To add a new minigame:
    1. Create the minigame scene class
    2. Add it to the MINIGAMES list with name, description, and scene class
    """

    # Modular minigame registry
    # Each entry: (name, description, scene_class)
    MINIGAMES = [
        ("Free Movement", "Move around the screen", "MovementMinigame"),
        ("Color Collector", "Catch falling circles", "ColorCollectorMinigame"),
    ]

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 28)
        self.selected_option = 0

        # Add "Back to Main Menu" option
        self.options = [f"{name} - {desc}" for name, desc, _ in self.MINIGAMES]
        self.options.append("Back to Main Menu")

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                # Return to main menu
                from .main_menu import MainMenuScene

                self.game.change_scene(MainMenuScene(self.game))

    def _select_option(self):
        """Handle option selection."""
        if self.selected_option < len(self.MINIGAMES):
            # Load the selected minigame
            _, _, scene_class_name = self.MINIGAMES[self.selected_option]

            # Dynamically import the scene class
            if scene_class_name == "MovementMinigame":
                from .minigame_movement import MovementMinigame

                self.game.change_scene(MovementMinigame(self.game))
            elif scene_class_name == "ColorCollectorMinigame":
                from .minigame_color_collector import ColorCollectorMinigame

                self.game.change_scene(ColorCollectorMinigame(self.game))
        else:
            # Back to Main Menu option
            from .main_menu import MainMenuScene

            self.game.change_scene(MainMenuScene(self.game))

    def update(self, dt):
        """Update menu state."""
        pass  # No updates needed for static menu

    def render(self, screen):
        """Render the minigame selection menu."""
        screen.fill(config.BLACK)

        # Draw title
        title_text = self.font.render("Select a Minigame", True, config.CYAN)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw menu options
        for i, option in enumerate(self.options):
            color = config.YELLOW if i == self.selected_option else config.WHITE
            text = self.small_font.render(option, True, color)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, 220 + i * 50))
            screen.blit(text, text_rect)

        # Draw instructions
        instructions = self.small_font.render(
            "UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, config.WHITE
        )
        instructions_rect = instructions.get_rect(center=(config.SCREEN_WIDTH // 2, 520))
        screen.blit(instructions, instructions_rect)

    @property
    def minigames(self):
        """Get list of available minigames (for testing)."""
        return self.MINIGAMES
