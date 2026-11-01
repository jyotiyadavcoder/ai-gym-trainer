import time
import threading

import cv2

from core.pose_detector import PoseDetector
from exercises.bicep_curl import BicepCurl
from exercises.squat import Squat
from exercises.pushup import PushUp

EXERCISES = {
    "bicep_curl": BicepCurl,
    "squat": Squat,
    "pushup": PushUp,
}


class VideoStream:
    def __init__(self):
        self.running = False
        self.exercise = None
        self.start_time = None
        self.lock = threading.Lock()

    def start(self, exercise_key="bicep_curl", side="left"):
        exercise_class = EXERCISES.get(exercise_key, BicepCurl)
        if side not in ("left", "right"):
            side = "left"
        with self.lock:
            self.exercise = exercise_class(side=side)
            self.start_time = time.time()
            self.running = True

    def stop(self):
        """Workout rokta hai aur uska result deta hai."""
        with self.lock:
            if not self.running or self.exercise is None:
                return None
            self.running = False
            return {
                "exercise": self.exercise.name,
                "reps": self.exercise.reps,
                "duration": int(time.time() - self.start_time),
            }

    def stats(self):
        if not self.running or self.exercise is None:
            return {"running": False, "reps": 0, "stage": "-",
                    "feedback": "Press Start", "angle": 0, "elapsed": 0}
        return {
            "running": True,
            "reps": self.exercise.reps,
            "stage": self.exercise.stage or "-",
            "feedback": self.exercise.feedback,
            "angle": int(self.exercise.angle),
            "elapsed": int(time.time() - self.start_time),
        }

    def frames(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        detector = PoseDetector()

        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = detector.find_pose(frame)
                self.exercise.update(detector)

                ok, buffer = cv2.imencode(".jpg", frame)
                if not ok:
                    continue
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")
        finally:
            cap.release()