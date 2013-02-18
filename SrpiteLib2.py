import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *
from Global_Constants import *

__metaclass__ = type # 

# each type of game object gets an init and an
# update function. the update function is called
# once per cur_frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard


def load_image(file, scale = 1):
    file = os.path.join(ART_DIR, file)

    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s' % (file, pygame.get_error())
    if scale > 1:
        surface = pygame.transform.scale(surface, (surface.get_width()*scale, surface.get_height()*scale))
    return surface.convert_alpha()

def load_images(file_list, scale = 1):
    image_list = []
    for file in file_list:
        img = load_image(file, scale)
        image_list.append(img)
    return image_list


class Player(pygame.sprite.Sprite):

    scale = PLAYER_SCALE
    speed = PLAYER_SPEED
    #half_width = 0
    image_list = []

    @staticmethod
    def loadImage(file_name):
        img = load_image(file_name, Player.scale)
        Player.image_list.append(img)
        #Player.half_width = img.get_width() / 2


    def __init__(self,):
        super(Player, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(midbottom = SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top


    def move(self, direction):
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)


    def gunpos(self):
        #pos = self.half_width + self.rect.left # +self.rect.centerx
        pos = self.rect.centerx
        return pos, self.rect.top


class InvaderC(pygame.sprite.Sprite):
    speed = INVADER_SPEED
    animcycle = INVADER_ANIM_CYCLE
    image_list = []
    scale = INVADER_SCALE
    image_list = []
    file_list = ['invader_c_0.png', 'invader_c_1.png' ]

    @staticmethod
    def loadImages():
        InvaderC.image_list = load_images(InvaderC.file_list, InvaderC.scale)

    def __init__(self):
        super(InvaderC, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * InvaderC.speed
        self.cur_frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.cur_frame = self.cur_frame + 1
        self.image = self.image_list[self.cur_frame / self.animcycle % INVADER_NUM_FRAMES]


class InvaderB(pygame.sprite.Sprite):
    speed = INVADER_SPEED
    animcycle = INVADER_SPEED
    image_list = []
    scale = INVADER_SCALE
    image_list = []
    file_list = ['invader_b_0.png', 'invader_b_1.png' ]

    @staticmethod
    def loadImages():
        InvaderB.image_list = load_images(InvaderB.file_list, InvaderB.scale)

    def __init__(self):
        super(InvaderB, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * InvaderB.speed
        self.cur_frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.cur_frame = self.cur_frame + 1
        self.image = self.image_list[self.cur_frame / self.animcycle % INVADER_NUM_FRAMES]


class InvaderA(pygame.sprite.Sprite):
    speed = INVADER_SPEED
    animcycle = INVADER_SPEED
    image_list = []
    scale = INVADER_SCALE
    image_list = []
    file_list = ['invader_a_0.png', 'invader_a_1.png' ]

    @staticmethod
    def loadImages():
        InvaderA.image_list = load_images(InvaderA.file_list, InvaderA.scale)

    def __init__(self):
        super(InvaderA, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * InvaderA.speed
        self.cur_frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.cur_frame = self.cur_frame + 1
        self.image = self.image_list[self.cur_frame / self.animcycle % INVADER_NUM_FRAMES]


class Explosion(pygame.sprite.Sprite):
    defaultlife = EXPLOSION_DEFAULT_LIFE
    animcycle = EXPLOSION_ANIM_CYCLE
    image_list = []
    scale = 1

    @staticmethod
    def loadImage(file_name):
        Explosion.image_list.append(load_image(file_name, Explosion.scale))
        Explosion.image_list.append(pygame.transform.flip(Explosion.image_list[0], 1, 1))

    def __init__(self, actor):
        super(Explosion, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center = actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        self.image = self.image_list[self.life / self.animcycle % EXPLOSION_ANIM_FRAMES]
        if self.life <= 0: self.kill()


class LaserShot(pygame.sprite.Sprite):
    speed = LASER_SHOT_SPEED
    image_list = []
    scale = 1

    @staticmethod
    def loadImage(file_name):
        LaserShot.image_list.append(load_image(file_name, LaserShot.scale))

    def __init__(self, pos):
        super(LaserShot, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class InvaderBomb(pygame.sprite.Sprite):
    speed = 9
    image_list = []
    scale = 1

    @staticmethod
    def loadImage(file_name):
        InvaderBomb.image_list.append(load_image(file_name, InvaderBomb.scale))

    def __init__(self, alien):
        super(InvaderBomb, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(midbottom =
                    alien.rect.move(0, 5).midbottom)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 470:
            Explosion(self)
            self.kill()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.score = 0
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def addToScore(self, score_inc):
        self.score += score_inc

    def update(self):
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score: %d" % self.score
            self.image = self.font.render(msg, 0, self.color)

