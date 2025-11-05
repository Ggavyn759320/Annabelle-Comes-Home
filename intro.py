import cv2,pygame,threading
from moviepy.editor import VideoFileClip
from config import screen,welcome_bg,title_font,text_font,WHITE,GRAY,small_font,SCREEN_HEIGHT,SCREEN_WIDTH,clock,load_image

def draw_welcome_screen():
    screen.blit(welcome_bg or background_house, (0, 0))
    title = title_font.render("Annabelle Comes Home", True, WHITE)
    play = text_font.render("Use open-hand to ENTER a room", True, GRAY)
    hint = small_font.render("Move hand to move player. Press Q to quit.", True, GRAY)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
    screen.blit(play, play.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)))
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)))

def play_intro_video(video_path):
    cap = cv2.VideoCapture(video_path)
    try:
        clip = VideoFileClip(video_path)
    except Exception as e:
        print("Could not load video with MoviePy:", e)
        clip = None

    def play_audio():
        if clip and clip.audio:
            try:
                clip.audio.preview()
            except Exception as e:
                print("Audio playback error:", e)

    if clip:
        threading.Thread(target=play_audio, daemon=True).start()

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                cap.release()
                if clip: clip.close()
                return
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
        surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(fps)
    cap.release()
    if clip:
        clip.close()

def show_intro_text():
    pygame.mixer.music.load("sounds/doll_box_conjuring.mp3")
    pygame.mixer.music.play(-1)
    bg = load_image("assets/hunted_house.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 80)
    text_font = pygame.font.Font(None, 28)
    title = title_font.render("Welcome to Anabella Comes Home", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title, title_rect)
    story_lines = [
        "You and your friends entered the abandoned Blackwood House to prove it’s not haunted.",
        "But laughter turned to screams — one by one, your friends vanished into the shadows.",
        "Now only you remain, trapped inside walls that whisper your name.",
        "Four rooms stand between you and the exit, but one hides the cursed doll — Annabelle.",
        "If she finds you, the game ends… and so does your story.",
        "Keep your hands steady, your breath quiet — and survive the night."
    ]
    y_offset = 200
    for line in story_lines:
        text = text_font.render(line, True, GRAY)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40
    small_font = pygame.font.Font(None, 36)
    prompt = small_font.render("Press 'Space Key' to Play or 'Q' to Quit", True, WHITE)
    prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
    screen.blit(prompt, prompt_rect)
    pygame.display.flip()
