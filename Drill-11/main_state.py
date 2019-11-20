import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from terrain import Terrain
from grass import Grass
from ball import Ball, BigBall

name = "MainState"

boy = None
terrain = None
grass = None
balls = []
big_balls = []


def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb();
    left_b, bottom_b, right_b, top_b = b.get_bb();

    if left_a > right_b : return False;
    if right_a < left_b : return False;
    if top_a < bottom_b : return False;
    if bottom_a > top_b : return False;
    
    return True;




def enter():
    global boy
    boy = Boy()
    game_world.add_object(boy, 1)

    global grass
    grass = Grass()
    game_world.add_object(grass, 0)

    # fill here for balls
    global balls;
    balls = [Ball() for i in range(10)] + [BigBall() for i in range(10)];
    game_world.add_objects(balls, 1);

    global terrain;
    terrain = Terrain();
    game_world.add_object(terrain, 1);






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
    for ball in balls:
    
        if collide(terrain, ball):
            ball.stop();
            ball.set_x(int(terrain.dir * terrain.velocity));
            
        else:
            ball.start();

        if collide(grass, ball):
            ball.stop();
    
        if collide(boy, ball):
            balls.remove(ball);
            game_world.remove_object(ball);
            
    if boy :

        if collide(terrain, boy):
            boy.is_ground = True;
            boy.x += int(terrain.dir * terrain.velocity);
        elif collide(grass, boy):
            boy.is_ground = True;
            #boy.x += int(terrain.dir * terrain.velocity);
        else :
            boy.is_ground = False;
            




    #delay(0.9)

    # fill here for collision check



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()





