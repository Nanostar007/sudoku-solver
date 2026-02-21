## Sudoku Solver

Simple desktop Sudoku solver with nice GUI.  
Write numbers, get automatic solve, hints, input validation, row/column/block highlight.

# Features
- 9×9 grid with clear 3×3 blocks
- Type numbers → auto jump to next empty cell
- SPACEBAR or button → get one safe hint
- Shows invalid moves in red
- Highlights current row, column and block in light blue
- Counts empty cells
- Solve button uses backtracking (fast on normal puzzles)
- Clear button resets everything
- Pre-filled numbers stay read-only after solve

# Requirements
- Python 3.8+
- tkinter (usually comes with Python)

# Install & Run

git clone https://github.com/Nanostar007/sudoku-solver.git
cd sudoku-solver
python sudoku_solver.py


# Controls
- Click or tab to move between cells
- Backspace on empty cell → jumps back
- SPACE → hint

# Screenshots

<img width="810" height="861" alt="Screenshot 2026-02-21 225425" src="https://github.com/user-attachments/assets/0484df3a-3169-491e-bda4-feb0feca3cca" />
<img width="810" height="862" alt="Screenshot 2026-02-21 225417" src="https://github.com/user-attachments/assets/377da45e-1149-4c75-a3ba-b8bf3c85f57c" />


# License
MIT License – feel free to use, modify, share.
