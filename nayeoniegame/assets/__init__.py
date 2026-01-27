"""Simple asset loader for the game.

Provides a thin API to load and cache image Surfaces. If a file is missing
or running in a headless/test environment, a simple placeholder Surface is
generated using the project's color constants.

Usage:
  from nayeoniegame.assets import get_image
  surf = get_image('maze_wall', size=(32,32))
"""

from __future__ import annotations

from pathlib import Path

import pygame

from .. import config

ASSET_DIR = Path(__file__).parent

# Basic color mapping for placeholders (name -> rgb tuple)
PLACEHOLDER_COLORS = {
    "maze_wall": config.WHITE,
    "maze_floor": (40, 40, 40),
    "player": config.CYAN,
    "circle": config.RED,
}

_cache: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}


def _create_placeholder(name: str, size: tuple[int, int]) -> pygame.Surface:
    """Create a simple placeholder surface for the given asset name and size."""
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    color = PLACEHOLDER_COLORS.get(name, config.WHITE)

    if name == "circle":
        # draw a circle on transparent background
        surf.fill((0, 0, 0, 0))
        pygame.draw.circle(surf, color, (w // 2, h // 2), min(w, h) // 2 - 2)
    elif name == "player":
        surf.fill((0, 0, 0, 0))
        pygame.draw.circle(surf, color, (w // 2, h // 2), min(w, h) // 2 - 2)
    else:
        surf.fill(color)

    return surf


def _try_load_file(name: str) -> Path | None:
    """Return a file path for known asset names if it exists (png preferred)."""
    # Prefer PNG, but allow SVG placeholders to exist in repo for humans
    png_path = ASSET_DIR / f"{name}.png"
    if png_path.exists():
        return png_path

    svg_path = ASSET_DIR / f"{name}.svg"
    if svg_path.exists():
        # Not loadable by pygame; still keep for editors / designers.
        return None

    return None


def get_image(name: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    """Return a `pygame.Surface` for the named asset.

    If `size` is provided the image will be scaled (or a placeholder sized)
    accordingly. Results are cached.
    """
    key = (name, size)
    if key in _cache:
        return _cache[key]

    file_path = _try_load_file(name)

    try:
        if file_path is not None:
            img = pygame.image.load(str(file_path)).convert_alpha()
            if size is not None:
                img = pygame.transform.smoothscale(img, size)
            _cache[key] = img
            return img
    except Exception:
        # Fall through and create placeholder
        pass

    # Create a generated placeholder surface
    if size is None:
        size = (32, 32)

    surf = _create_placeholder(name, size)
    _cache[key] = surf
    return surf
