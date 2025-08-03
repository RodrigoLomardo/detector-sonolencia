import time
from typing import List, Tuple

class SleepinessAnalyzer:
    def __init__(self, ear_threshold: float = 0.2, mar_threshold: float = 0.5):
        self.EAR_THRESHOLD = ear_threshold
        self.MAR_THRESHOLD = mar_threshold
        self.events: List[Tuple[str, float]] = []
        
    def add_event(self, event_type: str, timestamp: float):
        """Registra um evento (olhos/bocejo) com timestamp."""
        self.events.append((event_type, timestamp))
        
    def evaluate_risk(self, time_window: float = 30.0, min_events: int = 3) -> bool:
        """Verifica se há risco crítico nos últimos 'time_window' segundos."""
        current_time = time.time()
        recent_events = [e for e in self.events if current_time - e[1] <= time_window]
        return len(recent_events) >= min_events
    
    def get_recent_events(self, time_window: float = 30.0) -> list:
        current_time = time.time()
        return [e for e in self.events if current_time - e[1] <= time_window]