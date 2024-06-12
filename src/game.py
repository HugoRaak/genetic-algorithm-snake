import tkinter as tk
import random

GRID_SIZE = 10
CELL_SIZE = 55
WINDOW_SIZE = GRID_SIZE * CELL_SIZE


class Game:
    def __init__(self, root, display=False):
        self.root = root
        self.display = display
        self.root.title("Snake Game")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (WINDOW_SIZE // 2)
        position_y = (screen_height // 2) - (WINDOW_SIZE // 2) - 50
        root.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE + 30}+{position_x}+{position_y}")

        self.score = 0
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()

        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
        self.canvas.pack()

        # Initialisation de la grille
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Position initiale du serpent
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.grid[5][5] = 1
        self.grid[5][4] = 1
        self.grid[5][3] = 1
        self.direction = 'Right'

        # Ajout de la première pomme
        self.add_apple()

        # Liaison des touches
        self.root.bind("<KeyPress>", self.change_direction)

        self.updated = False

        # Démarrer le jeu
        self.update()

    def add_apple(self):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 2
                break

    def change_direction(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            opposite_directions = {
                'Right': 'Left',
                'Left': 'Right',
                'Up': 'Down',
                'Down': 'Up'
            }
            if self.direction == opposite_directions.get(event.keysym) or not self.updated:
                return
            self.direction = event.keysym
            self.updated = False

    def update(self):
        head_x, head_y = self.snake[0]

        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)

        if (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE and self.grid[new_head[1]][new_head[0]] != 1):
            self.snake.insert(0, new_head)
            if self.grid[new_head[1]][new_head[0]] == 2:
                self.add_apple()
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
            else:
                tail = self.snake.pop()
                self.grid[tail[1]][tail[0]] = 0

            self.grid[new_head[1]][new_head[0]] = 1
            if self.display:
                self.draw()
                self.root.after(200, self.update)
            else:
                self.update()
        else:
            self.gameover()

        self.updated = True

    def draw(self):
        self.canvas.delete(tk.ALL)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # Définir la couleur du damier
                self.canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                             (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                             outline="", fill="#aad751" if (i + j) % 2 == 0 else "#9ac745")
                # Dessiner le serpent
                if self.grid[j][i] == 1:
                    self.canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE,
                                                 (i + 1) * CELL_SIZE, (j + 1) * CELL_SIZE,
                                                 fill="#4674e9")
                    if (i, j) == self.snake[0]:  # Tête du serpent
                        if self.direction == 'Up':
                            self.drawEye(i, j, "top-left")
                            self.drawEye(i, j, "top-right")
                        elif self.direction == 'Down':
                            self.drawEye(i, j, "bottom-left")
                            self.drawEye(i, j, "bottom-right")
                        elif self.direction == 'Left':
                            self.drawEye(i, j, "top-left")
                            self.drawEye(i, j, "bottom-left")
                        elif self.direction == 'Right':
                            self.drawEye(i, j, "top-right")
                            self.drawEye(i, j, "bottom-right")

                # Dessiner les pommes
                elif self.grid[j][i] == 2:
                    self.canvas.create_oval(i * CELL_SIZE + 10, j * CELL_SIZE + 10,
                                            (i + 1) * CELL_SIZE - 10, (j + 1) * CELL_SIZE - 10,
                                            outline="", fill="#e7471d")

    def drawEye(self, i, j, eye):
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

    def gameover(self):
        self.canvas.create_rectangle(WINDOW_SIZE // 2 - 150, WINDOW_SIZE // 2 - 50,
                                     WINDOW_SIZE // 2 + 150, WINDOW_SIZE // 2 + 50,
                                     fill="#42551f")
        self.canvas.create_text(WINDOW_SIZE // 2, WINDOW_SIZE // 2,
                                text="Game Over", fill="white", font=("Arial", 30))
        self.root.bind("<KeyPress>", self.close_game)

    def close_game(self, event):
        self.root.destroy()