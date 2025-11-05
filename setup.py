import pygame,random,cv2
from hand_control import count_extended_fingers,draw_steering_overlay,cvframe_to_surf
from room_screen import show_room_screen
from config import SCREEN_HEIGHT,SCREEN_WIDTH,room_textures,global_cap,global_hands,screen,background_house,player_img,small_font,WHITE,clock,mp_hands_module,MIRROR_CAMERA,DEADZONE,PLAYER_SPEED,STATE_PLAY

def run_game():
    pygame.mixer.music.pause()
    pygame.mixer.music.load("sounds/doll_box_conjuring.mp3")
    pygame.mixer.music.play(-1)
    center_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200)
    rooms = {
        "center": center_rect,
        "left": pygame.Rect(center_rect.left - 250, center_rect.top, 200, 200),
        "right": pygame.Rect(center_rect.right + 50, center_rect.top, 200, 200),
        "up": pygame.Rect(center_rect.left, center_rect.top - 250, 200, 200),
        "down": pygame.Rect(center_rect.left, center_rect.bottom + 50, 200, 200),
    }
    possible_rooms = ["left", "right", "up", "down"]
    anabella_room = random.choice(possible_rooms)
    exit_room = random.choice([r for r in possible_rooms if r != anabella_room])
    room_open_images = {r: None for r in possible_rooms}
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    thumb_size = (200, 200)
    default_thumb = pygame.transform.smoothscale(
        room_textures["default"] or pygame.Surface((200, 200)), thumb_size
    )

    open_thumbs = {}
    for k in ("open1", "open2", "open3"):
        img = room_textures.get(k)
        open_thumbs[k] = pygame.transform.smoothscale(img if img else room_textures["default"], thumb_size)
    prev_open_state = False

    while True:
        ret, frame = global_cap.read()
        if not ret:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return None
            continue
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = global_hands.process(frame_rgb)
        dx = dy = 0
        hand_open = False
        hand_closed = False
        fingers_count = 0
        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0]
            fingers_count = count_extended_fingers(lm)
            if fingers_count >= 4:
                hand_open = True
            if fingers_count <= 1:
                hand_closed = True
            wrist = lm.landmark[mp_hands_module.HandLandmark.WRIST]
            raw_x, raw_y = int(wrist.x * SCREEN_WIDTH), int(wrist.y * SCREEN_HEIGHT)
            x = SCREEN_WIDTH - raw_x if MIRROR_CAMERA else raw_x
            y = raw_y
            cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            if x < cx - DEADZONE: dx = -PLAYER_SPEED
            elif x > cx + DEADZONE: dx = PLAYER_SPEED
            if y < cy - DEADZONE: dy = -PLAYER_SPEED
            elif y > cy + DEADZONE: dy = PLAYER_SPEED
        player_pos[0] = max(0, min(SCREEN_WIDTH, player_pos[0] + dx))
        player_pos[1] = max(0, min(SCREEN_HEIGHT, player_pos[1] + dy))
        touching = None
        for name, rect in rooms.items():
            if rect.collidepoint(player_pos):
                touching = name
        screen.blit(background_house, (0, 0))
        for name, rect in rooms.items():
            if name == "center":
                pygame.draw.rect(screen, (150, 150, 150), rect, 2)
                continue
            assigned_key = room_open_images[name]
            if assigned_key is None:
                screen.blit(default_thumb, rect)
            else:
                screen.blit(open_thumbs[assigned_key], rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        try:
            steering_frame = frame.copy()
            steering_frame = draw_steering_overlay(steering_frame)
            cam_small = cvframe_to_surf(steering_frame, (320, 180), mirror=True)
            screen.blit(cam_small, (SCREEN_WIDTH - 330, 10))
            cam_border = pygame.Rect(SCREEN_WIDTH - 330, 10, 320, 180)
            pygame.draw.rect(screen, (255, 255, 255), cam_border, 2)
        except Exception as e:
            print("Camera display error:", e)

        if player_img:
            rect = player_img.get_rect(center=player_pos)
            screen.blit(player_img, rect)

        tip = small_font.render("Move hand to move. Open hand to ENTER a room. Fist to go back / quit.", True, WHITE)
        screen.blit(tip, (10, SCREEN_HEIGHT - 40))

        if touching and touching != "center":
            info = small_font.render(f"Touched: {touching} ({'Anabella' if touching==anabella_room else 'Exit' if touching==exit_room else 'Room'})", True, WHITE)
            screen.blit(info, (10, SCREEN_HEIGHT - 70))
            pygame.draw.rect(screen, (255,200,0), rooms[touching], 4)

        pygame.display.flip()
        clock.tick(30)

        if hand_open and not prev_open_state and touching and touching != "center":
            door = pygame.mixer.Sound("sounds/door_open.mp3")
            door.play()
            if touching == anabella_room:
                pygame.mixer.music.stop()
                door.stop()
                pygame.mixer.music.load("sounds/ghost.mp3")
                pygame.mixer.music.play()
                action = show_room_screen(touching, "anabella","ghost")
                if action == "play":
                    return STATE_PLAY
                elif action == "quit":
                    return None
            elif touching == exit_room:
                pygame.mixer.music.stop()
                door.stop()
                pygame.mixer.music.load("sounds/conjuring.mp3")
                pygame.mixer.music.play()
                action = show_room_screen(touching, "exit","winn")
                if action == "play":
                    return STATE_PLAY
                elif action == "quit":
                    return None
            else:
                if room_open_images[touching] is None:
                    choice = random.choice(["open1", "open2", "open3"])
                    room_open_images[touching] = choice
                    _ = show_room_screen(touching, choice,None)
                else:
                    _ = show_room_screen(touching, room_open_images[touching],None)

        prev_open_state = hand_open
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    return None
    return None