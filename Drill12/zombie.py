import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state
from const import *;

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10


animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        positions = [(43, 750),(1118, 750),(1050, 530),(575, 220),(235, 33), (575,220),(1050, 530), (1118,750)] 
        self.patrol_positions = []
        self.load_images()
        self.patrol_order = 1;
        for p in positions: 
            self.patrol_positions.append((p[0], 1024-p[1])) # convert for origin at bottom, left
        self.target_x, self.target_y = None, None;
        self.font = load_font('ENCR10B.TTF', 16)
        self.x, self.y = random.randint(0, Const.WIN_WIDTH), random.randint(0, Const.WIN_HEIGHT);

        self.load_images();
        self.dir = random.random()*2*math.pi # random moving direction
        self.speed = 0
        self.timer = 1.0 # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()
        self.current_hp = 100;

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def wander(self):
        self.speed = RUN_SPEED_PPS;
        self.calculate_current_position();
        self.timer -= game_framework.frame_time;
        if self.timer < 0:
            self.timer +=1.0;
            self.dir = random.random() * 2 * math.pi;

        return BehaviorTree.SUCCESS;

    def find_player(self):
        boy = main_state.get_boy();
        #distance = (boy.x - self.x ) ** 2 + ( boy.y - self.y ) ** 2;
        #if distance < ( PIXEL_PER_METER * 8 ) ** 2:
        self.dir = math.atan2(boy.y - self.y, boy.x - self.x);
        return BehaviorTree.SUCCESS;
        #else:
            #self.speed = 0;
            #return BehaviorTree.FAIL;
        #pass

    def find_ball(self):
        balls = main_state.get_balls();

        if not balls:
            self.speed = 0;
            return BehaviorTree.FAIL;

        for ball in balls:
            #distance = (ball.x - self.x ) ** 2 + ( ball.y - self.y ) ** 2;
            #if distance < ( PIXEL_PER_METER * 5 ) ** 2:
            self.dir = math.atan2(ball.y - self.y, ball.x - self.x); #있으면 가고 아니면 말고
            return BehaviorTree.SUCCESS;

        ##없으면 업는대로 ㅇㅇ
        #self.speed = 0;
        #return BehaviorTree.FAIL;

    def find_big_ball(self):
        balls = main_state.get_big_balls();
        
        if not balls:
            self.speed = 0;
            return BehaviorTree.FAIL;

        for ball in balls:
            distance = (ball.x - self.x ) ** 2 + ( ball.y - self.y ) ** 2;
            #if distance < ( PIXEL_PER_METER * 5 ) ** 2:
            self.dir = math.atan2(ball.y - self.y, ball.x - self.x); #있으면 가고 아니면 말고
            return BehaviorTree.SUCCESS;


    def move_to_player(self):
        # fill here
        self.speed = RUN_SPEED_PPS;
        self.calculate_current_position();
        
        return BehaviorTree.SUCCESS;

    def move_to_ball(self):
        self.speed = RUN_SPEED_PPS;
        self.calculate_current_position();
        return BehaviorTree.SUCCESS;

    def move_to_big_ball(self):
        self.speed = RUN_SPEED_PPS;
        self.calculate_current_position();
        return BehaviorTree.SUCCESS;

    # 다음 xy에 볼이 있으면 다른방향으.
    def bypass_ball(self):
        self.speed = RUN_SPEED_PPS;
        self.calculate_current_position();
        
        balls = main_state.get_balls();
        while(True) :
            for ball in balls:
                if main_state.collide(self, ball):
                    #부딪힌다면 다른 방향으로 살작 이동 난수로
                    self.dir = -self.dir;
                    self.calculate_current_position();
                    #원래자리로 돌아와서 
                    print("dsd");
                    self.dir = random.random()*2*math.pi;
                    # 랜덤 방향으로 우회.
                    self.calculate_current_position();

                    return BehaviorTree.SUCCESS;
            
            print("ㅋㅋbypass_ball");
            return BehaviorTree.FAIL;

        

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)] 
        self.patrol_order += 1;
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x) 
        return BehaviorTree.SUCCESS


    def move_to_target(self):
        self.speed = RUN_SPEED_PPS 
        self.calculate_current_position();

        distance = (self.target_x - self.x)**2 + (self.target_y - self.y)**2

        if distance < PIXEL_PER_METER**2: 
            return BehaviorTree.SUCCESS 
        else: 
            return BehaviorTree.RUNNING


    
    def build_behavior_tree(self):
        chase_big_ball_node = SequenceNode("Chase Big Ball");
        find_big_ball_node = LeafNode("Find Big Ball", self.find_big_ball);
        
        move_to_big_ball_node = SelectorNode("Move to Big Ball");
        go_to_big_ball_node = LeafNode("Move to Big Ball", self.move_to_big_ball);
        bypass_ball_node = LeafNode("Bypass Ball", self.bypass_ball);
        move_to_big_ball_node.add_children(bypass_ball_node, go_to_big_ball_node);

        chase_big_ball_node.add_children(find_big_ball_node, move_to_big_ball_node);

        
        chase_ball_node = SequenceNode("Chase Ball");
        find_ball_node = LeafNode("Find Ball", self.find_ball);
        move_to_ball_node = LeafNode("Move to Ball", self.move_to_ball);
        chase_ball_node.add_children(find_ball_node, move_to_ball_node);


        chase_player_node = SequenceNode("Chase Player");
        find_player_node = LeafNode("Find Player", self.find_player);#수정 필요. 무조건 성공 요함. 거리 상관 x
        move_to_player_node = LeafNode("Move to Player", self.move_to_player);
        chase_player_node.add_children(find_player_node, move_to_player_node);

        wander_chase_node = SelectorNode("WanderChase");
        wander_chase_node.add_children(chase_big_ball_node, chase_ball_node, chase_player_node);

        self.bt = BehaviorTree(wander_chase_node)
        pass


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        # fill here
        self.bt.run();
        pass


    def draw(self):
        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)

        self.font.draw(self.x - 30, self.y + 50, "HP : {0}".format(self.current_hp), (255, 255, 0));


    def handle_event(self, event):
        pass

    def increase_hp(self, hp):
        self.current_hp += hp;

