import pygame
import random
import music
import environment
import saves

pygame.init()


def text_objects(text, font_edit):
    text_surface = font_edit.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()


class Button:

    def __init__(self, message, x, y, width, height, inactive_color, active_color):
        self.message = message
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def print_text(self):
        text_surf, text_rect = text_objects(self.message, environment.menu_font)
        text_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        screen.blit(text_surf, text_rect)

    def show_button(self):
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
            if click[0] == 1:
                self.print_text()
                return True
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))
        self.print_text()
        return False


class GameButton(Button):

    def __init__(self,  message, x, y, width, height, inactive_color, active_color, level):
        super().__init__(message, x, y, width, height, inactive_color, active_color)
        self.level = level

    def set_button_color(self, level_status):
        if level_status is False:
            self.active_color = environment.red
        else:
            self.active_color = environment.green


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
        self.color = random.randint(1, len(environment.colors) - 1)
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
    height = 0
    width = 0
    x = 60
    y = 60
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
                music.bell_sound.play()
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


def start(game):
    music.play_music(music.music_for_levels[game.level - 1])
    done = False
    pause = False
    pressing_down = False
    game_goes = True
    counter = 0

    text_level = environment.font3.render("Level: " + str(game.level), True, environment.BLACK)
    text_lives = environment.font3.render("Lives: " + str(menu.lives), True, environment.BLACK)
    text_open = environment.font2.render("You open " + str(game.level + 1) + " level!", True, (75, 0, 130))

    while not done:
        if pygame.mixer.music.get_busy() is False and game.state == "play":
            music.play_music(music.music_for_levels[game.level - 1])
        if game.figure is None:
            game.new_figure()
            game.new_next_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (11 - (menu.difficulty + 1) - game.level) == 0 or pressing_down:
            if game.state == "play":
                game.go_down()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    if pause is False:
                        game.state = "pause"
                        pause = True
                    else:
                        game.state = "play"
                        pause = False
                if game.state == "play":
                    if e.key == pygame.K_UP:
                        game.rotate()
                    if e.key == pygame.K_DOWN:
                        pressing_down = True
                    if e.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if e.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if e.key == pygame.K_SPACE:
                        game.go_space()
                if e.key == pygame.K_RETURN:
                    if game.state == "Gameover":
                        menu.lives -= 1
                    done = True
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(environment.WHITE)
        if game.state == "play" or game.state == "pause":
            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, environment.GRAY,
                                     [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, environment.colors[game.field[i][j]],
                                         [game.x + game.zoom * j + 1,
                                          game.y + game.zoom * i + 1,
                                          game.zoom - 2, game.zoom - 2])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(screen, environment.colors[game.figure.color],
                                             [game.x + game.zoom * (j + game.figure.x) + 1,
                                              game.y + game.zoom * (i + game.figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])

            if game.next_figure is not None:
                for i in range(4):
                    for j in range(4):
                        pygame.draw.rect(screen, environment.GRAY,
                                         [445 + game.zoom * j, 100 + game.zoom * i, game.zoom, game.zoom], 1)
                        p = i * 4 + j
                        if p in game.next_figure.image():
                            pygame.draw.rect(screen, environment.colors[game.next_figure.color],
                                             [352 + game.zoom * (j + game.next_figure.x) + 1,
                                              100 + game.zoom * (i + game.next_figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])

            text_score = environment.font3.render("Score: " + str(game.score), True, environment.BLACK)
            screen.blit(environment.text_next_figure, [400, 70])
            screen.blit(text_score, [0, 30])
            screen.blit(text_level, [0, 5])
            screen.blit(text_lives, [130, 5])

        if game.state == "Gameover":
            screen.fill(environment.WHITE)
            screen.blit(environment.text_game_over, [110, 595])
            screen.blit(environment.text_continue, (150, 670))
            if game_goes is True:
                game_goes = False
                pygame.mixer.music.stop()
                if menu.lives == 1:
                    music.lose_sound.play()
                else:
                    music.sad_sound.play()
            if menu.lives > 1:
                screen.blit(environment.pepe, (0, 0))
            else:
                screen.blit(environment.master, (0, 0))

        if game.score >= game.level * 5 * (menu.difficulty + 1):
            screen.blit(environment.text_congratulation, (15, 300))
            screen.blit(environment.text_continue, (125, 600))
            if game.level == 5:
                screen.blit(environment.font2.render("Game Complete!", True, (255, 100, 180)), (75, 500))
            else:
                screen.blit(text_open, (100, 400))
            if game.state == "play":
                music.win_sound.play()
                music.play_music(music.music_for_levels[5])
                game.state = "Complete"

        if game.state == "pause":
            screen.blit(environment.menu_font.render("PAUSE", True, environment.BLACK), [200, 150])

        pygame.display.flip()
        clock.tick(fps)
    music.random_music_for_menu()
    return game.state


size = (600, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
fps = 30


def set_true(button_level):
    if start(Tetris(20, 10, button_level)) == "Complete":
        if button_level < 5:
            saves.set_new_save(menu.difficulty, button_level - 1)
            menu.set_accepts()
            print(menu.accepts)


def start_level(button_level):
    if button_level != 1:
        if menu.accepts[menu.difficulty][button_level - 2] is True:
            set_true(button_level)
    else:
            set_true(button_level)


def show_play_menu():
    if first_level_button.show_button() is True:
        start_level(1)
    second_level_button.set_button_color(menu.accepts[menu.difficulty][0])
    if second_level_button.show_button() is True:
        start_level(2)
    third_level_button.set_button_color(menu.accepts[menu.difficulty][1])
    if third_level_button.show_button() is True:
        start_level(3)
    forth_level_button.set_button_color(menu.accepts[menu.difficulty][2])
    if forth_level_button.show_button() is True:
        start_level(4)
    fifth_level_button.set_button_color(menu.accepts[menu.difficulty][3])
    if fifth_level_button.show_button() is True:
        start_level(5)
    if back_button.show_button() is True:
        menu.set_main_menu()


def show_menu():
    if start_button.show_button() is True:
        menu.set_play_menu()
    if options_button.show_button() is True:
        menu.set_settings()
    if exit_button.show_button() is True:
        quit_game()


def show_settings():
    music_volume_text = environment.menu_font.render("Volume: " + str(int(round(menu.music_volume * 10, 0))), True,
                                                     environment.BLACK)
    sounds_volume_text = environment.menu_font.render("Volume: " + str(int(round(menu.sound_volume * 10, 0))), True,
                                                      environment.BLACK)
    screen.blit(music_volume_text, [175, 150])
    screen.blit(sounds_volume_text, [175, 250])
    screen.blit(environment.text_sound, [200, 205])
    screen.blit(environment.text_music, [210, 105])
    if increase_sound_button.show_button() is True:
        menu.increase_sound_volume()
    if decrease_sound_button.show_button() is True:
        menu.decrease_sound_volume()
    if increase_music_button.show_button() is True:
        menu.increase_music_volume()
    if decrease_music_button.show_button() is True:
        menu.decrease_music_volume()
    if increase_difficult_button.show_button() is True:
        menu.increase_difficult()
    if decrease_difficult_button.show_button() is True:
        menu.decrease_difficult()
    difficult_text = environment.menu_font.render("Difficulty: " + find_difficult(), True, environment.BLACK)
    screen.blit(difficult_text, (135, 350))
    if new_game_button.show_button() is True:
        saves.set_zero_saves()
    if back_button.show_button() is True:
        menu.set_main_menu()


difficult_slovar = {0: 'Easy', 1: 'Norm', 2: 'Hard', 3: 'HELL'}


def find_difficult():
    return difficult_slovar.get(menu.difficulty)


class Menu:

    state = "main"
    lives = 3
    difficulty = 0
    music_volume = 0.5
    sound_volume = 0.5
    accepts = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
    ]

    def __init__(self, state, diffuculty, lives, music_volume, sound_volume):
        self.state = state
        self.difficulty = diffuculty
        self.lives = lives
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.set_accepts()

    def set_settings(self):
        self.state = "settings"

    def set_play_menu(self):
        self.state = "play menu"

    def set_main_menu(self):
        self.state = "main"

    def increase_difficult(self):
        if self.difficulty <= 2:
            self.difficulty += 1

    def decrease_difficult(self):
        if self.difficulty >= 1:
            self.difficulty -= 1

    def increase_music_volume(self):
        self.music_volume = music.increase_volume(self.music_volume)
        pygame.mixer.music.set_volume(self.music_volume)

    def decrease_music_volume(self):
        self.music_volume = music.decrease_volume(self.music_volume)
        pygame.mixer.music.set_volume(self.music_volume)

    def increase_sound_volume(self):
        self.sound_volume = music.increase_volume(self.sound_volume)
        music.new_sound_volume(self.sound_volume)

    def decrease_sound_volume(self):
        self.sound_volume = music.decrease_volume(self.sound_volume)
        music.new_sound_volume(self.sound_volume)

    def set_accepts(self):
        self.accepts = saves.set_saves(self.accepts)


def quit_game():
    pygame.quit()
    quit()


start_button = Button("GO!", 200, 150, 200, 50, environment.BLACK, environment.green)
exit_button = Button("Quit", 200, 350, 200, 50, environment.BLACK, environment.red)
options_button = Button("Options", 200, 250, 200, 50, environment.BLACK, environment.yellow)
increase_music_button = Button("+", 475, 150, 50, 50, environment.BLACK, environment.green)
decrease_music_button = Button("-", 75, 150, 50, 50, environment.BLACK, environment.red)
increase_sound_button = Button("+", 475, 250, 50, 50, environment.BLACK, environment.green)
decrease_sound_button = Button("-", 75, 250, 50, 50, environment.BLACK, environment.red)
increase_difficult_button = Button("+", 475, 350, 50, 50, environment.BLACK, environment.green)
decrease_difficult_button = Button("-", 75, 350, 50, 50, environment.BLACK, environment.red)
back_button = Button("Back", 200, 550, 200, 50, environment.BLACK, environment.red)
first_level_button = GameButton("Level 1", 200, 25, 200, 50, environment.BLACK, environment.green, 1)
second_level_button = GameButton("Level 2", 200, 125, 200, 50, environment.BLACK, environment.green, 2)
third_level_button = GameButton("Level 3", 200, 225, 200, 50, environment.BLACK, environment.green, 3)
forth_level_button = GameButton("Level 4", 200, 324, 200, 50, environment.BLACK, environment.green, 4)
fifth_level_button = GameButton("Level 5", 200, 425, 200, 50, environment.BLACK, environment.green, 5)
new_game_button = Button("New game", 175, 450, 250, 55, environment.BLACK, environment.yellow)

menu = Menu("main", 0, 3, 0.5, 0.5)
pygame.mixer.music.set_volume(menu.music_volume)
play = False

number_of_music_menu = music.random_music_for_menu()

while not play:

    screen.fill((52, 78, 91))
    if pygame.mixer.music.get_busy() is False:
        number_of_music_menu = music.random_music_for_menu()
    screen.blit(environment.text_play, [20, 600])
    screen.blit(environment.menu_font.render(str(music.music_slovar.get(number_of_music_menu)),
                                             True, environment.BLACK), [20, 635])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = True
        if menu.lives == 0:
            saves.set_zero_saves()
            menu.accepts = saves.set_saves(menu.accepts)
            menu.lives = 3
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if menu.state == "main":
            show_menu()
        elif menu.state == "settings":
            show_settings()
            menu.accepts = saves.set_saves(menu.accepts)
        else:
            show_play_menu()
        pygame.display.update()
