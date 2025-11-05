import cv2
import pygame
from config import MIRROR_CAMERA
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def cvframe_to_surf(frame, size=None, mirror=True):
    if mirror:
        frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if size:
        frame_rgb = cv2.resize(frame_rgb, size)
    surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
    return surf

def draw_steering_overlay(frame):
    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    dx, dy = int(w * 0.25), int(h * 0.25)

    overlay = frame.copy()
    cv2.rectangle(overlay, (cx - dx, cy - dy), (cx + dx, cy + dy), (80, 80, 220), -1)
    cv2.addWeighted(overlay, 0.15, frame, 0.85, 0, frame)

    cv2.line(frame, (cx, 0), (cx, h), (150, 150, 150), 1)
    cv2.line(frame, (0, cy), (w, cy), (150, 150, 150), 1)

    cv2.putText(frame, "UP", (cx - 20, cy - dy - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "DOWN", (cx - 40, cy + dy + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "LEFT", (cx - dx - 70, cy + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "RIGHT", (cx + dx + 20, cy + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    cv2.circle(frame, (cx, cy), 25, (255, 255, 255), 1)
    return frame

def count_extended_fingers(hand_landmarks):
    count = 0
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip_idx, pip_idx in zip(tips, pips):
        tip = hand_landmarks.landmark[tip_idx]
        pip = hand_landmarks.landmark[pip_idx]
        if tip.y < pip.y:
            count += 1
    return count

def get_hand_state_from_frame(frame, hands, mirror=MIRROR_CAMERA, draw_hand=True):
    if frame is None:
        return None, 0

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return None, 0

    lm = results.multi_hand_landmarks[0]

    if draw_hand:
        mp_drawing.draw_landmarks(
            frame,
            lm,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 100, 255), thickness=2),
        )

    fingers = count_extended_fingers(lm)

    if fingers >= 4:
        state = "open"
    elif fingers <= 1:
        state = "closed"
    else:
        state = "neutral"

    return state, fingers

    