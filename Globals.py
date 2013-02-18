#import random

# import pygame modules
import pygame
from pygame.locals import Rect

# import my modules
import SoundUtil
import SpriteLib



ALIEN_ODDS = 22     #chances a new alien appears
ALIEN_RELOAD = 60     #frames between new aliens
ART_DIR = 'data'
BACKGROUND_IMAGE = 'si_orig_background.png'
BASE_SHELTER_FILE = 'base_shelter.png'
BIT_DEPTH = 32
BOMB_FILE = 'invader_fired_sqg3_*.png'
BOMB_ODDS = 120        #chances a new bomb will drop

EXPLOSION_ANIM_CYCLE = 3
EXPLOSION_ANIM_FRAMES = 2
EXPLOSION_DEFAULT_LIFE = 12
EXPLOSION_INVADER_LIFE = 3

EXPLOSION_DEFAULT_LIFE_PLAYER = 18
EXPLOSION_DEFAULT_LIFE_SHELTER = 18
EXPLOSION_DEFAULT_LIFE_BOMB = 18
EXPLOSION_DEFAULT_LIFE_UFO = 18

SFX_FADEOUT_UFO = 500
POS_SCORE_X = 10
POS_SCORE_Y = 475
POS_UFO_Y = 10

FONT_SIZE = 20
FRAMES_PER_SEC = 30
GAME_NAME = 'Space Invaders'
ICON_HEIGHT = 32
ICON_WIDTH = 32
INVADER_ANIM_CYCLE = 12
INVADER_EXPLOSION = 'invader_exp_0.png'
INVADER_NUM_FRAMES = 2
INVADER_SCALE = 2
INVADER_SHOT = 'shoot.wav'
INVADER_SPEED = 3
INVADER_THUMP = [ 'fastinvader1.wav', 'fastinvader2.wav', 'fastinvader3.wav', 'fastinvader4.wav' ]
LASER_BASE_FILE = "laser_base.png"
LASER_SHOT_FILE = 'invader_laser_shot.png'
LASER_SHOT_SPEED = -11
SOUND_LOOP_FOREVER = -1
MAX_SHOTS = 2      #most player bullets onscreen
MUSIC_TOGGLE = False
ONE_SECOND = 1000

PLAYER_EXPLOSION = 'explosion.wav'
PLAYER_SCALE = 2
PLAYER_SHOT = 'invaderkilled.wav'

SCORE_INVADER_A = 10
SCORE_INVADER_B = 20
SCORE_INVADER_C = 30
SCORE_UFO = 100

SCREEN_HEIGHT = 490
SCREEN_WIDTH = 450

SHOOT_SOUND = 'car_door.wav'

SOUND_UFO_FADEOUT_MS = 200

SPEED_PLAYER = 10
SPEED_UFO = 3

UFO_ALERT = 'ufo_lowpitch.wav'
UFO_RELOAD_TIME = 360

SCREENRECT = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)





class GameData:
    __metaclass__ = type

    aliens = []
    shots = []
    bombs = []
    all = []
    lastalien = []
    shots = []
    base_shelters = []
    shelterList = []
    ufo = []

    @staticmethod
    def loadImages():
        #SpriteLib.Player.loadImages([ LASER_BASE_FILE ], SpriteLib.Player)

        #SpriteLib.BaseInvader.loadImages()
        SpriteLib.InvaderBomb.loadImage(BOMB_FILE)
        SpriteLib.LaserShot.loadImage(LASER_SHOT_FILE)
        SpriteLib.BaseShelter.loadImages([ BASE_SHELTER_FILE ], SpriteLib.BaseShelter)
        SpriteLib.BaseExplosion.loadImages()
        SpriteLib.Ufo.loadImages([ "invader_ufo.png" ], SpriteLib.Ufo)

    @staticmethod
    def setupContainers():
        # Initialize Game Groups

        GameData.shots = pygame.sprite.Group()
        GameData.bombs = pygame.sprite.Group()
        GameData.all = pygame.sprite.RenderUpdates()
        GameData.lastalien = pygame.sprite.GroupSingle()
        GameData.base_shelters = pygame.sprite.Group()
        GameData.aliens = pygame.sprite.Group()
        GameData.ufo = pygame.sprite.GroupSingle()

        #assign default groups to each sprite class
        SpriteLib.Ufo.containers = GameData.all, GameData.ufo
        #SpriteLib.Player.containers = GameData.all
        SpriteLib.InvaderA.containers = GameData.aliens, GameData.all, GameData.lastalien
        SpriteLib.InvaderB.containers = GameData.aliens, GameData.all, GameData.lastalien
        SpriteLib.InvaderC.containers = GameData.aliens, GameData.all, GameData.lastalien
        SpriteLib.LaserShot.containers = GameData.shots, GameData.all
        SpriteLib.InvaderBomb.containers = GameData.bombs, GameData.all

        SpriteLib.InvaderExplosion.containers = GameData.all

        SpriteLib.Score.containers = GameData.all
        SpriteLib.BaseShelter.containers = GameData.base_shelters, GameData.all
        SpriteLib.BombOnShelterExplosion.containers = GameData.all
        SpriteLib.InvaderExplosion.containers = GameData.all
        SpriteLib.PlayerExplosion.containers = GameData.all
        SpriteLib.BombOnShelterExplosion.containers = GameData.all
        SpriteLib.BombHitsGroundExplosion.containers = GameData.all
        SpriteLib.BombInSkyExplosion.containers = GameData.all
        SpriteLib.BombHitsLaserExplosion.containers = GameData.all
        SpriteLib.UfoExplosion.containers = GameData.all

    @staticmethod
    def doStaticInits():
        SpriteLib.Player.static_init([GameData.all])
        SpriteLib.BaseInvader.static_init()

    @staticmethod
    def loadSounds():
        # load some sounds
        SpriteLib.Ufo.alert_sound = SoundUtil.load_sound(UFO_ALERT)
        #SpriteLib.Player.explosion_sound = load_sound(PLAYER_EXPLOSION)

    @staticmethod
    def setBaseShelters():

        for x in range(64, 424, 90):
            shelter = SpriteLib.BaseShelter((x, 400))
            GameData.shelterList.append(shelter)

        """
        shelter = SpriteLib.BaseShelter((64, 400))
        SpriteLib.shelterList.append(shelter)
        
        SpriteLib.BaseShelter((154, 400))
        SpriteLib.BaseShelter((244, 400))
        SpriteLib.BaseShelter((334, 400))
        """
    #def __init__(self):

