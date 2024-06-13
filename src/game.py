import time
import tkinter as tk
import random
import numpy as np

CELL_SIZE = 55


class Game:
    def __init__(self, root=None):
        self.root = root
        self.width = 10
        self.height = 10
        self.grid = []
        self.right = 0
        self.left = 1
        self.up = 2
        self.down = 3
        self.score = 0
        self.snake = []
        self.apple = ()
        self.direction = self.right

        if root is not None:
            self.window_size = self.width * CELL_SIZE
            self.root.title("Snake Game")
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            position_x = (screen_width // 2) - (self.window_size // 2)
            position_y = (screen_height // 2) - (self.window_size // 2) - 50
            root.geometry(f"{self.window_size}x{self.window_size + 30}+{position_x}+{position_y}")

            self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
            self.score_label.pack()

            self.canvas = tk.Canvas(root, width=self.window_size, height=self.window_size)
            self.canvas.pack()

            self.root.bind("<KeyPress-Escape>", self.close_game)
            self.running = True


    def reset(self):
        self.grid = np.zeros(shape=(self.height + 2, self.width + 2), dtype=int)
        self.grid[[0, -1], :] = 1
        self.grid[:, [0, -1]] = 1
        self.snake = [(5, 5), (4, 5), (3, 5)]
        for p in self.snake:
            self.grid[p[1]][p[0]] = 1
        self.add_apple()
        self.direction = self.right
        self.score = 0
        if self.root is not None:
            self.score_label.config(text=f"Score: {self.score}")

    def add_apple(self):
        empty_cells = [(x, y) for x in range(1, self.width + 1) for y in range(1, self.height + 1) if
                       self.grid[y][x] == 0]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.apple = (x, y)
            self.grid[y][x] = 2

    def do_step(self, direction):
        self.direction = direction
        head_x, head_y = self.snake[0]

        if self.direction == self.right:
            new_head = (head_x + 1, head_y)
        elif self.direction == self.left:
            new_head = (head_x - 1, head_y)
        elif self.direction == self.up:
            new_head = (head_x, head_y - 1)
        else:
            new_head = (head_x, head_y + 1)

        if self.grid[new_head[1]][new_head[0]] != 1:
            self.snake.insert(0, new_head)
            if self.grid[new_head[1]][new_head[0]] == 2:
                self.add_apple()
                self.score += 1
                if self.root is not None:
                    self.score_label.config(text=f"Score: {self.score}")
            else:
                tail = self.snake.pop()
                self.grid[tail[1]][tail[0]] = 0

            self.grid[new_head[1]][new_head[0]] = 1
            if self.root is not None:
                self.draw()
            return self.score, False
        else:
            return self.score, True

    def draw(self):
        self.canvas.delete(tk.ALL)
        for i in range(1, self.width + 1):
            for j in range(1, self.height + 1):
                # Définir la couleur du damier
                self.canvas.create_rectangle((i - 1) * CELL_SIZE, (j - 1) * CELL_SIZE,
                                             i * CELL_SIZE, j * CELL_SIZE,
                                             outline="", fill="#aad751" if (i + j) % 2 == 0 else "#9ac745")
                # Dessiner le serpent
                if self.grid[j][i] == 1:
                    self.canvas.create_rectangle((i - 1) * CELL_SIZE, (j - 1) * CELL_SIZE,
                                                 i * CELL_SIZE, j * CELL_SIZE,
                                                 fill="#4674e9")
                    if (i, j) == self.snake[0]:  # Tête du serpent
                        if self.direction == self.up:
                            self.draw_eye((i - 1), (j - 1), "top-left")
                            self.draw_eye((i - 1), (j - 1), "top-right")
                        elif self.direction == self.down:
                            self.draw_eye((i - 1), (j - 1), "bottom-left")
                            self.draw_eye((i - 1), (j - 1), "bottom-right")
                        elif self.direction == self.left:
                            self.draw_eye((i - 1), (j - 1), "top-left")
                            self.draw_eye((i - 1), (j - 1), "bottom-left")
                        elif self.direction == self.right:
                            self.draw_eye((i - 1), (j - 1), "top-right")
                            self.draw_eye((i - 1), (j - 1), "bottom-right")

                # Dessiner les pommes
                elif self.grid[j][i] == 2:
                    self.canvas.create_oval((i - 1) * CELL_SIZE + 10, (j - 1) * CELL_SIZE + 10,
                                            i * CELL_SIZE - 10, j * CELL_SIZE - 10,
                                            outline="", fill="#e7471d")

    def draw_eye(self, i, j, eye):
        if eye == "top-left":
            self.canvas.create_oval(i * CELL_SIZE + 10, j * CELL_SIZE + 10,
                                    (i + 1) * CELL_SIZE - 32, (j + 1) * CELL_SIZE - 32,
                                    outline="", fill="white")
            self.canvas.create_oval(i * CELL_SIZE + 14, j * CELL_SIZE + 14,
                                    (i + 1) * CELL_SIZE - 36, (j + 1) * CELL_SIZE - 36,
                                    outline="", fill="black")
        elif eye == "top-right":
            self.canvas.create_oval(i * CELL_SIZE + 32, j * CELL_SIZE + 10,
                                    (i + 1) * CELL_SIZE - 10, (j + 1) * CELL_SIZE - 32,
                                    outline="", fill="white")
            self.canvas.create_oval(i * CELL_SIZE + 36, j * CELL_SIZE + 14,
                                    (i + 1) * CELL_SIZE - 14, (j + 1) * CELL_SIZE - 36,
                                    outline="", fill="black")
        elif eye == "bottom-left":
            self.canvas.create_oval(i * CELL_SIZE + 10, j * CELL_SIZE + 32,
                                    (i + 1) * CELL_SIZE - 32, (j + 1) * CELL_SIZE - 10,
                                    outline="", fill="white")
            self.canvas.create_oval(i * CELL_SIZE + 14, j * CELL_SIZE + 36,
                                    (i + 1) * CELL_SIZE - 36, (j + 1) * CELL_SIZE - 14,
                                    outline="", fill="black")
        elif eye == "bottom-right":
            self.canvas.create_oval(i * CELL_SIZE + 32, j * CELL_SIZE + 32,
                                    (i + 1) * CELL_SIZE - 10, (j + 1) * CELL_SIZE - 10,
                                    outline="", fill="white")
            self.canvas.create_oval(i * CELL_SIZE + 36, j * CELL_SIZE + 36,
                                    (i + 1) * CELL_SIZE - 14, (j + 1) * CELL_SIZE - 14,
                                    outline="", fill="black")

    def close_game(self, event):
        self.running = False
        self.root.destroy()
