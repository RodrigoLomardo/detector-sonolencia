import pygame
import time
import cv2

class AlertManager:
    def __init__(self, sound_path="assets/alert.wav"):
        pygame.init()
        self.alarm_sound = pygame.mixer.Sound(sound_path)
        self.last_alert_time = None
        self.ALARM_DURATION = 1.0

    def trigger_alert(self, frame, text, position, color=(0, 0, 255)):
        """Exibe alerta visual e toca som."""
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        if not pygame.mixer.get_busy():
            self.alarm_sound.play()
        self.last_alert_time = time.time()

    def stop_alert(self):
        """Para o alerta sonoro."""
        if pygame.mixer.get_busy():
            pygame.mixer.stop()

    def is_alert_active(self):
        """Verifica se o alerta ainda está no período de persistência."""
        return self.last_alert_time and (time.time() - self.last_alert_time) < self.ALARM_DURATION