# not working

import cv2
import time
import practicess11 as pr
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
bTime = 0

detector = pr.poseDetector()
count = 0  # To count the number of reps
direction_r = 0  # Right arm direction (0 = down, 1 = up)
direction_l = 0  # Left arm direction (0 = down, 1 = up)

while True:
    success, image = cap.read()
    image = cv2.resize(image, (1280, 720))
    image = cv2.flip(image, 2)
    image = detector.findPose(image, False)
    lmList = detector.findPosition(image, False)

    if len(lmList) != 0:
        # Right arm reverse fly angle (shoulder -> elbow -> wrist)
        arm_r = detector.findAngle(image, 12, 14, 16)  # Right shoulder, elbow, wrist
        # Left arm reverse fly angle (shoulder -> elbow -> wrist)
        arm_l = detector.findAngle(image, 11, 13, 15)  # Left shoulder, elbow, wrist

        # Interpolating angles to percentages for the reverse fly motion
        per_r = np.interp(arm_r, (45, 160), (0, 100))  # Right arm (0-100%)
        per_l = np.interp(arm_l, (45, 160), (0, 100))  # Left arm (0-100%)

        # Right arm reverse fly movement tracking
        if per_r == 100:  # Arm fully raised
            if direction_r == 0:  # Was moving up
                count += 0.5  # Half rep (up)
                direction_r = 1  # Now moving down
        if per_r == 0:  # Arm fully lowered
            if direction_r == 1:  # Was moving down
                count += 0.5  # Half rep (down)
                direction_r = 0  # Now moving up

        # Left arm reverse fly movement tracking
        if per_l == 100:  # Arm fully raised
            if direction_l == 0:  # Was moving up
                count += 0.5  # Half rep (up)
                direction_l = 1  # Now moving down
        if per_l == 0:  # Arm fully lowered
            if direction_l == 1:  # Was moving down
                count += 0.5  # Half rep (down)
                direction_l = 0  # Now moving up

        # Display the rep count
        print(f"Count: {int(count)}")
        cv2.rectangle(image, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, str(int(count)), (40, 670), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 13)

        # Visual feedback for the reverse fly motion
        color_r = (0, 255, 0) if direction_r == 1 else (255, 0, 0)
        color_l = (0, 255, 0) if direction_l == 1 else (255, 0, 0)

        # Draw progress bars for each arm
        cv2.rectangle(image, (1100, 100), (1175, 400), color_r, 3)  # Right arm bar
        cv2.rectangle(image, (1100, int(400 - (per_r * 3))), (1175, 400), color_r, cv2.FILLED)

        cv2.rectangle(image, (50, 100), (125, 400), color_l, 3)  # Left arm bar
        cv2.rectangle(image, (50, int(400 - (per_l * 3))), (125, 400), color_l, cv2.FILLED)

        # Display the angles on the image for reference
        cv2.putText(image, f'{int(arm_r)} deg', (1100, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(image, f'{int(arm_l)} deg', (50, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Calculate and display FPS
    nTime = time.time()
    fps = 1 / (nTime - bTime)
    bTime = nTime
    cv2.putText(image, f"FPS: {int(fps)}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)

    # Display the video feed
    cv2.imshow("Reverse Flies", image)
    if cv2.waitKey(5) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
