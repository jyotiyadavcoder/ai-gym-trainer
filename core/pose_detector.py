import cv2
import mediapipe as mp

# Body ke joints ke number (MediaPipe me 33 points hote hain)
LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
LEFT_ELBOW, RIGHT_ELBOW = 13, 14
LEFT_WRIST, RIGHT_WRIST = 15, 16
LEFT_HIP, RIGHT_HIP = 23, 24
LEFT_KNEE, RIGHT_KNEE = 25, 26
LEFT_ANKLE, RIGHT_ANKLE = 27, 28


class PoseDetector:
    def __init__(self, detection_conf=0.5, tracking_conf=0.5):
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.results = None

    def find_pose(self, frame, draw=True):
        """Frame me body detect karta hai aur skeleton draw karta hai."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(rgb)
        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(
                frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS
            )
        return frame

    def get_point(self, index, min_visibility=0.6):
        """Ek joint ka [x, y] deta hai. Joint saaf na dikhe to None."""
        if self.results and self.results.pose_landmarks:
            lm = self.results.pose_landmarks.landmark[index]
            if lm.visibility < min_visibility:
                return None
            return [lm.x, lm.y]
        return None