"""Unit tests for MainMenuScene."""

import pygame

from nayeoniegame.scenes.main_menu import MainMenuScene


def test_main_menu_initialization(mock_game):
    """Test main menu initializes correctly."""
    scene = MainMenuScene(mock_game)
    assert scene.selected_option == 0
    assert len(scene.options) == 3  # Start Game, Settings, Quit


def test_main_menu_navigation_down(mock_game):
    """Test navigating down in menu."""
    scene = MainMenuScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
    scene.handle_event(event)
    assert scene.selected_option == 1


def test_main_menu_navigation_up(mock_game):
    """Test navigating up wraps around."""
    scene = MainMenuScene(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})
    scene.handle_event(event)
    assert scene.selected_option == 2  # Wraps to bottom (Quit)


def test_main_menu_select_start_game(mock_game):
    """Test selecting start game option."""
    scene = MainMenuScene(mock_game)
    scene.selected_option = 0
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_main_menu_select_quit(mock_game):
    """Test selecting quit option."""
    scene = MainMenuScene(mock_game)
    scene.selected_option = 2  # Quit is now option 2
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    scene.handle_event(event)
    assert not mock_game.running


def test_main_menu_render(mock_game, mock_screen):
    """Test main menu renders without errors."""
    scene = MainMenuScene(mock_game)
    scene.render(mock_screen)  # Should not raise


def test_main_menu_update(mock_game):
    """Test main menu update."""
    scene = MainMenuScene(mock_game)
    scene.update(0.016)  # Should not raise
