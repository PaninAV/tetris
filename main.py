import pygame
import random
import time

pygame.init()
pygame.mixer.music.set_volume(0.1)

colors = [
    (128, 0, 128),
    (123, 104, 238),
    (70, 130, 180),
    (75, 0, 130),
    (128, 0, 0),
    (139, 69, 19),
    (0, 128, 0),
    (199, 21, 133),
    (255, 215, 0),
    (255, 69, 0),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 0
    score = 0
    state = "play"
    field = []
    # размеры полтонка
    height = 0
    width = 0
    # начальные координаты полотна
    x = 60
    y = 60
    # размер клетки
    zoom = 31
    figure = None
    next_figure = None

    def __init__(self, height, width, level):
        self.height = height
        self.width = width
        self.level = level
        self.field = []
        self.score = 0
        self.state = "play"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_next_figure(self):
        self.next_figure = Figure(3, 0)

    def new_figure(self):
        self.figure = self.next_figure
        self.next_figure = None

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
                bell_sound.play()
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        self.new_next_figure()
        if self.intersects():
            self.state = "Gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def new_state(self, sound, music):
        pygame.mixer.music.stop()
        sound.play()
        time.sleep(2)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)


def start(game):
    done = False
    counter = 0
    win_count = 0
    pressing_down = False
    game.new_next_figure()

    pygame.mixer.music.load(musics[game.level - 1])
    pygame.mixer.music.play(-1)

    while not done:
        if game.figure is None:
            game.new_figure()
            game.new_next_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (11 - game.level) == 0 or pressing_down:
            if game.state == "play":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if game.state == "play":
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY,
                                 [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 2])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        if game.next_figure is not None:
            for i in range(4):
                for j in range(4):
                    pygame.draw.rect(screen, GRAY,
                                     [445 + game.zoom * j, 100 + game.zoom * i, game.zoom, game.zoom], 1)
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, colors[game.next_figure.color],
                                         [352 + game.zoom * (j + game.next_figure.x) + 1,
                                          100 + game.zoom * (i + game.next_figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 35, True, False)
        font1 = pygame.font.SysFont('Calibri', 90, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text2 = font.render("Level: " + str(game.level), True, BLACK)
        text_game_over = font1.render("Game Over", True, BLACK)
        text_congratulation = font1.render("Congratulation!", True, (255, 100, 180))
        text_next_figure = font.render("Next Figure:", True, BLACK)

        screen.blit(text_next_figure, [400, 70])
        screen.blit(text, [0, 30])
        screen.blit(text2, [0, 5])

        if game.state == "Gameover":
            screen.fill(WHITE)
            screen.blit(master, (0, 0))
            screen.blit(text_game_over, [110, 600])

        if game.state == "Complete":
            screen.blit(text_congratulation, [5, 250])

        if game.score >= game.level * 2:
            game.state = "Complete"
            if win_count == 0:
                game.new_state(win_sound, musics[2])
                win_count += 1

        pygame.display.flip()
        clock.tick(fps)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (600, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

master = pygame.image.load("dung.jpg")

musics = [
    "Flamingo.mp3",
    "FACE_LABIRINT.mp3",
    "Pobednaya.mp3"
]

bell_sound = pygame.mixer.Sound("bell-sound.mp3")
win_sound = pygame.mixer.Sound("kidcheer.mp3")
sad_sound = pygame.mixer.Sound("Грустный тромбон.mp3")

clock = pygame.time.Clock()
fps = 30

level1 = Tetris(20, 10, 1)
level2 = Tetris(20, 10, 2)
level3 = Tetris(20, 10, 3)

start(level1)

play = False
while not play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DELETE:
                play = True

        pygame.display.update()
