import game_framework
import pico2d
import os;

#import main_state as start_state
import world_build_state as start_state

PIXEL_PER_METER = 100 / 3;

os.chdir("Lecture16_Game_Data_Management");
pico2d.open_canvas(int(40 * PIXEL_PER_METER), int(30 * PIXEL_PER_METER))
game_framework.run(start_state)
pico2d.close_canvas()