"""Unit tests for SnakeMinigame."""

import pygame

from nayeoniegame.scenes.minigame_snake import SnakeMinigame


def test_snake_initialization(mock_game):
    scene = SnakeMinigame(mock_game)
    assert scene.snake is not None
    assert len(scene.snake) >= 3
    assert scene.score == 0
    assert not scene.game_over


def test_snake_direction_change(mock_game):
    scene = SnakeMinigame(mock_game)
    # Change direction to down
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
    scene.handle_event(event)
    assert scene.direction == (0, 1)


def test_snake_move_progresses(mock_game):
    scene = SnakeMinigame(mock_game)
    head_before = scene.snake[0]
    scene.update(scene.move_interval)
    head_after = scene.snake[0]
    assert head_after != head_before


def test_snake_eat_food_increases_score_and_length(mock_game):
    scene = SnakeMinigame(mock_game)
    head = scene.snake[0]
    # Place food directly in front of the head
    scene.food = (head[0] + scene.direction[0], head[1] + scene.direction[1])
    length_before = len(scene.snake)
    score_before = scene.score
    scene.update(scene.move_interval)
    assert scene.score == score_before + 1
    assert len(scene.snake) == length_before + 1


def test_snake_wall_collision_sets_game_over(mock_game):
    scene = SnakeMinigame(mock_game)
    # Place head at right edge and move right to collide
    row = scene.snake[0][1]
    scene.snake[0] = (scene.cols - 1, row)
    scene.direction = (1, 0)
    scene.update(scene.move_interval)
    assert scene.game_over


def test_snake_esc_returns_to_selection(mock_game):
    scene = SnakeMinigame(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_snake_enter_restarts_after_game_over(mock_game):
    scene = SnakeMinigame(mock_game)
    scene.game_over = True
    scene.score = 5
    scene.snake = [(0, 0)]
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    scene.handle_event(event)
    assert not scene.game_over
    assert scene.score == 0
    assert len(scene.snake) >= 3


def test_snake_render(mock_game, mock_screen):
    scene = SnakeMinigame(mock_game)
    scene.render(mock_screen)  # Should not raise


def test_snake_self_collision_sets_game_over(mock_game):
    """Place the snake in a configuration where the next move causes self-collision."""
    scene = SnakeMinigame(mock_game)
    # Create a U-shape so the head will move into the body
    # Head at (2,1), body occupies (2,2),(1,2),(1,1) and direction down into (2,2)
    scene.snake = [(2, 1), (2, 2), (1, 2), (1, 1)]
    scene.direction = (0, 1)  # moving down into (2,2)

    # Trigger a move
    scene.update(scene.move_interval)

    assert scene.game_over
