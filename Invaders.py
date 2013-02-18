#! /usr/bin/env python

# import system modules
import random
import os.path

# import pygame module
import pygame

# import my modules
import SpriteLib
import Globals
import SoundUtil


# see if we can load more than standard BMP
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
    bestdepth = pygame.display.mode_ok(Globals.SCREENRECT.size, winstyle, Globals.BIT_DEPTH)
    screen = pygame.display.set_mode(Globals.SCREENRECT.size, winstyle, bestdepth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    Globals.GameData.setupContainers()
    Globals.GameData.loadSounds()
    Globals.GameData.doStaticInits()
    Globals.GameData.loadImages()
    Globals.GameData.setBaseShelters()


    # decorate the game window
    icon = pygame.transform.scale(SpriteLib.InvaderA.image_list[0], (Globals.ICON_WIDTH, Globals.ICON_HEIGHT))
    pygame.display.set_icon(icon)
    pygame.display.set_caption(Globals.GAME_NAME)
    pygame.mouse.set_visible(0)

    # create the background, tile the bgd image
    bgdtile = SpriteLib.load_image(Globals.BACKGROUND_IMAGE)
    background = pygame.Surface(Globals.SCREENRECT.size)
    for x in range(0, Globals.SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()


    # move the below to the formation object
    invader_thump = SoundUtil.load_sound(Globals.INVADER_THUMP[0])

    if pygame.mixer and Globals.MUSIC_TOGGLE:
        music = os.path.join(Globals.ART_DIR, Globals.INVADER_THUMP[0])
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)


    # Create Some Starting Values
    alienreload = 0
    clock = pygame.time.Clock()

    # initialize our starting sprites
    player = SpriteLib.Player()

    if pygame.font:
        Score = SpriteLib.Score()
        Globals.GameData.all.add(Score)

    #pygame.time.set_timer(pygame.USEREVENT, 13)
    invader_thump.play(Globals.SOUND_LOOP_FOREVER)
    ufo = 0

    while player.alive():

        # get input
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT or \
                (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
                    return
            #elif event.type == pygame.USEREVENT:
            #        pygame.time.set_timer(pygame.USEREVENT, 750)
            #        invader_thump.play()

        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        Globals.GameData.all.clear(screen, background)

        # update all the sprites
        Globals.GameData.all.update()

        # handle player input
        direction = keystate[pygame.locals.K_RIGHT] - keystate[pygame.locals.K_LEFT]
        player.move(direction)
        firing = keystate[pygame.locals.K_SPACE]

        if not player.reloading and firing and len(Globals.GameData.shots) < Globals.MAX_SHOTS:
            player.fire()

        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * Globals.ALIEN_ODDS):
            inv_type = int(random.random() * 3)
            if inv_type == 0:
                SpriteLib.InvaderA()
            elif inv_type == 1:
                SpriteLib.InvaderB()
            elif inv_type == 2:
                SpriteLib.InvaderC()
            else:
                print "error inv_type %d" % inv_type
            alienreload = Globals.ALIEN_RELOAD


        SpriteLib.Ufo.reload_time = SpriteLib.Ufo.reload_time - 1

        if not SpriteLib.Ufo.ufo_overhead and SpriteLib.Ufo.reload_time <= 0:
            SpriteLib.Ufo.ufo_overhead = True
            ufo = SpriteLib.Ufo()
            SpriteLib.Ufo.reload_time = Globals.UFO_RELOAD_TIME


        # Detect collisions
        for alien in pygame.sprite.spritecollide(player, Globals.GameData.aliens, 1):
            Score.addToScore(alien.score)
            player.handleDeath()

        for bomb in pygame.sprite.groupcollide(Globals.GameData.bombs, Globals.GameData.shots, 1, 1).keys():
            SpriteLib.BombHitsLaserExplosion(bomb)
            Score.addToScore(1)

        if SpriteLib.Ufo.ufo_overhead:
            for laser_shot in pygame.sprite.spritecollide(ufo, Globals.GameData.shots, 1):
                ufo.takeHit()
                Score.addToScore(ufo.score)

        if len(Globals.GameData.bombs):
            for bomb in Globals.GameData.bombs:
                for shelter in pygame.sprite.groupcollide(Globals.GameData.base_shelters, [bomb], 0, 0).keys():
                    shelter.bombHit(bomb, False)

        if len(Globals.GameData.shots):
            for shot in Globals.GameData.shots:
                for shelter in pygame.sprite.groupcollide(Globals.GameData.base_shelters, [shot], 0, 0).keys():
                    shelter.bombHit(shot, True)

        for alien in pygame.sprite.groupcollide(Globals.GameData.aliens, Globals.GameData.shots, 1, 1).keys():
            Score.addToScore(alien.score)

        for bomb in pygame.sprite.spritecollide(player, Globals.GameData.bombs, 1):
            SpriteLib.PlayerExplosion(player)
            player.kill()

        # draw the scene
        dirty = Globals.GameData.all.draw(screen)
        pygame.display.update(dirty)

        # cap the framerate
        clock.tick(Globals.FRAMES_PER_SEC)

    if pygame.mixer:
        pygame.mixer.music.fadeout(Globals.ONE_SECOND)
    pygame.time.wait(Globals.ONE_SECOND)


# call the "main" function if running this script
if __name__ == '__main__': main()

