from collections import deque

from core.pose_detector import (
    LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST,
    RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST,
)
from core.utils import calculate_angle


class BicepCurl:
    name = "Bicep Curl"

    DOWN_ANGLE = 160   # isse zyada = haath neeche (seedha)
    UP_ANGLE = 40      # isse kam = haath upar (mudha hua)

    def __init__(self, side="left"):
        self.side = side
        self.reps = 0
        self.stage = "down"
        self.feedback = "Start curling"
        self.angle = 0
        self.history = deque(maxlen=5)   # angle ko smooth karne ke liye

    def reset(self):
        self.reps = 0
        self.stage = "down"
        self.feedback = "Start curling"
        self.angle = 0
        self.history.clear()

    def update(self, detector):
        """Har frame par call hota hai. Angle nikalta hai aur reps update karta hai."""
        if self.side == "left":
            ids = (LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
        else:
            ids = (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)

        shoulder = detector.get_point(ids[0])
        elbow = detector.get_point(ids[1])
        wrist = detector.get_point(ids[2])

        if not (shoulder and elbow and wrist):
            self.feedback = "Body not visible"
            return self.angle

        raw_angle = calculate_angle(shoulder, elbow, wrist)
        self.history.append(raw_angle)
        self.angle = sum(self.history) / len(self.history)

        # Rep counting (state machine)
        # Rep counting (state machine)
        if self.angle > self.DOWN_ANGLE:
            self.stage = "down"
            self.feedback = "Curl up!"
        elif self.angle < self.UP_ANGLE and self.stage == "down":
            self.stage = "up"
            self.reps += 1
            self.feedback = "Good! Now lower slowly"
        elif self.stage is None:
            self.feedback = "Straighten your arm to start"
        elif self.stage == "down":
            self.feedback = "Keep going up"