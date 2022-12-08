import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 215, 0)

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

font1 = pygame.font.SysFont('Calibri', 90)
font2 = pygame.font.SysFont("Calibri", 60)
font3 = pygame.font.SysFont("Calibri", 35)
menu_font = pygame.font.SysFont("arialblack", 40)

text_game_over = font1.render("Game Over", True, BLACK)
text_congratulation = font1.render("Congratulation!", True, (255, 100, 180))
text_next_figure = font3.render("Next Figure:", True, BLACK)
text_continue = font3.render("Press Enter to continue!", True, BLACK)
text_play = menu_font.render("Play:", True, BLACK)
text_music = menu_font.render("MUSIC", True, BLACK)
text_sound = menu_font.render("SOUNDS", True, BLACK)
master = pygame.image.load("images/dung.jpg")
pepe = pygame.image.load("images/pepe.png")
