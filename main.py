import pygame,sys
from setup import run_game
from config import game_state,STATE_WELCOME,global_cap,global_hands,clock,STATE_VIDEO,STATE_INTRO_TEXT,STATE_PLAY,STATE_GAME_OVER,STATE_WIN
from intro import draw_welcome_screen,play_intro_video,show_intro_text
from hand_control import get_hand_state_from_frame

pygame.init()
pygame.mixer.quit()

running = True
while running:
    if game_state == STATE_WELCOME:
        draw_welcome_screen()
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    game_state = STATE_VIDEO
                elif e.key == pygame.K_q:
                    running = False
        ret, f = global_cap.read()
        if ret:
            state, fc = get_hand_state_from_frame(f, global_hands)
            if state == "open":
                game_state = STATE_VIDEO

    elif game_state == STATE_VIDEO:
        play_intro_video("assets/intro.mp4")
        game_state = STATE_INTRO_TEXT

    elif game_state == STATE_INTRO_TEXT:
        show_intro_text()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    waiting = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    game_state = STATE_PLAY
                    waiting = False
            ret, f = global_cap.read()
            if ret:
                state, fc = get_hand_state_from_frame(f, global_hands)
                if state == "open":
                    game_state = STATE_PLAY
                    waiting = False
            clock.tick(30)
    elif game_state == STATE_PLAY:
        result = run_game()
        if result == STATE_PLAY:
            game_state = STATE_PLAY
        elif result == STATE_GAME_OVER:
            game_state = STATE_GAME_OVER
        elif result == STATE_WIN:
            game_state = STATE_WIN
        elif result is None:
            running = False
        else:
            game_state = STATE_WELCOME

    elif game_state == STATE_GAME_OVER:
        ...
    elif game_state == STATE_WIN:
        ...

    clock.tick(30)

global_cap.release()
global_hands.close()
pygame.quit()
sys.exit()

