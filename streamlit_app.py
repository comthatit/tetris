import streamlit as st
import pygame
import random
import numpy as np

# Initialize pygame and set constants
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

# Initialize game variables
def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def valid_move(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = off_x + x
                new_y = off_y + y
                if (
                    new_x < 0
                    or new_x >= COLS
                    or new_y >= ROWS
                    or (new_y >= 0 and grid[new_y][new_x])
                ):
                    return False
    return True

# Draw the grid
def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = WHITE if cell else BLACK
            pygame.draw.rect(
                surface,
                color,
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                0,
            )
            pygame.draw.rect(
                surface,
                RED,
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1,
            )

# Main function for Streamlit
def main():
    st.title("Classic Tetris Game")

    st.write("Use your keyboard arrow keys to play.")

    if "grid" not in st.session_state:
        st.session_state.grid = create_grid()
    if "current_piece" not in st.session_state:
        st.session_state.current_piece = random.choice(SHAPES)
    if "current_position" not in st.session_state:
        st.session_state.current_position = [0, COLS // 2 - len(st.session_state.current_piece[0]) // 2]

    # Streamlit does not support pygame directly, so we notify users.
    st.warning("This implementation works better as a local app using pygame. For now, the game logic is set up but not interactable in Streamlit.")

    # Example rendering of the grid
    grid = np.array(st.session_state.grid)
    grid_html = "<table style='border-collapse: collapse;'>"
    for row in grid:
        grid_html += "<tr>"
        for cell in row:
            color = "#FFFFFF" if cell else "#000000"
            grid_html += f"<td style='width: {BLOCK_SIZE}px; height: {BLOCK_SIZE}px; background-color: {color}; border: 1px solid #FF0000;'></td>"
        grid_html += "</tr>"
    grid_html += "</table>"

    st.markdown(grid_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

