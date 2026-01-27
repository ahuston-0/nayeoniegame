"""Settings manager for game configuration with TOML persistence."""

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError as e:
        raise ImportError(
            "tomli is required for TOML support. Please install it with `pip install tomli`."
        ) from e


class SettingsManager:
    """Manage game settings with TOML file persistence."""

    # Default settings
    DEFAULTS = {
        "video": {
            "resolution": "800x600",
            "window_mode": "windowed",  # windowed, fullscreen, borderless
        },
        "gameplay": {
            "maze_difficulty": "medium",  # easy, medium, hard
            "snake_speed": "medium",  # easy, medium, hard (affects snake move interval)
        },
    }

    # Available options
    RESOLUTIONS = [
        "800x600",
        "1024x768",
        "1280x720",
        "1366x768",
        "1600x900",
        "1920x1080",
    ]

    WINDOW_MODES = ["windowed", "fullscreen", "borderless"]

    MAZE_DIFFICULTIES = {
        "easy": 30,  # Cell size in pixels
        "medium": 25,
        "hard": 20,
    }

    # Snake speed presets (seconds per move). Smaller = faster.
    SNAKE_MOVE_INTERVALS = {
        "easy": 0.18,
        "medium": 0.12,
        "hard": 0.08,
    }

    def __init__(self, settings_file: Path | None = None):
        """Initialize settings manager.

        Args:
            settings_file: Path to settings TOML file. If None, uses default location.
        """
        if settings_file is None:
            # Store in user's home directory
            config_dir = Path.home() / ".config" / "nayeoniegame"
            config_dir.mkdir(parents=True, exist_ok=True)
            settings_file = config_dir / "settings.toml"

        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> dict:
        """Load settings from TOML file or return defaults."""
        if not self.settings_file.exists():
            return self._deep_copy_dict(self.DEFAULTS)

        try:
            if tomllib is None:
                # Fallback to defaults if tomllib not available
                return self._deep_copy_dict(self.DEFAULTS)

            with open(self.settings_file, "rb") as f:
                loaded = tomllib.load(f)

            # Merge with defaults to handle missing keys
            settings = self._deep_copy_dict(self.DEFAULTS)
            self._deep_update(settings, loaded)
            return settings
        except Exception:
            # If file is corrupted, return defaults
            return self._deep_copy_dict(self.DEFAULTS)

    def _deep_copy_dict(self, d: dict) -> dict:
        """Deep copy a dictionary."""
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._deep_copy_dict(value)
            else:
                result[key] = value
        return result

    def _deep_update(self, target: dict, source: dict) -> None:
        """Deep update target dict with source dict."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def save(self) -> None:
        """Save settings to TOML file."""
        try:
            # Generate TOML manually (simple format)
            lines = []
            for section, values in self.settings.items():
                lines.append(f"[{section}]")
                for key, value in values.items():
                    if isinstance(value, str):
                        lines.append(f'{key} = "{value}"')
                    else:
                        lines.append(f"{key} = {value}")
                lines.append("")  # Empty line between sections

            self.settings_file.write_text("\n".join(lines))
        except Exception:
            pass  # Silently fail if can't write settings

    def get(self, section: str, key: str, default=None):
        """Get a setting value."""
        return self.settings.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value) -> None:
        """Set a setting value."""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value

    def get_resolution(self) -> tuple[int, int]:
        """Get resolution as (width, height) tuple."""
        res_str = self.get("video", "resolution", "800x600")
        try:
            width, height = res_str.split("x")
            return (int(width), int(height))
        except (ValueError, AttributeError):
            return (800, 600)

    def get_window_mode(self) -> str:
        """Get window mode."""
        return self.get("video", "window_mode", "windowed")

    def get_maze_cell_size(self) -> int:
        """Get maze cell size based on difficulty setting."""
        difficulty = self.get("gameplay", "maze_difficulty", "medium")
        return self.MAZE_DIFFICULTIES.get(difficulty, 25)

    def get_maze_difficulty(self) -> str:
        """Get maze difficulty setting."""
        return self.get("gameplay", "maze_difficulty", "medium")

    def get_snake_move_interval(self) -> float:
        """Get snake movement interval (seconds per move) based on settings.

        Returns a float number of seconds between snake steps.
        """
        difficulty = self.get("gameplay", "snake_speed", "medium")
        return float(self.SNAKE_MOVE_INTERVALS.get(difficulty, 0.12))
