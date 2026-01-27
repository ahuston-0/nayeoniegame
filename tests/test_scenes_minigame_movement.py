"""Unit tests for MovementMinigame."""

import pygame
from nayeoniegame.scenes.minigame_movement import MovementMinigame


def test_movement_minigame_initialization(mock_game):
    """Test movement minigame initializes correctly."""
    scene = MovementMinigame(mock_game)
    assert scene.player is not None
    assert len(scene.all_sprites) == 1


def test_movement_minigame_esc_returns_to_selection(mock_game):
    """Test ESC returns to minigame selection."""
    scene = MovementMinigame(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_movement_minigame_update(mock_game):
    """Test movement minigame updates correctly."""
    scene = MovementMinigame(mock_game)
    scene.update(0.016)  # One frame at 60fps
    # Should not raise


def test_movement_minigame_render(mock_game, mock_screen):
    """Test movement minigame renders without errors."""
    scene = MovementMinigame(mock_game)
    scene.render(mock_screen)  # Should not raise
