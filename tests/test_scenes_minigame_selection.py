"""Unit tests for MinigameSelectionScene."""

import pygame

from nayeoniegame.scenes.minigame_selection import MinigameSelectionScene


def test_minigame_selection_initialization(mock_game):
    """Test minigame selection initializes correctly."""
    scene = MinigameSelectionScene(mock_game)
    assert scene.selected_option == 0
    assert len(scene.minigames) == 2  # Movement and Color Collector


def test_minigame_selection_navigation(mock_game):
    """Test navigation in minigame selection."""
    scene = MinigameSelectionScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
    scene.handle_event(event)
    assert scene.selected_option == 1


def test_minigame_selection_navigation_wraps(mock_game):
    """Test navigation wraps around."""
    scene = MinigameSelectionScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
    scene.handle_event(event)
    # Should wrap to last option
    assert scene.selected_option == len(scene.options) - 1


def test_minigame_selection_esc_returns_to_main(mock_game):
    """Test ESC returns to main menu."""
    scene = MinigameSelectionScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_minigame_selection_render(mock_game, mock_screen):
    """Test minigame selection renders without errors."""
    scene = MinigameSelectionScene(mock_game)
    scene.render(mock_screen)  # Should not raise


def test_minigame_selection_update(mock_game):
    """Test minigame selection update."""
    scene = MinigameSelectionScene(mock_game)
    scene.update(0.016)  # Should not raise
