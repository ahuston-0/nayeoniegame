"""Pytest configuration and fixtures."""

import pytest
import pygame
import os


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """Initialize pygame in headless mode for all tests."""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_screen():
    """Create a mock pygame screen surface."""
    return pygame.Surface((800, 600))


@pytest.fixture
def mock_game():
    """Create a mock Game instance for testing scenes."""

    class MockGame:
        def __init__(self):
            self.screen = pygame.Surface((800, 600))
            self.current_scene = None
            self.running = True

        def change_scene(self, scene):
            self.current_scene = scene

        def quit(self):
            self.running = False

    return MockGame()
