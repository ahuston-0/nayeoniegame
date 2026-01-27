"""Unit tests for ColorCollectorMinigame."""

import pygame
from nayeoniegame.scenes.minigame_color_collector import ColorCollectorMinigame
from nayeoniegame import config


def test_color_collector_initialization(mock_game):
    """Test color collector initializes correctly."""
    scene = ColorCollectorMinigame(mock_game)
    assert scene.paddle is not None
    assert scene.paddle.rect.bottom == config.SCREEN_HEIGHT - 70
    assert scene.score == 0
    assert scene.lives == config.MAX_LIVES
    assert not scene.game_over


def test_color_collector_spawn_circle(mock_game):
    """Test spawning falling circles."""
    scene = ColorCollectorMinigame(mock_game)
    initial_count = len(scene.falling_circles)
    scene._spawn_circle()
    assert len(scene.falling_circles) == initial_count + 1


def test_color_collector_catch_increases_score(mock_game):
    """Test catching circle increases score."""
    scene = ColorCollectorMinigame(mock_game)
    initial_score = scene.score
    scene._handle_catch()
    assert scene.score == initial_score + 10


def test_color_collector_miss_decreases_lives(mock_game):
    """Test missing circle decreases lives."""
    scene = ColorCollectorMinigame(mock_game)
    initial_lives = scene.lives
    scene._handle_miss()
    assert scene.lives == initial_lives - 1


def test_color_collector_game_over(mock_game):
    """Test game over when lives reach zero."""
    scene = ColorCollectorMinigame(mock_game)
    scene.lives = 1
    scene._handle_miss()
    assert scene.game_over


def test_color_collector_render(mock_game, mock_screen):
    """Test color collector renders without errors."""
    scene = ColorCollectorMinigame(mock_game)
    scene.render(mock_screen)  # Should not raise


def test_color_collector_render_game_over(mock_game, mock_screen):
    """Test color collector renders game over screen."""
    scene = ColorCollectorMinigame(mock_game)
    scene.game_over = True
    scene.render(mock_screen)  # Should not raise


def test_color_collector_update(mock_game):
    """Test color collector updates."""
    scene = ColorCollectorMinigame(mock_game)
    scene.update(0.016)  # Should not raise


def test_color_collector_esc_returns_to_selection(mock_game):
    """Test ESC returns to minigame selection."""
    scene = ColorCollectorMinigame(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    scene.handle_event(event)
    assert mock_game.current_scene is not None
