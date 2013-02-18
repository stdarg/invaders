#! /usr/bin/env python
import random

#import basic pygame modules
import pygame
from pygame.locals import *

# import my own modules
from Global_Constants import *
from SoundUtil import *
import SpriteLib
from SpriteMgr import *


#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit, "Sorry, extended image module required"


def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print 'Warning, no sound'
        pygame.mixer = None

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, BIT_DEPTH)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    SpriteMgr.loadImages();
    """
    SpriteLib.Player.loadImage(LASER_BASE_FILE)
    SpriteLib.Explosion.loadImage(EXPLOSION_FILE)
    SpriteLib.BaseInvader.loadImages()
    #SpriteLib.InvaderA.loadImages()
    #SpriteLib.InvaderB.loadImages()
    #SpriteLib.InvaderC.loadImages()
    SpriteLib.InvaderBomb.loadImage(BOMB_FILE)
    SpriteLib.LaserShot.loadImage(LASER_SHOT_FILE)
    """

    #decorate the game window
    icon = pygame.transform.scale(SpriteLib.InvaderA.image_list[0], (ICON_WIDTH, ICON_HEIGHT))
    pygame.display.set_icon(icon)
    pygame.display.set_caption(GAME_NAME)
    pygame.mouse.set_visible(0)

    #create the background, tile the bgd image
    bgdtile = SpriteLib.load_image(BACKGROUND_IMAGE)
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #load the sound effects
    boom_sound = load_sound(BOOM_SOUND)
    shoot_sound = load_sound(SHOOT_SOUND)

    if pygame.mixer and MUSIC_TOGGLE:
        music = os.path.join(ART_DIR, GAME_MUSIC)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    SpriteMgr.setupContainers()
    """
    # Initialize Game Groups
    #aliens = pygame.sprite.Group()
    aliens = SpriteLib.InvaderGroup()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()

    #assign default groups to each sprite class
    SpriteLib.Player.containers = all
    SpriteLib.InvaderA.containers = aliens, all, lastalien
    SpriteLib.InvaderB.containers = aliens, all, lastalien
    SpriteLib.InvaderC.containers = aliens, all, lastalien
    SpriteLib.LaserShot.containers = shots, all
    SpriteLib.InvaderBomb.containers = bombs, all
    SpriteLib.Explosion.containers = all
    SpriteLib.Score.containers = all
    """

    #Create Some Starting Values
    alienreload = ALIEN_RELOAD
    clock = pygame.time.Clock()

    # initialize our starting sprites
    player = SpriteLib.Player()
    player
    SpriteLib.InvaderA() #note, this 'lives' because it goes into a sprite group
    if pygame.font:
        Score = SpriteLib.Score()
        all.add(Score)

    while player.alive():

        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        firing = keystate[K_SPACE]
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            SpriteLib.LaserShot(player.gunpos())
            shoot_sound.play()
        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            inv_type = int(random.random() * 3)
            if inv_type == 0:
                SpriteLib.InvaderA()
            elif inv_type == 1:
                SpriteLib.InvaderB()
            elif inv_type == 2:
                SpriteLib.InvaderC()
            else:
                print "error inv_type %d" % inv_type
            alienreload = ALIEN_RELOAD

        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            SpriteLib.InvaderBomb(lastalien.sprite)

        # Detect collisions
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            boom_sound.play()
            SpriteLib.Explosion(alien)
            SpriteLib.Explosion(player)
            Score.addToScore(1)
            player.kill()

        for bomb in pygame.sprite.groupcollide(shots, bombs, 1, 1).keys():
            boom_sound.play()
            SpriteLib.Explosion(bomb)

        for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
            boom_sound.play()
            SpriteLib.Explosion(alien)
            Score.addToScore(1)

        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            boom_sound.play()
            SpriteLib.Explosion(player)
            SpriteLib.Explosion(bomb)
            player.kill()

        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(FRAMES_PER_SEC)

    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)


#call the "main" function if running this script
if __name__ == '__main__': main()

