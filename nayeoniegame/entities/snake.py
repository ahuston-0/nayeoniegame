"""Snake entity representing game logic for snake movement and food.

This keeps movement, collision, and scoring logic separated from rendering.
"""

import random


class Snake:
    """Entity encapsulating snake game state and logic."""

    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.reset()

    def reset(self):
        mid_col = self.cols // 2
        mid_row = self.rows // 2
        self.segments = [(mid_col, mid_row), (mid_col - 1, mid_row), (mid_col - 2, mid_row)]
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.spawn_food()

    def spawn_food(self):
        # Choose from available free cells to avoid infinite loop when board is nearly full
        free_cells = [
            (c, r)
            for c in range(self.cols)
            for r in range(self.rows)
            if (c, r) not in self.segments
        ]

        if not free_cells:
            # No free cell available — treat as win / end condition
            self.food = None
            self.game_over = True
            return

        self.food = random.choice(free_cells)

    def set_direction(self, new_dir):
        # Prevent reversing into self
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        self.direction = new_dir

    def step(self):
        """Advance the snake by one cell. Update score and game_over as needed."""
        if self.game_over:
            return

        head = self.segments[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= self.cols
            or new_head[1] < 0
            or new_head[1] >= self.rows
        ):
            self.game_over = True
            return

        # Self collision
        if new_head in self.segments:
            self.game_over = True
            return

        # Move
        self.segments.insert(0, new_head)

        # Eat
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.segments.pop()
