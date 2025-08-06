import numpy as np
import time
from collections import deque

class Calibrator:
    def __init__(self):
        self.ear_resting = deque(maxlen=30)
        self.mar_resting = deque(maxlen=30)
        self.ear_active = deque(maxlen=30)
        self.mar_active = deque(maxlen=30)
        self.current_phase = 0
        self.phase_start_time = time.time()
        self.calibration_done = False

    def update_phase(self, duration_per_phase=5):
        if time.time() - self.phase_start_time >= duration_per_phase:
            self.current_phase += 1
            self.phase_start_time = time.time()
            if self.current_phase >= 3:
                self.calibration_done = True

    def get_instructions(self):
        phases = [
            "Mantenha olhos abertos e boca fechada",
            "Pisque 3 vezes normalmente",
            "Boceje (se possivel)"
        ]
        return phases[self.current_phase] if not self.calibration_done else "Calibracao completa!"

    def add_sample(self, ear, mar):
        if not self.calibration_done:
            if self.current_phase == 0:
                self.ear_resting.append(ear)
                self.mar_resting.append(mar)
            elif self.current_phase == 1 and ear < 0.2:
                self.ear_active.append(ear)
            elif self.current_phase == 2 and mar > 0.4:
                self.mar_active.append(mar)

    def calculate_thresholds(self):
        # Valores padrão caso as listas estejam vazias
        default_ear = 0.25
        default_mar = 0.5
        
        try:
            ear_thresh = np.percentile(list(self.ear_resting), 25) * 0.8 if self.ear_resting else default_ear
            mar_thresh = np.percentile(list(self.mar_resting), 75) * 1.8 if self.mar_resting else default_mar
            
            # Limites de segurança
            ear_thresh = max(0.15, min(ear_thresh, 0.3))
            mar_thresh = max(0.3, min(mar_thresh, 0.7))
            
            return ear_thresh, mar_thresh
        except:
            return default_ear, default_mar