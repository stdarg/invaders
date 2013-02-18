# import system modules
import random
import os.path
import glob

# import basic pygame modules
import pygame

# import my own modules
import Globals
import SoundUtil


#
# Using the bitmap image, create a mask for collisions
# It uses the color key to clear to clear the mask so
# transparent parts of the image don't collide
#
def maskFromSurface(surface, threshold = 127):

    # get the mask from the image
    mask = pygame.mask.Mask(surface.get_size())

    # get the color for transparency
    key = surface.get_colorkey()

    # if there is a transparent color
    if key:
        # iterate over all the image pixels
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                # if the pixel is not transparent, set the pixel for collision
                if surface.get_at((x + 0.1, y + 0.1)) != key:
                    mask.set_at((x, y), 1)
    else:  # there is no transparent color
        for y in range(surface.get_height()):
            for x in range (surface.get_width()):
                if surface.get_at((x, y))[3] > threshold:
                    mask.set_at((x, y), 1)
    return mask

# each type of game object gets an init and an
# update function. the update function is called
# once per cur_frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about



def load_image(file, scale = 1):
    file = os.path.join(Globals.ART_DIR, file)

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


def load_images_pattern(file_pattern, scale = 1):
    file_pattern = os.path.join(Globals.ART_DIR, file_pattern)
    file_list = glob.glob(file_pattern)

    #print file_pattern

    if not file_list:
        print "No file list from pattern"
        return

    image_list = []
    for file in file_list:
        #print file
        try:
            surface = pygame.image.load(file)
        except pygame.error:
            raise SystemExit, 'Could not load image "%s" %s' % (file, pygame.get_error())

        if scale > 1:
            surface = pygame.transform.scale(surface, (surface.get_width()*scale, surface.get_height()*scale))

        img = surface.convert_alpha()
        image_list.append(img)

        if 0 == len(image_list):
            print "Error no image list"

    #print image_list
    return image_list


class GameData(pygame.sprite.Sprite):
    scale = Globals.PLAYER_SCALE

    @staticmethod
    def loadImages(file_name_list, ObjType):
        ObjType.file_name_list = file_name_list
        ObjType.image_list = load_images(ObjType.file_name_list, ObjType.scale)
        ObjType.num_images = len(ObjType.image_list)

    def sanityCheck(self):
        if len(type(self).image_list) == 0:
            raise SystemExit, 'Game object of type: %s has an empty image list.' % type(self)

        if type(self).num_images == 0:
            raise SystemExit, 'Game object of type: %s has no viewable frames.' % type(self)

        if not self.containers:
            raise SystemExit, "Game object has no container, type; '%s'" % type(self)

    def __init__(self):
        self.sanityCheck()
        super(GameData, self).__init__(self.containers)
        #self.cur_frame = 0



class AnimGameData(GameData):

    def __init__(self, anim_cycle):
        super(AnimGameData, self).__init__()
        self.cur_frame = 0
        self.image = self.image_list[self.cur_frame]
        self.anim_cycle = anim_cycle

    @staticmethod
    def loadImages(file_pattern, ObjType):
        file_pattern = os.path.join(Globals.ART_DIR, file_pattern)
        ObjType.file_name_list = glob.glob(file_pattern)

        #print file_pattern
        if not ObjType.file_name_list:
            raise SystemExit, "No file list from pattern '%s'" % file_pattern
            return

        ObjType.image_list = []
        for file in ObjType.file_name_list:
            #print file
            try:
                surface = pygame.image.load(file)
            except pygame.error:
                raise SystemExit, 'Could not load image "%s" %s' % (file, pygame.get_error())

            if ObjType.scale > 1:
                surface = pygame.transform.scale(surface, (surface.get_width()*ObjType.scale, surface.get_height()*ObjType.scale))

            img = surface.convert_alpha()
            ObjType.image_list.append(img)

            ObjType.num_images = len(ObjType.image_list)
            if 0 == ObjType.num_images:
                raise SystemExit, "Error no image list"
        #print image_list

    def nextAnimImg(self):
        if self.num_images == 0:
            return

        self.cur_frame += 1
        self.image = self.image_list[self.cur_frame / self.anim_cycle % Globals.INVADER_NUM_FRAMES]


class Ufo(GameData):
    speed = Globals.SPEED_UFO
    image_list = []
    num_images = 0
    file_name_list = []
    ufo_overhead = False
    score = Globals.SCORE_UFO
    reload_time = 0

    def __init__(self):
        super(Ufo, self).__init__()
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.width = self.rect.right
        self.rect.move_ip(-self.width, Globals.POS_UFO_Y)
        Ufo.ufo_overhead = True
        Ufo.alert_sound.play(Globals.SOUND_LOOP_FOREVER, 0, Globals.SOUND_UFO_FADEOUT_MS)

    def takeHit(self):
        UfoExplosion(self)
        self.kill()
        self.rect.move_ip(-20, -20)
        Ufo.alert_sound.stop()


    def update(self):
        self.rect.move_ip(Ufo.speed, 0)

        if self.rect[0] > Globals.SCREEN_WIDTH:
            Ufo.ufo_overhead = False
            Ufo.alert_sound.fadeout(Globals.SOUND_UFO_FADEOUT_MS)
            self.kill()
        else:
            Ufo.ufo_overhead = True


