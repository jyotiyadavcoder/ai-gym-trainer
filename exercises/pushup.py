import time
from collections import deque

from core.pose_detector import (
    LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, LEFT_HIP, LEFT_ANKLE,
    RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST, RIGHT_HIP, RIGHT_ANKLE,
)
from core.utils import calculate_angle


class PushUp:
    name = "Push-up"

    UP_ANGLE = 160        # isse zyada = haath seedhe (upar)
    DOWN_ANGLE = 90       # isse kam = neeche
    MIN_BODY_ANGLE = 150  # isse kam = kamar jhuki hui

    def __init__(self, side="left"):
        self.side = side
        self.history = deque(maxlen=5)
        self.reset()

    def reset(self):
        self.reps = 0
        self.stage = None
        self.feedback = "Get in plank position"
        self.angle = 0
        self.last_rep_time = 0
        self.history.clear()

    def update(self, detector):
        if self.side == "left":
            ids = (LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, LEFT_HIP, LEFT_ANKLE)
        else:
            ids = (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST, RIGHT_HIP, RIGHT_ANKLE)

        shoulder = detector.get_point(ids[0])
        elbow = detector.get_point(ids[1])
        wrist = detector.get_point(ids[2])
        hip = detector.get_point(ids[3])
        ankle = detector.get_point(ids[4])

        if not (shoulder and elbow and wrist):
            self.feedback = "Arm not visible"
            return self.angle

        self.history.append(calculate_angle(shoulder, elbow, wrist))
        self.angle = sum(self.history) / len(self.history)

        if self.angle > self.UP_ANGLE:
            self.stage = "up"
            self.feedback = "Lower your body"
        elif (self.angle < self.DOWN_ANGLE and self.stage == "up"
              and time.time() - self.last_rep_time > 0.5):
            self.stage = "down"
            self.reps += 1
            self.last_rep_time = time.time()
            self.feedback = "Good! Push back up"
        elif self.stage is None:
            self.feedback = "Straighten your arms to start"
        elif self.stage == "up":
            self.feedback = "Go lower"

        # Form check: shareer seedhi line me hona chahiye
        if hip and ankle:
            body_angle = calculate_angle(shoulder, hip, ankle)
            if body_angle < self.MIN_BODY_ANGLE:
                self.feedback = "Keep your body straight"

        return self.angle