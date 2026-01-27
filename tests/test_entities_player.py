"""Unit tests for Player entity."""

from nayeoniegame.entities.player import Player


def test_player_initialization():
    """Test player initializes at correct position."""
    player = Player(100, 200)
    assert player.rect.centerx == 100
    assert player.rect.centery == 200
    assert player.speed == 200


def test_player_set_direction():
    """Test player direction setting."""
    player = Player(100, 100)
    player.set_direction(1, 0)
    assert player.dx == 1
    assert player.dy == 0


def test_player_movement():
    """Test player moves correctly."""
    player = Player(100, 100)
    player.set_direction(1, 0)
    initial_x = player.rect.x
    player.update(0.1)  # 0.1 second
    assert player.rect.x > initial_x


def test_player_stays_on_screen():
    """Test player clamping to screen bounds."""
    player = Player(0, 0)
    player.set_direction(-1, -1)
    player.update(1.0)
    assert player.rect.x >= 0
    assert player.rect.y >= 0


def test_player_diagonal_normalization():
    """Test diagonal movement is normalized."""
    player = Player(100, 100)
    player.set_direction(1, 1)
    player.update(0.01)
    # After normalization, diagonal should be ~0.7071
    assert abs(player.dx - 0.7071) < 0.001
