import game_framework
from pico2d import *

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



# Boy Event
RIGHTKEY_DOWN, LEFTKEY_DOWN, UPKEY_DOWN, DOWNKEY_DOWN, RIGHTKEY_UP, LEFTKEY_UP, UPKEY_UP, DOWNKEY_UP, SPACE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFTKEY_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UPKEY_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWNKEY_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHTKEY_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFTKEY_UP,
    (SDL_KEYUP, SDLK_UP): UPKEY_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWNKEY_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Boy States

class WalkingState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHTKEY_DOWN:
            boy.x_velocity += RUN_SPEED_PPS
        elif event == RIGHTKEY_UP:
            boy.x_velocity -= RUN_SPEED_PPS
        if event == LEFTKEY_DOWN:
            boy.x_velocity -= RUN_SPEED_PPS
        elif event == LEFTKEY_UP:
            boy.x_velocity += RUN_SPEED_PPS

        if event == UPKEY_DOWN:
            boy.y_velocity += RUN_SPEED_PPS
        elif event == UPKEY_UP:
            boy.y_velocity -= RUN_SPEED_PPS
        if event == DOWNKEY_DOWN:
            boy.y_velocity -= RUN_SPEED_PPS
        elif event == DOWNKEY_UP:
            boy.y_velocity += RUN_SPEED_PPS



    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        boy.x += boy.x_velocity * game_framework.frame_time
        boy.y += boy.y_velocity * game_framework.frame_time

        boy.x = clamp(0, boy.x, boy.bg.w );
        boy.y = clamp(0, boy.y, boy.bg.h );

    @staticmethod
    def draw(boy):
        cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom;
        if boy.x_velocity > 0:
            boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, cx, cy)
            boy.dir = 1
        elif boy.x_velocity < 0:
            boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, cx, cy)
            boy.dir = -1
        else:
            # if boy x_velocity == 0
            if boy.y_velocity > 0 or boy.y_velocity < 0:
                if boy.dir == 1:
                    boy.image.clip_draw(int(boy.frame) * 100, 100, 100, 100, cx, cy)
                else:
                    boy.image.clip_draw(int(boy.frame) * 100, 0, 100, 100, cx, cy)
            else:
                # boy is idle
                if boy.dir == 1:
                    boy.image.clip_draw(int(boy.frame) * 100, 300, 100, 100, cx, cy)
                else:
                    boy.image.clip_draw(int(boy.frame) * 100, 200, 100, 100, cx, cy)


next_state_table = {
    WalkingState: {RIGHTKEY_UP: WalkingState, LEFTKEY_UP: WalkingState, RIGHTKEY_DOWN: WalkingState, LEFTKEY_DOWN: WalkingState,
                UPKEY_UP: WalkingState, UPKEY_DOWN: WalkingState, DOWNKEY_UP: WalkingState, DOWNKEY_DOWN: WalkingState,
                SPACE: WalkingState}
}


class Boy:

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('animation_sheet.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.x_velocity, self.y_velocity = 0, 0
        self.frame = 0
        self.event_que = []
        self.cur_state = WalkingState
        self.cur_state.enter(self, None)

        self.eaten_ball_counter = 0;

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def eat_ball(self):
        self.eaten_ball_counter += 1;

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

        x  =  clamp( 0, self.x - self.bg.window_left - 60, self.canvas_width - 60);
        y  =  clamp( 0, self.y - self.bg.window_bottom + 50, self.canvas_height + 50);

        self.font.draw(x, y, "ball counter : {0}".format(self.eaten_ball_counter), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

