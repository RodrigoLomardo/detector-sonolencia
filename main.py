import cv2
from utils.face_utils import FaceUtils
import time
import pygame


def main():
    # Inicializa a captura de vídeo e o detector
    cap = cv2.VideoCapture(0)
    face_utils = FaceUtils()
    
    pygame.init()
    alarm_sound = pygame.mixer.Sound("assets/alert.wav")  # Carrega o som do alarme
    
    # Configurações de temporização do EAR (Eye Aspect Ratio)
    EYE_CLOSED_THRESHOLD = 2.0  # Tempo mínimo para considerar sonolência (2 segundos)
    ALARM_DURATION = 1.0         # Tempo que o alerta persiste após o EAR normalizar
    eye_closed_start_time = None
    last_alarm_time = None
    
    # Configurações de temporização do MAR (Mouth Aspect Ratio)
    mouth_open_start_time = None
    MOUTH_OPEN_THRESHOLD = 2 # Limite para detecção de bocejo
    MAR_THRESHOLD = 0.5  # Limiar do MAR 
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detecta rostos
        faces = face_utils.detect_faces(frame)
        
        # Desenha retângulos nos rostos detectados
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # obtem os landmarks do rosto
            landmarks = face_utils.get_landmarks(frame, face)
            
            # Calculo do EAR
            left_ear = face_utils.calculate_ear(landmarks, face_utils.LEFT_EYE_POINTS)
            right_ear = face_utils.calculate_ear(landmarks, face_utils.RIGHT_EYE_POINTS)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # exibe o EAR na imagem
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            current_time = time.time()
            
            
             # Condição para detectar sonolência
            # alerta se o ear estiver abaixo de 0.25
            if avg_ear < 0.25:
              if eye_closed_start_time is None: # inicia um contador
                eye_closed_start_time = current_time
              elif current_time - eye_closed_start_time >= EYE_CLOSED_THRESHOLD:
               last_alarm_time = current_time
            else:
              eye_closed_start_time = None
              
              
            if last_alarm_time and (current_time - last_alarm_time) < ALARM_DURATION:
              cv2.putText(frame, "ALERTA: SONOLENCIA!", (x, y - 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
              
              if not pygame.mixer.get_busy():
                alarm_sound.play()
            else:
              if pygame.mixer.get_busy():
                pygame.mixer.stop()
                
                
            # Calculo do MAR
                
            mar = face_utils.calculate_mar(landmarks, face_utils.MOUTH_POINTS)
            cv2.putText(frame, f"MAR: {mar:.2f}", (x, y - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            # Condição para detectar bocejo
            if mar > MAR_THRESHOLD:
                if mouth_open_start_time is None:
                    mouth_open_start_time = current_time
                elif current_time - mouth_open_start_time >= MOUTH_OPEN_THRESHOLD:
                    cv2.putText(frame, "BOCEJO DETECTADO!", (x, y - 130),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else: # Boca fechada
                mouth_open_start_time = None
              
              
              
              
            # desenha os 68 pontos de landmarks
            for n in range(68):
              x_point = landmarks.part(n).x
              y_point = landmarks.part(n).y
              cv2.circle(frame, (x_point, y_point), 1, (255, 0, 0), -1)
            
        cv2.imshow("Detecçao de Sonolencia", frame)
        
        # interromper o script se a tecla 'q' for pressionada
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()