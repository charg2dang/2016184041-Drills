import random
import json
import pickle
import os

from pico2d import *
import game_framework
import game_world

import world_build_state
import ranking_state;

name = "MainState"
# game

def collide(a, b) -> bool:
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

boy = None

def enter():
    global boy
    boy = world_build_state.get_boy()
    pass

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
            #game_framework.change_state(world_build_state)
            game_framework.change_state(ranking_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_world.save()
        else:
            boy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    from boy import Boy;
    my_boy = Boy.my_boy;

    for game_object in game_world.all_objects():
        if not isinstance(game_object, Boy) :
            if collide(game_object, my_boy) :
                game_framework.change_state(ranking_state);





def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






