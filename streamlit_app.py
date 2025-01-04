import streamlit as st
import random
from streamlit.components.v1 import html

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

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

# Create empty grid
def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Check if move is valid
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

# Rotate shape
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Place shape on the grid
def place_shape(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[off_y + y][off_x + x] = cell

# Clear full rows
def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_grid)
    new_grid = [[0 for _ in range(COLS)] for _ in range(cleared)] + new_grid
    return new_grid, cleared

# Draw the grid in Streamlit
def draw_grid(grid):
    grid_html = "<table style='border-collapse: collapse;'>"
    for row in grid:
        grid_html += "<tr>"
        for cell in row:
            color = "#FFFFFF" if cell else "#000000"
            grid_html += f"<td style='width: {BLOCK_SIZE}px; height: {BLOCK_SIZE}px; background-color: {color}; border: 1px solid #CCCCCC;'></td>"
        grid_html += "</tr>"
    grid_html += "</table>"
    return grid_html

# Main function
def main():
    st.title("Tetris Game")

    st.markdown(
        """
        ### How to Play
        - **Start**: Press the Spacebar to start the game.
        - **Move Left**: Press the Left Arrow key.
        - **Move Down**: Press the Down Arrow key.
        - **Move Right**: Press the Right Arrow key.
        - **Rotate**: Press the Up Arrow key.
        """
    )

    if "grid" not in st.session_state:
        st.session_state.grid = create_grid()
    if "current_piece" not in st.session_state:
        st.session_state.current_piece = random.choice(SHAPES)
    if "current_position" not in st.session_state:
        st.session_state.current_position = [0, COLS // 2 - len(st.session_state.current_piece[0]) // 2]
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    def handle_keypress(key):
        grid = st.session_state.grid
        current_piece = st.session_state.current_piece
        current_position = st.session_state.current_position

        if key == "ArrowLeft":
            new_position = [current_position[0], current_position[1] - 1]
            if valid_move(grid, current_piece, new_position):
                st.session_state.current_position = new_position
        elif key == "ArrowDown":
            new_position = [current_position[0] + 1, current_position[1]]
            if valid_move(grid, current_piece, new_position):
                st.session_state.current_position = new_position
            else:
                place_shape(grid, current_piece, current_position)
                st.session_state.grid, cleared = clear_rows(grid)
                st.session_state.score += cleared * 10
                st.session_state.current_piece = random.choice(SHAPES)
                st.session_state.current_position = [0, COLS // 2 - len(st.session_state.current_piece[0]) // 2]
        elif key == "ArrowRight":
            new_position = [current_position[0], current_position[1] + 1]
            if valid_move(grid, current_piece, new_position):
                st.session_state.current_position = new_position
        elif key == "ArrowUp":
            rotated_piece = rotate_shape(current_piece)
            if valid_move(grid, rotated_piece, current_position):
                st.session_state.current_piece = rotated_piece
        elif key == "Space":
            st.session_state.game_started = True

    # Render grid
    temp_grid = [row[:] for row in st.session_state.grid]
    if st.session_state.game_started:
        for y, row in enumerate(st.session_state.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    temp_grid[st.session_state.current_position[0] + y][st.session_state.current_position[1] + x] = cell

    st.markdown(draw_grid(temp_grid), unsafe_allow_html=True)

    html(
        """
        <script>
        document.addEventListener('keydown', function(event) {
            var key = event.key;
            var parent = window.parent;
            parent.postMessage({key: key}, '*');
        });
        </script>
        """,
        height=0,
    )

    st.write(f"Score: {st.session_state.score}")

    key_event = st.query_params.get("key", [None])[0]
    if key_event:
        handle_keypress(key_event)

if __name__ == "__main__":
    main()
