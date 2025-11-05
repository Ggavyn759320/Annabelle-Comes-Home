import pygame,cv2
import mediapipe as mp

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Annabelle Comes Home")
clock = pygame.time.Clock()

def load_image(path, size=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except Exception as e:
        print(f"⚠️ Failed to load {path}: {e}")
        return None

welcome_bg = load_image("assets/welcome_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
background_house = load_image("assets/background_house.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
player_img = load_image("assets/player.png", (60, 60))

room_textures = {
    "default": load_image("assets/default_room.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "open1": load_image("assets/room_open1.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "open2": load_image("assets/room_open2.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "open3": load_image("assets/room_open3.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "anabella": load_image("assets/room_annabelle.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    "exit": load_image("assets/room_exit.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
}

if background_house is None:
    background_house = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_house.fill((20, 20, 20))

title_font = pygame.font.SysFont("Times New Roman", 72, bold=True)
text_font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 22)
WHITE, GRAY, RED, GREEN = (255, 255, 255), (180, 180, 180), (200, 50, 50), (50, 200, 50)

STATE_WELCOME = "welcome"
STATE_VIDEO = "video"
STATE_INTRO_TEXT = "intro_text"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
game_state = STATE_WELCOME

PLAYER_SPEED = 6
MIRROR_CAMERA = True
DEADZONE = 80

mp_hands_module = mp.solutions.hands
global_cap = cv2.VideoCapture(0)
global_hands = mp_hands_module.Hands(max_num_hands=1, min_detection_confidence=0.6)