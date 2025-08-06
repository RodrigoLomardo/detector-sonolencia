import time
import csv
import os
from typing import List, Tuple

# Caminho para o arquivo CSV único que armazenará dados de todas as sessões
ALL_SESSIONS_CSV_PATH = os.path.join("reports", "all_sessions_data.csv")

class EventLogger:
    def __init__(self, session_id: str, ear_threshold: float = 0.2, mar_threshold: float = 0.5):
        self.session_id = session_id
        self.EAR_THRESHOLD = ear_threshold
        self.MAR_THRESHOLD = mar_threshold
        self.events: List[Tuple[str, float, float]] = [] # (event_type, timestamp, metric_value)
        self._initialize_csv()
        
    def _initialize_csv(self):
        """Inicializa o arquivo CSV único com cabeçalhos se ele não existir ou estiver incorreto."""
        headers = ['session_id', 'timestamp', 'event_type', 'metric_value']
        
        if not os.path.exists(ALL_SESSIONS_CSV_PATH):
            with open(ALL_SESSIONS_CSV_PATH, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
        else:
            # Verifica se o cabeçalho existente é o esperado
            with open(ALL_SESSIONS_CSV_PATH, mode='r', newline='') as file:
                reader = csv.reader(file)
                try:
                    current_headers = next(reader)
                    if current_headers != headers:
                        print(f"Aviso: Cabeçalho do CSV {ALL_SESSIONS_CSV_PATH} está incorreto. Por favor, verifique ou remova o arquivo para recriá-lo.")
                        # Poderíamos adicionar uma lógica para recriar o arquivo ou migrar dados, mas por enquanto, apenas avisamos.
                except StopIteration:
                    # Arquivo existe mas está vazio, escreve o cabeçalho
                    with open(ALL_SESSIONS_CSV_PATH, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)
        
    def add_event(self, event_type: str, timestamp: float, metric_value: float):
        """Registra um evento (olhos/bocejo) com timestamp e valor da métrica, e salva no CSV único."""
        self.events.append((event_type, timestamp, metric_value))
        with open(ALL_SESSIONS_CSV_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.session_id, timestamp, event_type, metric_value])
        
    def evaluate_risk(self, time_window: float = 30.0, min_events: int = 3) -> bool:
        """Verifica se há risco crítico nos últimos 'time_window' segundos."""
        current_time = time.time()
        recent_events = [e for e in self.events if current_time - e[1] <= time_window]
        return len(recent_events) >= min_events
    
    def get_recent_events(self, time_window: float = 30.0) -> list:
        """Retorna eventos recentes da sessão atual."""
        current_time = time.time()
        return [e for e in self.events if current_time - e[1] <= time_window]