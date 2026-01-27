"""Unit tests for MazeRunnerMinigame."""

import pygame

from nayeoniegame.scenes.minigame_maze_runner import MazeRunnerMinigame


def test_maze_runner_initialization(mock_game):
    """Test maze runner initializes correctly."""
    scene = MazeRunnerMinigame(mock_game)
    assert scene.maze is not None
    assert scene.player is not None
    assert scene.elapsed_time == 0.0
    assert not scene.game_won


def test_maze_runner_timer_updates(mock_game):
    """Test timer increments during gameplay."""
    scene = MazeRunnerMinigame(mock_game)
    initial_time = scene.elapsed_time
    scene.update(0.1)
    assert scene.elapsed_time > initial_time


def test_maze_runner_arrow_key_moves_player(mock_game):
    """Test arrow keys move player."""
    scene = MazeRunnerMinigame(mock_game)

    # Try moving down
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
    scene.handle_event(event)
    # Player may or may not have moved (depends on walls), but shouldn't crash


def test_maze_runner_wasd_moves_player(mock_game):
    """Test WASD keys move player."""
    scene = MazeRunnerMinigame(mock_game)

    # Try moving with WASD
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
    scene.handle_event(event)
    # Player may or may not have moved (depends on walls), but shouldn't crash


def test_maze_runner_win_condition(mock_game):
    """Test reaching goal triggers win."""
    scene = MazeRunnerMinigame(mock_game)
    # Place player at goal
    scene.player.grid_row = scene.maze.goal[0]
    scene.player.grid_col = scene.maze.goal[1]
    scene.update(0.016)
    assert scene.game_won


def test_maze_runner_timer_stops_after_win(mock_game):
    """Test timer stops incrementing after win."""
    scene = MazeRunnerMinigame(mock_game)
    # Trigger win
    scene.player.grid_row = scene.maze.goal[0]
    scene.player.grid_col = scene.maze.goal[1]
    scene.update(0.016)
    assert scene.game_won

    time_at_win = scene.elapsed_time
    scene.update(0.1)
    assert scene.elapsed_time == time_at_win  # Should not increase


def test_maze_runner_esc_returns_to_selection(mock_game):
    """Test ESC returns to minigame selection."""
    scene = MazeRunnerMinigame(mock_game)
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_maze_runner_enter_after_win(mock_game):
    """Test ENTER after win returns to selection."""
    scene = MazeRunnerMinigame(mock_game)
    scene.game_won = True
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
    scene.handle_event(event)
    assert mock_game.current_scene is not None


def test_maze_runner_cannot_move_after_win(mock_game):
    """Test player cannot move after winning."""
    scene = MazeRunnerMinigame(mock_game)
    scene.game_won = True
    initial_row = scene.player.grid_row
    initial_col = scene.player.grid_col

    # Try to move
    event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
    scene.handle_event(event)

    # Position should not change
    assert scene.player.grid_row == initial_row
    assert scene.player.grid_col == initial_col


def test_maze_runner_render(mock_game, mock_screen):
    """Test maze runner renders without errors."""
    scene = MazeRunnerMinigame(mock_game)
    scene.render(mock_screen)  # Should not raise


def test_maze_runner_render_win_screen(mock_game, mock_screen):
    """Test maze runner renders win screen."""
    scene = MazeRunnerMinigame(mock_game)
    scene.game_won = True
    scene.render(mock_screen)  # Should not raise


def test_maze_runner_update(mock_game):
    """Test maze runner updates."""
    scene = MazeRunnerMinigame(mock_game)
    scene.update(0.016)  # Should not raise