class Player(GameData):
    speed = Globals.SPEED_PLAYER
    image_list = []
    num_images = 0
    file_name_list = []
    explosion_sound = 0
    #lives = 3
    shoot_sound = 0


    @staticmethod
    def static_init(container_list):
        Player.explosion_sound = SoundUtil.load_sound(Globals.PLAYER_EXPLOSION)
        Player.loadImages([ Globals.LASER_BASE_FILE ], Player)
        Player.containers = container_list
        Player.shoot_sound = SoundUtil.load_sound(Globals.PLAYER_SHOT)

    def __init__(self):
        super(Player, self).__init__()
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(midbottom = Globals.SCREENRECT.move(0, -20).midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.lives = 3

    def fire(self):
        LaserShot(self.gunpos())
        Player.shoot_sound.play()

    def move(self, direction):
        self.rect.move_ip(direction * Player.speed, 0)
        self.rect = self.rect.clamp(Globals.SCREENRECT)

    def gunpos(self):
        pos = self.rect.centerx
        return pos, self.rect.top

    def hasAnotherLife(self):
        if self.lives > 0:
            return True
        return False

    def handleDeath(self):
        Ufo.explosion_sound.play()
        PlayerExplosion(self)
        self.lives = self.lives - 1
        self.kill()

class BaseShelter(GameData):
    speed = Globals.SPEED_PLAYER
    image_list = []
    num_images = 0
    file_name_list = []

    def __init__(self, screen_loc):
        super(BaseShelter, self).__init__()
        self.image = self.image_list[0].copy()
        self.mask = maskFromSurface(self.image)
        self.rect = self.image.get_rect(topleft = screen_loc)
        self.screen_loc = screen_loc
        self.hit_count = 0

    def bombHit(self, bomb, reverseY = False):
        loc = pygame.sprite.collide_mask(self, bomb)
        if not loc:
            return

        surfarray = pygame.surfarray.pixels2d(self.image)
        if not len(surfarray):
            return

        self.hit_count += 1

        BombOnShelterExplosion(bomb)
        bomb.kill()

        maxX = self.rect[2] - 1
        maxY = self.rect[3] - 1

        if reverseY:
            inc = -1
            start = loc[1] + 10
            end = loc[1] - 8
        else:
            inc = 1
            start = loc[1] - 8
            end = loc[1] + 8

        for x in range(loc[0] - 8, loc[0] + 8):
            if x < 0 or x > maxX:
                continue
            for y in range(start, end, inc):
                if y < 0 or y > maxY:
                    continue
                surfarray[x][y] = 0

        self.mask = maskFromSurface(self.image)


class BaseInvader(AnimGameData):
    speed = Globals.INVADER_SPEED
    image_list = []
    invader_explosion = 0
    num_bombs = 0

    def __init__(self):
        AnimGameData.__init__(self, Globals.INVADER_ANIM_CYCLE)
        self.rect = self.image.get_rect()
        self.rect.move_ip(0, 50)
        self.facing = random.choice((-1, 1)) * BaseInvader.speed
        if self.facing < 0:
            self.rect.right = Globals.SCREENRECT.right

    @staticmethod
    def static_init():
        BaseInvader.invader_explosion = SoundUtil.load_sound(Globals.INVADER_SHOT)

        InvList = [ InvaderC, InvaderB, InvaderA ]

        for InvType in InvList:
            if 0 == len(InvType.file_list):
                raise SystemExit, "BaseInvader method loadImages failed - no image files lists!"
            InvType.image_list = load_images(InvType.file_list, BaseInvader.scale)
            InvType.num_images = len(InvType.image_list)
            if 0 == InvType.num_images:
                raise SystemExit, "BaseInvader method loadImages failed - no images were loaded!"

    def kill(self):
        BaseInvader.invader_explosion.play()
        super(BaseInvader, self).kill()
        InvaderExplosion(self)


    def dropBomb(self):
        if BaseInvader.num_bombs < 3:
            BaseInvader.num_bombs += 1
            InvaderBomb(self)
            print "Boms away num = %d" % BaseInvader.num_bombs
        else:
            print "Would have dropped a bomb  num = %d" % BaseInvader.num_bombs


    @staticmethod
    def bombExploded():
        BaseInvader.num_bombs -= 1
        print "Bomb exploded num = %d" % BaseInvader.num_bombs


    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not Globals.SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(Globals.SCREENRECT)

        self.nextAnimImg()
        if not int(random.random() * Globals.BOMB_ODDS):
            self.dropBomb()


class InvaderC(BaseInvader):
    image_list = []
    file_list = ['invader_c_0.png', 'invader_c_1.png' ]
    score = Globals.SCORE_INVADER_C

    def __init__(self):
        super(InvaderC, self).__init__()

class InvaderB(BaseInvader):
    image_list = []
    file_list = ['invader_b_0.png', 'invader_b_1.png' ]
    score = Globals.SCORE_INVADER_B

    def __init__(self):
        super(InvaderB, self).__init__()

class InvaderA(BaseInvader):
    image_list = []
    file_list = ['invader_a_0.png', 'invader_a_1.png' ]
    score = Globals.SCORE_INVADER_A

    def __init__(self):
        super(InvaderA, self).__init__()


class BaseExplosion(pygame.sprite.Sprite):
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE * 6
    animcycle = Globals.EXPLOSION_ANIM_CYCLE
    scale = Globals.PLAYER_SCALE

    @staticmethod
    def loadImages():
        InvList = [ InvaderExplosion, PlayerExplosion, BombOnShelterExplosion, BombOnShelterExplosion,
                    BombHitsGroundExplosion, BombInSkyExplosion, BombHitsLaserExplosion, UfoExplosion ]

        for InvType in InvList:
            if 0 == len(InvType.file_list):
                raise SystemExit, "BaseInvader method loadImages failed - no image files lists!"
            InvType.image_list = load_images(InvType.file_list, BaseInvader.scale)
            if 0 == len(InvType.image_list):
                raise SystemExit, "BaseInvader method loadImages failed - no images were loaded!"
            InvType.anim_frames = len(InvType.image_list)
            InvType.containers = Globals.GameData.all

    def __init__(self, actor):
        super(BaseExplosion, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center = actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        self.image = self.image_list[self.life / self.animcycle % self.anim_frames]
        if self.life <= 0:
            self.kill()


class InvaderExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'invader_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_INVADER_LIFE

    def __init__(self, actor):
        super(InvaderExplosion, self).__init__(actor)


class PlayerExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'laser_base_exp_0.png', 'laser_base_exp_1.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_PLAYER

    def __init__(self, actor):
        super(PlayerExplosion, self).__init__(actor)


class BombOnShelterExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'bomb_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_SHELTER

    def __init__(self, actor):
        super(BombOnShelterExplosion, self).__init__(actor)


class BombHitsGroundExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'bomb_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_BOMB

    def __init__(self, actor):
        super(BombHitsGroundExplosion, self).__init__(actor)


class BombInSkyExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'bomb_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_BOMB

    def __init__(self, actor):
        super(BombInSkyExplosion, self).__init__(actor)


class BombHitsLaserExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'bomb_air_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_BOMB

    def __init__(self, actor):
        super(BombHitsLaserExplosion, self).__init__(actor)


class UfoExplosion(BaseExplosion):

    image_list = []
    file_list = [ 'ufo_exp_0.png' ]
    anim_frames = 0
    defaultlife = Globals.EXPLOSION_DEFAULT_LIFE_UFO
    alert_sound = 0

    def __init__(self, actor):
        super(UfoExplosion, self).__init__(actor)

    def update(self):
        super(UfoExplosion, self).update()
        if not self.alive():
            Ufo.ufo_overhead = False
            Ufo.alert_sound.fadeout(Globals.SFX_FADEOUT_UFO)
            #self.actor.rect.move_ip(-20, -20)



class LaserShot(pygame.sprite.Sprite):
    speed = Globals.LASER_SHOT_SPEED
    image_list = []
    scale = Globals.PLAYER_SCALE
    num_frames = 0
    score = 0

    @staticmethod
    def loadImage(file_name):
        LaserShot.image_list.append(load_image(file_name, LaserShot.scale))
        LaserShot.num_frames = len(LaserShot.image_list)

    def __init__(self, pos):
        super(LaserShot, self).__init__(self.containers)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(midbottom = pos)
        self.cur_frame = 0

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()


class InvaderBomb(pygame.sprite.Sprite):
    speed = 9
    image_list = []
    scale = Globals.INVADER_SCALE
    num_frames = 0

    @staticmethod
    def loadImage(file_pattern):
        InvaderBomb.image_list = load_images_pattern(Globals.BOMB_FILE, InvaderBomb.scale)
        InvaderBomb.num_frames = len(InvaderBomb.image_list)

    def __init__(self, Invader):
        super(InvaderBomb, self).__init__(self.containers)
        self.cur_frame = 0
        if not InvaderBomb.image_list:
            print "Crap!"

        self.image = InvaderBomb.image_list[self.cur_frame]
        self.rect = self.image.get_rect(midbottom =
                    Invader.rect.move(0, 5).midbottom)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % InvaderBomb.num_frames
        self.image = self.image_list[self.cur_frame]
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= Globals.SCREEN_HEIGHT:
            BombHitsGroundExplosion(self)
            self.kill()

    def kill(self):
        BaseInvader.bombExploded()
        super(InvaderBomb, self).kill()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.font = pygame.font.Font(None, Globals.FONT_SIZE)
        self.font.set_italic(1)
        self.color = pygame.Color('white')
        self.lastscore = -1
        self.score = 0
        self.update()
        self.rect = self.image.get_rect().move(Globals.POS_SCORE_X, Globals.POS_SCORE_Y)

    def addToScore(self, score_inc):
        self.score += score_inc

    def update(self):
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Score: %d" % self.score
            self.image = self.font.render(msg, 0, self.color)

