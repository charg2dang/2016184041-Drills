import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from background import FixedBackground as Background;
#from background import InfiniteBackground as Background;

name = "MainState"

boy = None
background = None


def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True



def get_boy():
    return boy


def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global background
    background = Background()
    game_world.add_object(background, 0)

    background.set_center_object(boy);
    boy.set_background(background);

def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






