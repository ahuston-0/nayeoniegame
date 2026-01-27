"""Pytest configuration and fixtures."""

import os

import pygame
import pytest


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
def mock_game(tmp_path):
    """Create a mock Game instance for testing scenes."""
    from nayeoniegame.settings import SettingsManager

    class MockGame:
        def __init__(self):
            self.screen = pygame.Surface((800, 600))
            self.current_scene = None
            self.running = True
            # Use temporary path for settings in tests
            self.settings_manager = SettingsManager(tmp_path / "test_settings.toml")

        def change_scene(self, scene):
            self.current_scene = scene

        def quit(self):
            self.running = False

    return MockGame()
