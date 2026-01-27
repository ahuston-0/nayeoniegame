"""Unit tests for FallingCircle entity."""

from nayeoniegame.entities.falling_circle import FallingCircle
from nayeoniegame import config


def test_falling_circle_initialization():
    """Test falling circle initializes correctly."""
    circle = FallingCircle(100, 50, config.RED)
    assert circle.rect.centerx == 100
    assert circle.rect.centery == 50
    assert circle.color == config.RED


def test_falling_circle_falls():
    """Test circle falls downward."""
    circle = FallingCircle(100, 50, config.RED)
    initial_y = circle.rect.y
    circle.update(0.1)
    assert circle.rect.y > initial_y


def test_falling_circle_off_screen():
    """Test detecting when circle is off screen."""
    circle = FallingCircle(100, 700, config.RED)
    assert circle.is_off_screen()

    circle2 = FallingCircle(100, 50, config.BLUE)
    assert not circle2.is_off_screen()


def test_falling_circle_custom_speed():
    """Test falling circle with custom speed."""
    circle = FallingCircle(100, 50, config.GREEN, speed=300)
    assert circle.speed == 300
