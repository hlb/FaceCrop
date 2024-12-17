import cv2
import mediapipe as mp
import numpy as np

class FaceDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.haar_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.profile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_profileface.xml"
        )

    def detect_face(self, img):
        """
        Detect face in image using multiple methods
        Returns: tuple (x, y, w, h) or None if no face detected
        """
        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Try MediaPipe detection first with very low confidence threshold
        face_detected = False
        x = y = w = h = 0

        with self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.05, model_selection=1
        ) as face_detection:
            results = face_detection.process(rgb_img)
            if results.detections:
                detection = max(results.detections, key=lambda x: x.score[0])
                if detection.score[0] > 0.1:
                    bbox = detection.location_data.relative_bounding_box
                    x = int(bbox.xmin * width)
                    y = int(bbox.ymin * height)
                    w = int(bbox.width * width)
                    h = int(bbox.height * height)
                    face_detected = True

        # If MediaPipe fails, try Haar Cascade
        if not face_detected:
            for scale in [1.02, 1.05, 1.08]:
                faces = self.haar_cascade.detectMultiScale(
                    gray_eq,
                    scaleFactor=scale,
                    minNeighbors=3,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE,
                )
                if len(faces) > 0:
                    faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
                    x, y, w, h = faces[0]
                    face_detected = True
                    break

        # If frontal detection fails, try profile face detection
        if not face_detected:
            for is_flipped in [False, True]:
                current_img = cv2.flip(gray_eq, 1) if is_flipped else gray_eq
                faces = self.profile_cascade.detectMultiScale(
                    current_img,
                    scaleFactor=1.05,
                    minNeighbors=2,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE,
                )
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    if is_flipped:
                        x = width - x - w
                    face_detected = True
                    break

        return (x, y, w, h) if face_detected else None
