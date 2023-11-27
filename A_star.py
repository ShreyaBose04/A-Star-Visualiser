import pygame
from queue import PriorityQueue

WIDTH = 1000
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Visualiser")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.size = width
        self.total_rows = total_rows
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbours = []
    
    def get_position(self):
        return self.row, self.col
    
    def isClosed(self):
        return self.color == RED
    
    def isOpen(self):
        return self.color == YELLOW
    
    def isObstacle(self):
        return self.color == BLACK
    
    def isSrc(self):
        return self.color == BLUE

    def isDest(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE
    
    def close(self):
        self.color = RED
    
    def open(self):
        self.color = YELLOW
    
    def make_obstacle(self):
        self.color = BLACK
    
    def make_src(self):
        self.color = BLUE

    def make_dest(self):
        self.color = PURPLE
    
    def add_path(self):
        self.color = GREEN

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def add_neighbours(self, grid):
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isObstacle():
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isObstacle():
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isObstacle():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isObstacle():
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.add_path()
        draw()

def algorithm(draw, grid, src, dest):
    draw()
    count = 0
    openSet  = PriorityQueue()
    came_from = {}
    g_score = {}
    f_score = {}

    for row in grid:
        for node in row:
            g_score[node] =  float("inf")

    g_score[src] = 0
    
    for row in grid:
        for node in row:
            f_score[node] =  float("inf")

    f_score[src] = h(src.get_position(), dest.get_position())

    openSet.put((f_score[src], count, src))
    open_set_hash = {src}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        open_set_hash.remove(current)

        if current == dest:
            reconstruct_path(came_from, dest, draw)
            dest.make_dest()
            src.make_src()
            return True
        
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                g_score[neighbour] = temp_g_score
                came_from[neighbour] = current
                f_score[neighbour] = temp_g_score + h(neighbour.get_position(), dest.get_position())

                if neighbour not in open_set_hash:
                    count+=1
                    neighbour.open()
                    openSet.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    
        draw()

        if current != src:
            current.close()

    return False


def make_grid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, width))


def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()

def get_click_pos(pos, rows, width):
    gap = width //rows
    y, x = pos

    row = y // gap
    col = x// gap

    return row, col

def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    src = None
    dest = None

    run = True

    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False\

            if pygame.mouse.get_pressed()[0]:   #left
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                node = grid[row][col]

                if not src and node != dest:
                    src = node
                    src.make_src()

                elif not dest and node != src:
                    dest = node
                    dest.make_dest()

                elif node != src and node != dest:
                    node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:  #right
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == src:
                    src = None
                elif node == dest:
                    dest = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and src and dest:
                    for row in grid:
                        for node in row:
                            node.add_neighbours(grid)
                
                    algorithm(lambda: draw(window, grid, ROWS, width), grid, src, dest)

                if event.key == pygame.K_c:
                    src = None
                    dest = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WINDOW, WIDTH)

    
