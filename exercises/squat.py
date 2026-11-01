import time
from collections import deque

from core.pose_detector import (
    LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE, LEFT_ANKLE,
    RIGHT_SHOULDER, RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE,
)
from core.utils import calculate_angle, angle_from_vertical


class Squat:
    name = "Squat"

    STAND_ANGLE = 160     # isse zyada = khade hain
    SQUAT_ANGLE = 100     # isse kam = squat poora
    MAX_BACK_LEAN = 60    # isse zyada jhuke to warning

    def __init__(self, side="left"):
        self.side = side
        self.history = deque(maxlen=5)
        self.reset()

    def reset(self):
        self.reps = 0
        self.stage = None
        self.feedback = "Stand straight to start"
        self.angle = 0
        self.last_rep_time = 0
        self.history.clear()

    def update(self, detector):
        if self.side == "left":
            ids = (LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE, LEFT_ANKLE)
        else:
            ids = (RIGHT_SHOULDER, RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE)

        shoulder = detector.get_point(ids[0])
        hip = detector.get_point(ids[1])
        knee = detector.get_point(ids[2])
        ankle = detector.get_point(ids[3])

        if not (hip and knee and ankle):
            self.feedback = "Full body not visible"
            return self.angle

        self.history.append(calculate_angle(hip, knee, ankle))
        self.angle = sum(self.history) / len(self.history)

        if self.angle > self.STAND_ANGLE:
            self.stage = "up"
            self.feedback = "Squat down"
        elif (self.angle < self.SQUAT_ANGLE and self.stage == "up"
              and time.time() - self.last_rep_time > 0.8):
            self.stage = "down"
            self.reps += 1
            self.last_rep_time = time.time()
            self.feedback = "Good depth! Stand up"
        elif self.stage is None:
            self.feedback = "Stand straight to start"
        elif self.stage == "up":
            self.feedback = "Go lower"

        # Form check: back bahut jhuka hua
        if shoulder and self.angle < 150:
            if angle_from_vertical(shoulder, hip) > self.MAX_BACK_LEAN:
                self.feedback = "Keep your chest up"

        return self.angle