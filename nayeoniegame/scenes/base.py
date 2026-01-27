"""Base scene class for all game scenes."""

from abc import ABC, abstractmethod
import pygame


class Scene(ABC):
    """Base class for all game scenes."""

    def __init__(self, game):
        """Initialize the scene.

        Args:
            game: Reference to the main Game instance
        """
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        """Handle a pygame event.

        Args:
            event: pygame.Event to handle
        """
        pass

    @abstractmethod
    def update(self, dt):
        """Update scene state.

        Args:
            dt: Time delta in seconds since last frame
        """
        pass

    @abstractmethod
    def render(self, screen):
        """Render the scene.

        Args:
            screen: pygame.Surface to draw on
        """
        pass
