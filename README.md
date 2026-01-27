# Nayeonie Game

A pygame-based minigame collection built with uv and Nix flakes.

[![CI](https://github.com/ahuston-0/nayeoniegame/actions/workflows/ci.yml/badge.svg)](https://github.com/ahuston-0/nayeoniegame/actions/workflows/ci.yml)

[![Hippocratic License HL3-FULL](https://img.shields.io/static/v1?label=Hippocratic%20License&message=HL3-FULL&labelColor=5e2751&color=bc8c3d)](https://firstdonoharm.dev/version/3/0/full.html)

## Features

- **Modular minigame architecture** - Easy to add new minigames
- **Scene-based architecture** for game state management
- **Three playable minigames**:
  - **Free Movement**: Explore and move around freely with WASD/Arrow controls
  - **Color Collector**: Catch falling colored circles with a paddle
  - **Maze Runner**: Navigate through procedurally generated mazes
- **Comprehensive test suite** with >90% code coverage
- **Nix flakes** for reproducible development environment
- **uv** for fast, reliable Python package management

## Development Setup

### Prerequisites

- Nix with flakes enabled
- (Optional) direnv for automatic environment loading

### With Nix (Recommended)

Enter the development environment:

```bash
nix develop
```

If you're using direnv, it will automatically load when you enter the directory:

```bash
cd nayeoniegame
# Environment loads automatically with direnv
```

### Manual Setup (Without Nix)

Install uv and Python 3.10+, then:

```bash
uv sync
```

## Running the Game

**Note:** This game requires a graphical environment (X11, Wayland, or similar). It cannot run in headless environments like SSH sessions or containers without a virtual display.

Inside the Nix development shell or after running `uv sync`:

```bash
# Using uv (recommended)
uv run python -m nayeoniegame

# Or directly with Python
python -m nayeoniegame
```

### Running in Headless Environments

If you're in a headless environment (SSH, Docker, etc.), you can:

1. **Set up a virtual display** using Xvfb:
   ```bash
   # Install Xvfb
   nix-shell -p xorg.xorgserver

   # Run with virtual display
   xvfb-run -a python -m nayeoniegame
   ```

2. **Run the setup test** to verify everything works without needing a display:
   ```bash
   python -m nayeoniegame.test_setup
   ```

   This will test all imports, configuration, and basic game functionality.

## Building the Package

To build a distributable package with Nix:

```bash
nix build
./result/bin/nayeoniegame
```

## Minigames

### Free Movement
Move a cyan circle around the screen freely. Great for testing controls and exploring.
- **Controls**: WASD or Arrow keys to move, ESC to return to menu

### Color Collector
Catch falling colored circles with your paddle before they hit the bottom!
- **Controls**: A/D or Left/Right arrows to move paddle, ESC to return to menu
- **Objective**: Catch circles to increase score, avoid missing them (3 lives)

### Maze Runner
Navigate through procedurally generated mazes to reach the goal!
- **Controls**: WASD or Arrow keys to move, ESC to return to menu
- **Objective**: Find your way from the cyan starting position to the yellow goal
- **Challenge**: Beat your best time! The maze is randomly generated each playthrough

## Project Structure

```
nayeoniegame/
├── nayeoniegame/                      # Main game package
│   ├── __init__.py                    # Package initialization
│   ├── __main__.py                    # Entry point
│   ├── config.py                      # Game configuration constants
│   ├── game.py                        # Main game loop and window management
│   ├── scenes/                        # Game scenes
│   │   ├── __init__.py
│   │   ├── base.py                    # Base scene class
│   │   ├── main_menu.py               # Main menu scene
│   │   ├── minigame_selection.py      # Minigame selection menu
│   │   ├── minigame_movement.py       # Free movement minigame
│   │   ├── minigame_color_collector.py # Color collector minigame
│   │   └── minigame_maze_runner.py    # Maze runner minigame
│   └── entities/                      # Game sprites and objects
│       ├── __init__.py
│       ├── player.py                  # Player character (movement minigame)
│       ├── paddle.py                  # Paddle (color collector)
│       ├── falling_circle.py          # Falling circle (color collector)
│       ├── maze.py                    # Maze generation (maze runner)
│       └── maze_player.py             # Grid-based player (maze runner)
├── tests/                             # Unit tests
│   ├── conftest.py                    # Pytest fixtures
│   ├── test_entities_*.py             # Entity tests
│   └── test_scenes_*.py               # Scene tests
├── pyproject.toml                     # Python project configuration
├── uv.lock                            # Locked dependencies
└── flake.nix                          # Nix flake configuration
```

## Controls

### Main Menu
- **UP/DOWN arrows**: Navigate menu options
- **ENTER**: Select option
- **ESC**: Return to previous menu (or quit from main menu)

### Free Movement Minigame
- **WASD** or **Arrow keys**: Move player in all directions
- **ESC**: Return to minigame selection

### Color Collector Minigame
- **A/D** or **Left/Right arrows**: Move paddle horizontally
- **ESC**: Return to minigame selection
- **ENTER**: Continue after game over

### Maze Runner Minigame
- **WASD** or **Arrow keys**: Move player one cell at a time (discrete movement)
- **ESC**: Return to minigame selection
- **ENTER**: Continue after winning

## Dependencies

- Python 3.10+
- pygame 2.6.0+

## Development

The project uses:
- **uv** for dependency management
- **hatchling** as the build backend (PEP 621 compliant)
- **Nix flakes** for reproducible development environments
- **pygame** for game development
- **pytest** with coverage for testing
- **ruff** for linting and formatting

### Running Tests

Run the full test suite with coverage:

```bash
# Inside Nix shell
nix develop --command uv run pytest

# Or just
uv run pytest
```

The test suite includes:
- **68 unit tests** covering all entities and scenes
- **91.9% code coverage** (minimum 80% enforced)
- Headless pygame testing using dummy video driver

### View Coverage Report

```bash
# Generate HTML coverage report
uv run pytest

# Open the report
firefox htmlcov/index.html  # Or your preferred browser
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Type checking
uv run ty check nayeoniegame
```

### Adding New Minigames

The modular architecture makes it easy to add new minigames:

1. Create your minigame scene in `nayeoniegame/scenes/minigame_yourname.py`
2. Add it to the `MINIGAMES` list in `nayeoniegame/scenes/minigame_selection.py`
3. Add the import case in `_select_option()` method
4. Write unit tests in `tests/test_scenes_minigame_yourname.py`

See [minigame_color_collector.py](nayeoniegame/scenes/minigame_color_collector.py) for a complete example.

### Adding New Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --group dev package-name
```

## License

(Add your license here)
