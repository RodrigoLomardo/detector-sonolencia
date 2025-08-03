from utils.alert_manager import AlertManager
from modules.detector.face_detector import FaceDetector
from modules.analyzer.sleepiness_analyzer import SleepinessAnalyzer
import cv2
import time

def main():
    # Inicialização dos módulos
    cap = cv2.VideoCapture(0)
    face_detector = FaceDetector()
    alert_manager = AlertManager()
    sleepiness_analyzer = SleepinessAnalyzer(ear_threshold=0.2, mar_threshold=0.5)

    # Configurações de temporização
    EYE_CLOSED_THRESHOLD = 2.0  # Tempo mínimo para considerar olhos fechados
    MOUTH_OPEN_THRESHOLD = 2.0   # Tempo mínimo para considerar bocejo
    SONOLENCIA_THRESHOLD = 3     # Número mínimo de eventos para alerta grave
    
    # Variáveis de estado
    eye_closed_start_time = None
    mouth_open_start_time = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = face_detector.detect_faces(frame)
        
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            landmarks = face_detector.get_landmarks(frame, face)
            current_time = time.time()

            # Análise EAR
            left_ear = face_detector.calculate_ear(landmarks, face_detector.LEFT_EYE_POINTS)
            right_ear = face_detector.calculate_ear(landmarks, face_detector.RIGHT_EYE_POINTS)
            avg_ear = (left_ear + right_ear) / 2.0
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            if avg_ear < 0.25:
                if eye_closed_start_time is None:
                    eye_closed_start_time = current_time
                elif current_time - eye_closed_start_time >= EYE_CLOSED_THRESHOLD:
                    sleepiness_analyzer.add_event("olhos", current_time)
                    alert_manager.trigger_alert(frame, "ALERTA: OLHOS FECHADOS!", (x, y - 70))
                    eye_closed_start_time = None
            else:
                eye_closed_start_time = None

            # Análise MAR
            mar = face_detector.calculate_mar(landmarks, face_detector.MOUTH_POINTS)
            cv2.putText(frame, f"MAR: {mar:.2f}", (x, y - 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            if mar > 0.5:
                if mouth_open_start_time is None:
                    mouth_open_start_time = current_time
                elif current_time - mouth_open_start_time >= MOUTH_OPEN_THRESHOLD:
                    sleepiness_analyzer.add_event("bocejo", current_time)
                    alert_manager.trigger_alert(frame, "BOCEJO DETECTADO!", (x, y - 130))
                    mouth_open_start_time = None
            else:
                mouth_open_start_time = None

            # Verificação geral de risco
            if sleepiness_analyzer.evaluate_risk(min_events=SONOLENCIA_THRESHOLD):
                alert_manager.trigger_alert(frame, "ALERTA: MOTORISTA SONOLENTO", (10, 120))
            else:
                alert_manager.stop_alert()

            # Exibe contagem de eventos
            total_eventos = len(sleepiness_analyzer.get_recent_events())
            cv2.putText(frame, f"Eventos: {total_eventos}/{SONOLENCIA_THRESHOLD}", 
                       (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Desenha landmarks
            for n in range(68):
                x_point = landmarks.part(n).x
                y_point = landmarks.part(n).y
                cv2.circle(frame, (x_point, y_point), 1, (255, 0, 0), -1)

        cv2.imshow("Detecção de Sonolência", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()