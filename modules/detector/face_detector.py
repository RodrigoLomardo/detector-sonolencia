import cv2
import dlib
import os
import scipy.spatial.distance as distance

class FaceDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        
        self.LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]  # Landmarks do olho esquerdo
        self.RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]  # Landmarks do olho direito
        
        self.MOUTH_POINTS = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]  # Landmarks da boca
        
        # Carrega o modelo de landmarks (caminho relativo à raiz do projeto)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "../..", "models", "shape_predictor_68_face_landmarks.dat")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo de landmarks não encontrado em: {model_path}")
        
        self.predictor = dlib.shape_predictor(model_path)
        
        
    # detecta rostos em um frame
    def detect_faces(self, frame):
        """Detecta rostos em um frame usando dlib."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        return faces
      
    # obtém os landmarks do rosto
    def get_landmarks(self, frame, face):
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      landmarks = self.predictor(gray, face)
      return landmarks
    
    # calculo do EAR (Eye Aspect Ratio)
    def calculate_ear(self, landmarks, eye_points):
      """Calcula o Eye Aspect Ratio (EAR) para os pontos dos olhos."""

      # Obtém as coordenadas dos pontos dos olhos
      eye_region = [(landmarks.part(n).x, landmarks.part(n).y) for n in eye_points]
      
      # calcula a distancia vertical e horizontal
      A = distance.euclidean(eye_region[1], eye_region[5])  
      B = distance.euclidean(eye_region[2], eye_region[4])  
      C = distance.euclidean(eye_region[0], eye_region[3])
      
      EAR = (A + B) / (2.0 * C)
      return EAR
   
    #calculo do MAR (Mouth Aspect Ratio)
    def calculate_mar(self, landmarks, mouth_points):
      """calcula o mouth aspect ratio (MAR) para os pontos da boca. (detecta bocejos)"""
      
      # obtem as coordenadas dos pontos da boca
      mounth_region = [(landmarks.part(n).x, landmarks.part(n).y) for n in mouth_points]
      
      # calculo da distancia vertical e horizontal
      A = distance.euclidean(mounth_region[2], mounth_region[10])  # Distância vertical
      B = distance.euclidean(mounth_region[4], mounth_region[8])  # Distância vertical interna
      C = distance.euclidean(mounth_region[0], mounth_region[6]) # distancia horizontal
      
      MAR = (A + B) / (2.0 * C)
      return MAR