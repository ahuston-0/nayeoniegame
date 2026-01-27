"""Test script to verify the game setup without requiring a display."""

import sys


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import pygame

        print(f"  ✓ pygame {pygame.version.ver}")

        from nayeoniegame import config  # noqa F401

        print("  ✓ config module")

        from nayeoniegame.scenes.base import Scene  # noqa F401

        print("  ✓ base scene")

        from nayeoniegame.scenes.main_menu import MainMenuScene  # noqa F401

        print("  ✓ main menu scene")

        from nayeoniegame.scenes.minigame_movement import MovementMinigame  # noqa F401

        print("  ✓ movement minigame scene")

        from nayeoniegame.entities.player import Player  # noqa F401

        print("  ✓ player entity")

        from nayeoniegame.game import Game  # noqa F401

        print("  ✓ game class")

        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration values."""
    print("\nTesting configuration...")
    try:
        from nayeoniegame import config

        assert config.SCREEN_WIDTH > 0, "Screen width must be positive"
        assert config.SCREEN_HEIGHT > 0, "Screen height must be positive"
        assert config.FPS > 0, "FPS must be positive"
        assert config.TITLE, "Title must not be empty"

        print(f"  ✓ Screen: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
        print(f"  ✓ FPS: {config.FPS}")
        print(f"  ✓ Title: {config.TITLE}")

        return True
    except Exception as e:
        print(f"  ✗ Config test failed: {e}")
        return False


def test_player():
    """Test player entity creation."""
    print("\nTesting player entity...")
    try:
        import pygame

        pygame.init()

        from nayeoniegame.entities.player import Player

        player = Player(100, 100)
        assert player.rect.centerx == 100, "Player X position incorrect"
        assert player.rect.centery == 100, "Player Y position incorrect"

        player.set_direction(1, 0)
        player.update(0.016)  # Simulate one frame at 60fps

        print("  ✓ Player creation")
        print("  ✓ Player movement")

        pygame.quit()
        return True
    except Exception as e:
        print(f"  ✗ Player test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Nayeonie Game Setup Test")
    print("=" * 50)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Player Entity", test_player()))

    print("\n" + "=" * 50)
    print("Test Results")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("\n✓ All tests passed! The game is ready to run.")
        print("\nTo run the game (requires graphical environment):")
        print("  python -m nayeoniegame")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
