import tkinter as tk
from tkinter import messagebox
import random

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num: return False
    for x in range(9):
        if board[x][col] == num: return False
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num: return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def get_board():
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get().strip()
            row.append(int(val) if val.isdigit() and 1 <= int(val) <= 9 else 0)
        board.append(row)
    return board

def put_board(board):
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal", bg="white")
            entries[i][j].delete(0, tk.END)
            if board[i][j] != 0:
                entries[i][j].insert(0, str(board[i][j]))
                if original[i][j] != 0:
                    entries[i][j].config(state="disabled", disabledforeground="black")
            else:
                entries[i][j].config(state="normal")

def solve():
    board = get_board()
    board_copy = [row[:] for row in board]
    if solve_sudoku(board_copy):
        put_board(board_copy)
        update_count()
    else:
        messagebox.showinfo("Result", "No solution found")

def clear():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal", bg="white")
            entries[i][j].delete(0, tk.END)
    original[:] = [[0]*9 for _ in range(9)]
    update_count()
    clear_highlights()

def update_count():
    count = sum(1 for row in entries for e in row if e.get().strip() == "")
    count_label.config(text=f"Empty cells: {count}")

def give_hint():
    board = get_board()
    empties = [(i,j) for i in range(9) for j in range(9) if board[i][j] == 0]
    if not empties:
        messagebox.showinfo("Hint", "No empty cells left")
        return
    i, j = random.choice(empties)
    for num in range(1, 10):
        if is_valid(board, i, j, num):
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(num))
            entries[i][j].config(bg="#e0ffe0")  # light green for hint
            update_count()
            return
    messagebox.showinfo("Hint", "Cannot find safe hint right now")

def validate_input(event):
    widget = event.widget
    if not widget.cget("state") == "normal":
        return "break"
    if event.char.isdigit() and '1' <= event.char <= '9':
        widget.delete(0, tk.END)
        widget.insert(0, event.char)
        row, col = find_widget(widget)
        board = get_board()
        if not is_valid(board, row, col, int(event.char)):
            widget.config(bg="#ffcccc")  # light red for error
        else:
            widget.config(bg="white")
        move_next()
        update_count()
        return "break"
    elif event.keysym in ('BackSpace', 'Delete'):
        widget.config(bg="white")
        if widget.get() == "":
            move_prev()
        update_count()
        return None
    elif event.keysym == "space":
        give_hint()
        return "break"
    return "break"

def find_widget(widget):
    for i in range(9):
        for j in range(9):
            if entries[i][j] == widget:
                return i, j
    return -1, -1

def highlight(event):
    clear_highlights()
    widget = event.widget
    if not isinstance(widget, tk.Entry): return
    row, col = find_widget(widget)
    if row == -1: return
    # row
    for j in range(9):
        entries[row][j].config(bg="#e3f2fd" if entries[row][j].cget("state")=="normal" else entries[row][j].cget("bg"))
    # column
    for i in range(9):
        entries[i][col].config(bg="#e3f2fd" if entries[i][col].cget("state")=="normal" else entries[i][col].cget("bg"))
    # block
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            entries[start_row+i][start_col+j].config(bg="#e3f2fd" if entries[start_row+i][start_col+j].cget("state")=="normal" else entries[start_row+i][start_col+j].cget("bg"))
    widget.focus()

def clear_highlights():
    for i in range(9):
        for j in range(9):
            if entries[i][j].cget("state") == "normal" and entries[i][j].get().strip() == "":
                entries[i][j].config(bg="white")
            elif entries[i][j].cget("bg") == "#e3f2fd":
                entries[i][j].config(bg="white")

def move_next(event=None):
    widget = root.focus_get()
    if not isinstance(widget, tk.Entry): return
    row, col = find_widget(widget)
    if row == -1: return
    if col < 8 and entries[row][col+1].get() == "":
        entries[row][col+1].focus()
        return
    for ni in range(row, 9):
        startj = 0 if ni > row else col + 1
        for nj in range(startj, 9):
            if entries[ni][nj].get() == "":
                entries[ni][nj].focus()
                return

def move_prev(event=None):
    widget = root.focus_get()
    if not isinstance(widget, tk.Entry): return
    row, col = find_widget(widget)
    if row == -1: return
    if col > 0 and entries[row][col-1].get() == "":
        entries[row][col-1].focus()
        return
    for ni in range(row, -1, -1):
        endj = 8 if ni < row else col - 1
        for nj in range(endj, -1, -1):
            if entries[ni][nj].get() == "":
                entries[ni][nj].focus()
                return

# ── Window ───────────────────────────────────────────────
root = tk.Tk()
root.title("Sudoku Solver")
root.configure(bg="white")
root.resizable(False, False)

entries = [[None] * 9 for _ in range(9)]
original = [[0] * 9 for _ in range(9)]

for i in range(9):
    for j in range(9):
        entry = tk.Entry(
            root, width=3, font=("Arial", 22, "bold"),
            justify="center", bg="white", relief="solid", borderwidth=1
        )
        entry.grid(
            row=i, column=j,
            padx=(6 if j % 3 == 0 else 1, 6 if (j + 1) % 3 == 0 else 1),
            pady=(6 if i % 3 == 0 else 1, 6 if (i + 1) % 3 == 0 else 1),
            ipadx=8, ipady=8
        )
        entry.bind("<Key>", validate_input)
        entry.bind("<FocusIn>", highlight)
        entry.bind("<Button-1>", highlight)
        entries[i][j] = entry

frame = tk.Frame(root, bg="white")
frame.grid(row=9, column=0, columnspan=9, pady=20)

hint_button = tk.Button(frame, text="HINT", font=("Arial", 14, "bold"),
                        bg="#FF9800", fg="white", width=10, height=2, command=give_hint)
hint_button.pack(side="left", padx=15)

solve_button = tk.Button(frame, text="SOLVE", font=("Arial", 14, "bold"),
                         bg="#4CAF50", fg="white", width=10, height=2, command=solve)
solve_button.pack(side="left", padx=15)

clear_button = tk.Button(frame, text="CLEAR", font=("Arial", 14, "bold"),
                         bg="#f44336", fg="white", width=10, height=2, command=clear)
clear_button.pack(side="left", padx=15)

count_label = tk.Label(root, text="Empty cells: 81", font=("Arial", 12), bg="white")
count_label.grid(row=10, column=0, columnspan=9, pady=5)

root.bind("<space>", lambda e: give_hint())

update_count()

root.mainloop()