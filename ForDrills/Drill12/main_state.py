import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from ball import *;
from ground import Ground
from zombie import Zombie


name = "MainState"

boy = None
balls = [];
big_balls = [];
zombie = None


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

def get_balls():
    return balls;

def get_big_balls():
    return big_balls;

def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global zombie
    zombie = Zombie()
    game_world.add_object(zombie, 1)

    global balls;
    balls = [Ball() for i in range(5)];
    game_world.add_objects(balls, 1)

    global big_balls;
    big_balls = [BigBall() for i in range(5)];
    game_world.add_objects(big_balls, 1)

    ground = Ground()
    game_world.add_object(ground, 0)

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
    global big_balls,balls, boy, zombie;

    for game_object in game_world.all_objects():
        game_object.update()

    #for ball in balls:
    #    if boy:
    #        if collide(boy, ball):
    #            boy.increase_hp(ball.hp);
    #            balls.remove(ball);
    #            game_world.remove_object(ball);

    #for big_ball in big_balls:
    #    if boy:
    #        if collide(boy, big_ball):
    #            boy.increase_hp(big_ball.hp);
    #            big_balls.remove(big_ball);
    #            game_world.remove_object(big_ball);
    
    for ball in balls:
        if zombie:
            if collide(zombie, ball):
                zombie.increase_hp(ball.hp);
                balls.remove(ball);
                game_world.remove_object(ball);

    for big_ball in big_balls:
        if zombie:
            if collide(zombie, big_ball):
                zombie.increase_hp(big_ball.hp);
                big_balls.remove(big_ball);
                game_world.remove_object(big_ball);

    if zombie and boy:
        if collide(boy, zombie):
            if 0 <len( balls )or  0 <len( big_balls): #공을 다먹었으면 보이가 죽고 아니면 좁비가 죽음.
                game_world.remove_object(zombie);
            else:
                game_world.remove_object(boy);
    
    
                
            


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






