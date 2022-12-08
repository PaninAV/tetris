import random
import pygame

pygame.init()

music_for_levels = [
    "music_for_levels/Flamingo.mp3",
    "music_for_levels/poney.mp3",
    "music_for_levels/halloween_chikl.mp3",
    "music_for_levels/megalomania.mp3",
    "music_for_levels/Cut_My_Hair.mp3",
    "music_for_levels/Pobednaya.mp3",
]

music_for_menu = [
    "music_for_menu/Temmie_Village.mp3",
    "music_for_menu/Metal_Crusher.mp3",
    "music_for_menu/Tem_shop.mp3",
    "music_for_menu/Alphys.mp3",
    "music_for_menu/Another_Medium.mp3",
]

bell_sound = pygame.mixer.Sound("sounds/bell-sound.mp3")
win_sound = pygame.mixer.Sound("sounds/kidcheer.mp3")
lose_sound = pygame.mixer.Sound("sounds/Грустный тромбон.mp3")
sad_sound = pygame.mixer.Sound("sounds/aaaaaa.mp3")
new_sound = pygame.mixer.Sound("sounds/new_game.mp3")
music_slovar = {3: "Alphys", 0: "Temmie_Village", 1: "Metal_Crasher", 2: "Tem_shop", 4: "Another_Medium"}


def play_music(song):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()


def random_music_for_menu():
    music_number = random.randint(0, len(music_for_menu)-1)
    play_music(music_for_menu[music_number])
    return music_number


def new_sound_volume(sound):
    bell_sound.set_volume(sound)
    lose_sound.set_volume(sound)
    sad_sound.set_volume(sound)
    win_sound.set_volume(sound)
    new_sound.set_volume(sound)


def decrease_volume(volume):
    if volume >= 0.1:
        return volume - 0.1
    else:
        return volume


def increase_volume(volume):
    if volume <= 0.9:
        return volume + 0.1
    else:
        return volume
