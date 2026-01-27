# Nayeonie Game

A pygame-based game built with uv and Nix flakes.

## Features

- **Scene-based architecture** for easy game state management
- **Player movement** with keyboard controls (WASD/Arrow keys)
- **Main menu** with navigation
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

## Project Structure

```
nayeoniegame/
├── nayeoniegame/          # Main game package
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point
│   ├── config.py          # Game configuration constants
│   ├── game.py            # Main game loop and window management
│   ├── scenes/            # Game scenes (menu, gameplay, etc.)
│   │   ├── __init__.py
│   │   ├── base.py        # Base scene class
│   │   ├── main_menu.py   # Main menu scene
│   │   └── gameplay.py    # Gameplay scene
│   ├── entities/          # Game sprites and objects
│   │   ├── __init__.py
│   │   └── player.py      # Player character
│   └── assets/            # Game assets (images, sounds, fonts)
├── pyproject.toml         # Python project configuration (uv/pip)
├── uv.lock                # Locked dependencies
└── flake.nix              # Nix flake configuration
```

## Controls

### Main Menu
- **UP/DOWN arrows**: Navigate menu options
- **ENTER**: Select option

### Gameplay
- **WASD** or **Arrow keys**: Move player
- **ESC**: Return to main menu

## Dependencies

- Python 3.10+
- pygame 2.6.0+

## Development

The project uses:
- **uv** for dependency management
- **hatchling** as the build backend (PEP 621 compliant)
- **Nix flakes** for reproducible development environments
- **pygame** for game development

To add new dependencies:

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name
```

## License

(Add your license here)
