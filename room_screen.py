import pygame,sys
from hand_control import get_hand_state_from_frame
from config import room_textures,screen,global_cap,global_hands,SCREEN_HEIGHT,SCREEN_WIDTH,WHITE,clock

def show_room_screen(room_name, texture_key, room_end):
    wait = True
    while wait:
        img = room_textures.get(texture_key)
        if img:
            screen.blit(img, (0, 0))
        else:
            screen.fill((0, 0, 0))

        title_font = pygame.font.Font(None, 60)
        text_font = pygame.font.Font(None, 40)
        small_font = pygame.font.Font(None, 28)

        if room_end not in ("winn", "ghost"):
            title_text = title_font.render(f"Room: {room_name}", True, WHITE)
            screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, 80)))

            ret, frame = global_cap.read()
            if ret:
                small_w, small_h = 320, 180
                try:
                    small_surf = cvframe_to_surf(frame, (small_w, small_h), mirror=True)
                    screen.blit(small_surf, (SCREEN_WIDTH - small_w - 10, 10))
                except Exception:
                    pass

            label = text_font.render(f"{room_name.capitalize()} Room", True, WHITE)
            screen.blit(label, (20, 20))

        if room_end == "winn":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            msg1 = text_font.render("You Exit from House...", True, (0, 255, 0))
            screen.blit(msg1, msg1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180)))

            win_text = [
                "The first light of dawn cut through the mist as you stumbled out of Blackwood House.",
                "Behind you, the door slammed shut — sealing the horrors within.",
                "Your friends’ laughter still echoes faintly in your mind… or maybe it’s the house calling you back.",
                "You escaped Annabelle’s curse — this time.",
                "",
                "But remember: some stories never end. They just wait to begin again."
            ]

            y_offset = SCREEN_HEIGHT // 2 - 100
            for line in win_text:
                msg = small_font.render(line, True, (0, 255, 0))
                rect = msg.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(msg, rect)
                y_offset += 40

            tip = small_font.render("Press ENTER to Play Again | Q to Quit", True, WHITE)
            screen.blit(tip, tip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)))

        elif room_end == "ghost":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            msg1 = text_font.render("Annabelle Found You..", True, (255, 0, 0))
            screen.blit(msg1, msg1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180)))

            ghost_text = [
                "The whispers grew louder… until they spoke your name.",
                "The shadows closed in, cold fingers brushing against your neck.",
                "You turned — but it was already too late.",
                "Her porcelain face smiled, her glass eyes gleamed.",
                "The cursed doll claimed another soul… yours.",
                "",
                "The Blackwood House stands silent once again, waiting for the next to enter."
            ]

            y_offset = SCREEN_HEIGHT // 2 - 100
            for line in ghost_text:
                msg = small_font.render(line, True, (255, 0, 0))
                rect = msg.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(msg, rect)
                y_offset += 40

            tip = small_font.render("Press ENTER to Play Again | Q to Quit", True, WHITE)
            screen.blit(tip, tip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)))

        else:
            if texture_key in ("anabella", "exit"):
                tip = small_font.render("Press ENTER to Play Again | Q to Quit", True, WHITE)
            else:
                tip = small_font.render("Make a closed fist or press ENTER to go back", True, WHITE)
            screen.blit(tip, (20, SCREEN_HEIGHT - 60))

        pygame.display.flip()
        clock.tick(30)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    return "quit"
                if e.key == pygame.K_RETURN:
                    if room_end in ("winn", "ghost"):
                        return "play"
                    else:
                        return "back"

        if room_end in ("winn", "ghost"):
            continue

        if ret:
            state, _ = get_hand_state_from_frame(frame, global_hands)
            if state == "closed":
                return "back"
