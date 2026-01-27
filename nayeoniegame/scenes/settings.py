"""Settings menu scene."""

import pygame

from .. import config
from ..settings import SettingsManager
from .base import Scene


class SettingsScene(Scene):
    """Settings menu for configuring game options."""

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 28)
        self.settings_manager = game.settings_manager

        # Menu structure: (label, setting_section, setting_key, options)
        self.menu_items = [
            (
                "Resolution",
                "video",
                "resolution",
                SettingsManager.RESOLUTIONS,
            ),
            (
                "Window Mode",
                "video",
                "window_mode",
                ["windowed", "fullscreen", "borderless"],
            ),
            (
                "Maze Difficulty",
                "gameplay",
                "maze_difficulty",
                ["easy", "medium", "hard"],
            ),
            (
                "Snake Speed",
                "gameplay",
                "snake_speed",
                ["easy", "medium", "hard"],
            ),
            ("Back to Main Menu", None, None, None),
        ]

        self.selected_option = 0
        self.editing_option = False

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Save and return to main menu
                self._save_and_exit()
            elif event.key == pygame.K_UP:
                if not self.editing_option:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                if not self.editing_option:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_option()
            elif event.key == pygame.K_LEFT:
                if self.editing_option:
                    self._change_value(-1)
            elif event.key == pygame.K_RIGHT:
                if self.editing_option:
                    self._change_value(1)

    def _select_option(self):
        """Handle option selection."""
        if self.selected_option == len(self.menu_items) - 1:
            # Back to Main Menu
            self._save_and_exit()
        else:
            # Toggle editing mode for settings
            self.editing_option = not self.editing_option

    def _change_value(self, direction: int):
        """Change the selected setting value.

        Args:
            direction: -1 for left/previous, 1 for right/next
        """
        label, section, key, options = self.menu_items[self.selected_option]

        if section is None or options is None:
            return

        current_value = self.settings_manager.get(section, key)
        try:
            current_index = options.index(current_value)
            new_index = (current_index + direction) % len(options)
            new_value = options[new_index]
            self.settings_manager.set(section, key, new_value)

            # Apply video settings immediately
            if section == "video":
                self._apply_video_settings()

        except (ValueError, IndexError):
            pass

    def _apply_video_settings(self):
        """Apply video settings immediately (requires restart message)."""
        # Note: Actual resolution change requires game restart
        # We just save the setting here
        pass

    def _save_and_exit(self):
        """Save settings and return to main menu."""
        self.settings_manager.save()

        from .main_menu import MainMenuScene

        self.game.change_scene(MainMenuScene(self.game))

    def update(self, dt):
        """Update settings menu state."""
        pass  # No updates needed for static menu

    def render(self, screen):
        """Render the settings menu."""
        screen.fill(config.BLACK)

        # Draw title
        title_text = self.font.render("Settings", True, config.CYAN)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # Draw menu items
        start_y = 150
        spacing = 60

        for i, (label, section, key, _options) in enumerate(self.menu_items):
            y_pos = start_y + i * spacing

            # Determine color
            if i == self.selected_option:
                if self.editing_option and section is not None:
                    color = config.GREEN
                else:
                    color = config.YELLOW
            else:
                color = config.WHITE

            # Draw label
            if section is None:
                # Back button
                text = self.small_font.render(label, True, color)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, y_pos))
                screen.blit(text, text_rect)
            else:
                # Setting with value
                current_value = self.settings_manager.get(section, key, "")
                display_value = str(current_value).replace("_", " ").title()

                # Draw label on left
                label_text = self.small_font.render(f"{label}:", True, color)
                label_rect = label_text.get_rect(midright=(config.SCREEN_WIDTH // 2 - 20, y_pos))
                screen.blit(label_text, label_rect)

                # Draw value on right
                value_text = self.small_font.render(display_value, True, color)
                value_rect = value_text.get_rect(midleft=(config.SCREEN_WIDTH // 2 + 20, y_pos))
                screen.blit(value_text, value_rect)

                # Draw arrows if editing
                if i == self.selected_option and self.editing_option:
                    left_arrow = self.small_font.render("<", True, color)
                    right_arrow = self.small_font.render(">", True, color)
                    screen.blit(
                        left_arrow,
                        (value_rect.left - 30, y_pos - left_arrow.get_height() // 2),
                    )
                    screen.blit(
                        right_arrow,
                        (value_rect.right + 20, y_pos - right_arrow.get_height() // 2),
                    )

        # Draw instructions
        if self.editing_option:
            instructions = "LEFT/RIGHT: Change | ENTER: Done | ESC: Save & Exit"
        else:
            instructions = "UP/DOWN: Navigate | ENTER: Edit | ESC: Save & Exit"

        instructions_text = self.small_font.render(instructions, True, config.WHITE)
        instructions_rect = instructions_text.get_rect(
            center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 40)
        )
        screen.blit(instructions_text, instructions_rect)

        # Restart notice for video settings
        if (
            self.settings_manager.get("video", "resolution")
            != f"{config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}"
            or self.settings_manager.get("video", "window_mode") != "windowed"
        ):
            notice_text = self.small_font.render(
                "* Video changes require game restart",
                True,
                (200, 200, 0),
            )
            notice_rect = notice_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 80)
            )
            screen.blit(notice_text, notice_rect)
