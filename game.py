import numpy as np
import random


class Game:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.grid = []
        self.right = 0
        self.left = 1
        self.up = 2
        self.down = 3
        self.snake = []
        self.apple = ()
        self.direction = self.right
        self.score = 0

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
        self.add_apple()

    import random

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
            else:
                tail = self.snake.pop()
                self.grid[tail[1]][tail[0]] = 0

            self.grid[new_head[1]][new_head[0]] = 1
            return self.score, False
        else:
            return self.score, True
