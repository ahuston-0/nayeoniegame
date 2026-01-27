"""Main game class."""

import os
import sys

import pygame

from . import config
from .scenes.main_menu import MainMenuScene
from .settings import SettingsManager


class Game:
    """Main game class handling the game loop and scene management."""

    def __init__(self, headless=False):
        """Initialize the game.

        Args:
            headless: If True, run in headless mode (no display)
        """
        pygame.init()

        # Load settings
        self.settings_manager = SettingsManager()

        # Get display settings from saved preferences
        width, height = self.settings_manager.get_resolution()
        window_mode = self.settings_manager.get_window_mode()

        # Check if we can create a display
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            self.screen = pygame.display.set_mode((width, height))
        else:
            try:
                # Determine pygame display flags based on window mode
                flags = 0
                if window_mode == "fullscreen":
                    flags = pygame.FULLSCREEN
                elif window_mode == "borderless":
                    flags = pygame.NOFRAME

                self.screen = pygame.display.set_mode((width, height), flags)
                pygame.display.set_caption(config.TITLE)
            except pygame.error as e:
                print(f"Error: Could not create display: {e}")
                print("\nThis game requires a graphical environment to run.")
                print("If you're running in a headless environment (SSH, container, etc.),")
                print("you'll need to set up a virtual display or run on a system with a display.")
                print("\nFor testing purposes, you can verify the game imports correctly with:")
                print(
                    "  python -c 'from nayeoniegame.game import Game; print(\"Import successful!\")'"
                )
                pygame.quit()
                sys.exit(1)

        # Clock for framerate control
        self.clock = pygame.time.Clock()

        # Scene management
        self.current_scene = MainMenuScene(self)
        self.running = True

    def change_scene(self, new_scene):
        """Change to a new scene.

        Args:
            new_scene: Scene instance to switch to
        """
        self.current_scene = new_scene

    def quit(self):
        """Quit the game."""
        self.running = False

    def run(self):
        """Run the main game loop."""
        while self.running:
            # Calculate time delta
            dt = self.clock.tick(config.FPS) / 1000.0  # Convert ms to seconds

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_scene.handle_event(event)

            # Update
            self.current_scene.update(dt)

            # Render
            self.current_scene.render(self.screen)
            pygame.display.flip()

        # Clean up
        pygame.quit()
