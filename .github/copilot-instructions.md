# Copilot instructions for Nayeoniegame

This file gives concise, project-specific guidance so an AI coding agent can be immediately productive.

Summary
- The project is a small Pygame application structured around a single `Game` class (main loop + scene manager).
- High-level components: `nayeoniegame/game.py` (loop & scene switching), `nayeoniegame/scenes/` (UI/game scenes),
  and `nayeoniegame/entities/` (game objects / sprites). Settings are managed by `nayeoniegame/settings.py`.

Big picture / architecture
- `Game` holds a reference to the current `Scene` and exposes `change_scene()` and `quit()` for scene code to call.
- Scenes subclass `Scene` (see `nayeoniegame/scenes/base.py`) and receive the `game` instance in their constructor.
  They implement `handle_event(event)`, `update(dt)`, and `render(screen)`.
- Scenes often import other scenes lazily inside handlers to avoid circular imports (see `minigame_maze_runner.py`).
- Entities live in `nayeoniegame/entities/` and often subclass `pygame.sprite.Sprite` (e.g. `MazePlayer`).
- `nayeoniegame/config.py` contains global constants; prefer using those values for visuals/behavior.

Project-specific conventions & patterns
- Scene transitions: call `game.change_scene(NewScene(self.game))` from within a scene.
- Lazy imports: import other scenes inside methods (not at module top-level) to prevent import cycles.
- Grid-based games: Maze uses odd-sized grids; cell size comes from `SettingsManager.get_maze_cell_size()`.
- Settings persistence: `SettingsManager` writes a simple TOML to `~/.config/nayeoniegame/settings.toml` by default.
- Tests run with a headless SDL driver: tests set `SDL_VIDEODRIVER = dummy` in `tests/conftest.py`.

Key files (examples)
- Entry and loop: `nayeoniegame/game.py`
- Settings & persistence: `nayeoniegame/settings.py` (defaults, TOML load/save, maze difficulty mapping)
- Scenes: `nayeoniegame/scenes/` (see `minigame_maze_runner.py` for a representative scene)
- Entities: `nayeoniegame/entities/` (see `maze.py`, `maze_player.py` for maze logic + grid movement)
- Constants: `nayeoniegame/config.py` (screen sizes, colors, maze defaults)

Developer workflows / commands
- This project uses Nix Flakes (`flake.nix`) for reproducible developer environments and `uv` to run
  Python binaries from the project's virtualenv. If a required binary isn't on your PATH, run `nix develop`
  in the repo root to enter the dev shell.

- Typical commands (prefer running via `uv` inside the dev shell):

  # Enter Nix dev shell (if needed)
  nix develop

  # Run tests (headless SDL is configured in tests):
  uv run python -m pytest

  # Run tests with coverage:
  uv run python -m pytest --cov

  # Run the game locally (interactive):
  uv run python -m nayeoniegame

  # Quick import sanity check (headless):
  uv run python -c "from nayeoniegame.game import Game; print('Import successful')"

  # Install in editable mode for development (inside dev shell):
  uv run python -m pip install -e .

Linting / formatting
- Ruff is configured in `pyproject.toml` (line-length 100). Run `ruff .` or `ruff check .`.

Testing notes and gotchas
- Tests rely on `pygame` with `SDL_VIDEODRIVER=dummy`. If you run tests manually in your shell, export that env var if needed.
- The repository includes `flake.nix`; if a developer dependency or binary is missing, run `nix develop` first.
- This project uses `uv` to run Python and other tools inside the virtualenv created by the flake/dev environment
  (example: `uv run python -m pytest`). Prefer `uv run` so the correct interpreter and installed packages are used.
- Some UI-focused modules are omitted from coverage by design (see `[tool.coverage.run].omit` in `pyproject.toml`).
- Settings file location: tests use a temporary file via `SettingsManager(tmp_path / "test_settings.toml")` — follow that pattern when writing tests.

How to approach changes
- Preserve the `Scene` pattern; prefer adding new scenes under `nayeoniegame/scenes/` subclassing `Scene`.
- Use `SettingsManager` for configurable behavior (e.g., maze difficulty), avoid hardcoding in scenes.
- Use lazy imports for scene-to-scene transitions to avoid circular imports.
- Keep visual constants in `nayeoniegame/config.py` so other files stay decoupled from magic numbers.

Examples (copy-ready)
- Switch back to selection from a scene:

  from .minigame_selection import MinigameSelectionScene
  self.game.change_scene(MinigameSelectionScene(self.game))

- Query maze cell size in a scene:

  cell_size = game.settings_manager.get_maze_cell_size()

If anything in this summary is unclear or you want more examples (tests, adding a scene, or debugging tips), tell me which sections to expand.
