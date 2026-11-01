import cv2

from core.pose_detector import PoseDetector
from exercises.bicep_curl import BicepCurl

cap = cv2.VideoCapture(0)
detector = PoseDetector()
exercise = BicepCurl(side="left")   # right haath ke liye "right" likho

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Webcam se frame nahi mila")
        break

    frame = detector.find_pose(frame)
    exercise.update(detector)

    cv2.putText(frame, f"Reps: {exercise.reps}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(frame, f"Angle: {int(exercise.angle)}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(frame, f"Stage: {exercise.stage}", (10, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, exercise.feedback, (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    cv2.imshow("Bicep Curl (q = quit, r = reset)", frame)
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r'):
        exercise.reset()

cap.release()
cv2.destroyAllWindows()