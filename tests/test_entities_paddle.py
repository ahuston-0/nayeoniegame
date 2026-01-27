"""Unit tests for Paddle entity."""

from nayeoniegame.entities.paddle import Paddle
from nayeoniegame import config


def test_paddle_initialization():
    """Test paddle initializes correctly."""
    paddle = Paddle(400, 550)
    assert paddle.rect.centerx == 400
    assert paddle.rect.bottom == 550


def test_paddle_move_left():
    """Test paddle moves left."""
    paddle = Paddle(400, 550)
    initial_x = paddle.rect.x
    paddle.move_left(0.1)
    assert paddle.rect.x < initial_x


def test_paddle_move_right():
    """Test paddle moves right."""
    paddle = Paddle(400, 550)
    initial_x = paddle.rect.x
    paddle.move_right(0.1)
    assert paddle.rect.x > initial_x


def test_paddle_stays_within_bounds():
    """Test paddle cannot move off screen."""
    paddle = Paddle(0, 550)
    paddle.move_left(1.0)
    assert paddle.rect.left >= 0

    paddle = Paddle(800, 550)
    paddle.move_right(1.0)
    assert paddle.rect.right <= config.SCREEN_WIDTH
