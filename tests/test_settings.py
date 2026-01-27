"""Unit tests for settings manager."""

from nayeoniegame.settings import SettingsManager


def test_settings_manager_initialization(tmp_path):
    """Test settings manager initializes with defaults."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    assert manager.get("video", "resolution") == "800x600"
    assert manager.get("video", "window_mode") == "windowed"
    assert manager.get("gameplay", "maze_difficulty") == "medium"


def test_settings_manager_get_resolution(tmp_path):
    """Test get_resolution returns tuple."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    width, height = manager.get_resolution()
    assert width == 800
    assert height == 600


def test_settings_manager_set_and_get(tmp_path):
    """Test setting and getting values."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    manager.set("video", "resolution", "1920x1080")
    assert manager.get("video", "resolution") == "1920x1080"

    width, height = manager.get_resolution()
    assert width == 1920
    assert height == 1080


def test_settings_manager_save_and_load(tmp_path):
    """Test saving and loading settings."""
    settings_file = tmp_path / "test_settings.toml"

    # Create and modify settings
    manager1 = SettingsManager(settings_file)
    manager1.set("video", "resolution", "1280x720")
    manager1.set("gameplay", "maze_difficulty", "hard")
    manager1.save()

    # Load settings in new instance
    manager2 = SettingsManager(settings_file)
    assert manager2.get("video", "resolution") == "1280x720"
    assert manager2.get("gameplay", "maze_difficulty") == "hard"


def test_settings_manager_get_window_mode(tmp_path):
    """Test get_window_mode returns correct value."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    assert manager.get_window_mode() == "windowed"

    manager.set("video", "window_mode", "fullscreen")
    assert manager.get_window_mode() == "fullscreen"


def test_settings_manager_get_maze_cell_size(tmp_path):
    """Test get_maze_cell_size returns correct size for difficulty."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    # Default is medium
    assert manager.get_maze_cell_size() == 25

    # Test easy
    manager.set("gameplay", "maze_difficulty", "easy")
    assert manager.get_maze_cell_size() == 30

    # Test hard
    manager.set("gameplay", "maze_difficulty", "hard")
    assert manager.get_maze_cell_size() == 20


def test_settings_manager_get_maze_difficulty(tmp_path):
    """Test get_maze_difficulty returns current difficulty."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    assert manager.get_maze_difficulty() == "medium"

    manager.set("gameplay", "maze_difficulty", "easy")
    assert manager.get_maze_difficulty() == "easy"


def test_settings_manager_invalid_resolution(tmp_path):
    """Test handling of invalid resolution format."""
    settings_file = tmp_path / "test_settings.toml"
    manager = SettingsManager(settings_file)

    manager.set("video", "resolution", "invalid")
    width, height = manager.get_resolution()
    # Should fall back to defaults
    assert width == 800
    assert height == 600


def test_settings_manager_defaults_with_missing_file(tmp_path):
    """Test that defaults are used when file doesn't exist."""
    settings_file = tmp_path / "nonexistent_settings.toml"
    manager = SettingsManager(settings_file)

    assert not settings_file.exists()
    assert manager.get("video", "resolution") == "800x600"
    assert manager.get("gameplay", "maze_difficulty") == "medium"
