from pico2d import *

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP,  LEFT_SHIFT_DOWN , LEFT_SHIFT_UP, SLEEP_TIMER, RUN_TIMER = range(8);

# fill here
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): LEFT_SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT) : LEFT_SHIFT_UP
}





# Boy States

class IdleState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.timer = 1000

    @staticmethod
    def exit(boy, event):
        pass;

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8;
        boy.timer -= 1;
        if boy.timer == 0:
            boy.add_event(SLEEP_TIMER);

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 200, 100, 100, boy.x, boy.y)


class RunState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.dir = boy.velocity;

    @staticmethod
    def exit(boy, event):
        pass;

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        boy.x += boy.velocity;
        boy.x = clamp(25, boy.x, 800 -25 );

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)


class DashState:
    @staticmethod
    def enter(boy, event):
        print("dash_enter");
        if event == RIGHT_DOWN:
            boy.velocity += 1;
        elif event == LEFT_DOWN:
            boy.velocity -= 1;
        elif event == RIGHT_UP:
            boy.velocity -= 1;
        elif event == LEFT_UP:
            boy.velocity += 1;

        boy.dir = boy.velocity;
        boy.velocity *= 2;
        boy.timer = 100;


    @staticmethod
    def exit(boy, event):
        print("dash_eixt");
        boy.velocity /= 2;

        pass;

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1;
        boy.x += boy.velocity;
        boy.x = clamp(25, boy.x, 800 -25 );
        if boy.timer == 0:
            print("대시 지속시간 끝.");
            boy.add_event(RUN_TIMER);

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)


class SleepState:

    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass;

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8;
    
    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
            3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
            -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)


#폴링이니깐 값을 계속 받아 옴.
next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
    LEFT_SHIFT_DOWN : IdleState, LEFT_SHIFT_UP : IdleState,
    SLEEP_TIMER: SleepState},
    
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
    LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
    LEFT_SHIFT_DOWN : DashState, LEFT_SHIFT_UP : RunState
    },
 
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
    LEFT_UP: RunState, RIGHT_UP: RunState,
    LEFT_SHIFT_DOWN : SleepState, LEFT_SHIFT_UP : SleepState
    },

    DashState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
    LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
    LEFT_SHIFT_DOWN : DashState, LEFT_SHIFT_UP : RunState,
    RUN_TIMER : RunState
    },
}






class Boy:
    dash_state = False;
    def __init__(self):
        self.x, self.y = 800 // 2, 90
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0;
        self.timer = 0;
        self.event_que = [];
        self.cur_state = IdleState;
        self.cur_state.enter(self, None);

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event];
            self.cur_state.enter(self, event);

    def change_state(self,  state):
        # fill here
        pass


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

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)] # 테이블에서 값을 받아와 queue에 추가.
            self.add_event(key_event)

