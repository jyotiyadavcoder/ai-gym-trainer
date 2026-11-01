import cv2
from core.pose_detector import PoseDetector, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST
from core.utils import calculate_angle

cap = cv2.VideoCapture(0)
detector = PoseDetector()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Webcam se frame nahi mila")
        break

    frame = detector.find_pose(frame)

    shoulder = detector.get_point(LEFT_SHOULDER)
    elbow = detector.get_point(LEFT_ELBOW)
    wrist = detector.get_point(LEFT_WRIST)

    if shoulder and elbow and wrist:
        angle = calculate_angle(shoulder, elbow, wrist)
        cv2.putText(frame, f"Elbow angle: {int(angle)}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Pose Test (q = quit)", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()