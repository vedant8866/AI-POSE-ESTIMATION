# import cv2
# import time
# import practicess11 as pr
# import numpy as np

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# bTime = 0

# detector = pr.poseDetector()
# count = 0
# rep_up = 0

# while True:
#     success, image = cap.read()
#     if not success:
#         break
#     image = cv2.resize(image, (1280, 720))
#     image = cv2.flip(image, 1)  # Flip the image horizontally for a mirror view
#     image = detector.findPose(image, False)
#     lmList = detector.findPosition(image, False)

#     if len(lmList) != 0:
#         # Detect angles at the elbows for bicep curls
#         angle_r = detector.findAngle(image, 12, 14, 16)  # Right arm (shoulder, elbow, wrist)
#         angle_l = detector.findAngle(image, 11, 13, 15)  # Left arm (shoulder, elbow, wrist)

#         # Interpolate the angles to get a percentage value
#         per_r = np.interp(angle_r, (60, 160), (100, 0))  # Right arm
#         per_l = np.interp(angle_l, (60, 160), (100, 0))  # Left arm

#         # Check if the arms are fully curled or fully extended
#         if per_r == 100 and per_l == 100:
#             color = (255, 0, 255)
#             if rep_up == 0:
#                 count += 0.5
#                 rep_up = 1
#         if per_r == 0 and per_l == 0:
#             color = (0, 255, 0)
#             if rep_up == 1:
#                 count += 0.5
#                 rep_up = 0

#         # Display the count
#         cv2.rectangle(image, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
#         cv2.putText(image, str(int(count)), (40, 670), cv2.FONT_HERSHEY_PLAIN, 10,
#                     (255, 0, 0), 13)

#     nTime = time.time()
#     fps = 1 / (nTime - bTime)
#     bTime = nTime
#     cv2.putText(image, f"FPS: {int(fps)}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
#     cv2.imshow("Bicep Curl Counter", image)

#     if cv2.waitKey(5) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import time
import practicess11 as pr
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
bTime = 0

detector = pr.poseDetector()
count = 0  # To count the number of reps
rep_up = 0  # To keep track of whether the arm is moving up or down
direction_r = 0  # Right arm direction (0 = down, 1 = up)
direction_l = 0  # Left arm direction (0 = down, 1 = up)

while True:
    success, image = cap.read()
    image = cv2.resize(image, (1280, 720))
    image = cv2.flip(image, 2)
    image = detector.findPose(image, False)
    lmList = detector.findPosition(image, False)

    if len(lmList) != 0:
        # Right arm (Bicep Curl) angle
        arm_r = detector.findAngle(image, 12, 14, 16)
        # Left arm (Bicep Curl) angle
        arm_l = detector.findAngle(image, 11, 13, 15)

        # Interpolating angles to percentages for the bicep curl motion
        per_r = np.interp(arm_r, (50, 160), (100, 0))  # Right arm (0-100%)
        per_l = np.interp(arm_l, (50, 160), (100, 0))  # Left arm (0-100%)

        # Right arm bicep curl movement tracking
        if per_r == 100:  # Arm fully extended
            if direction_r == 1:  # Was moving up before
                count += 0.5  # Half rep (down)
                direction_r = 0  # Now moving down
        if per_r == 0:  # Arm fully flexed
            if direction_r == 0:  # Was moving down before
                count += 0.5  # Half rep (up)
                direction_r = 1  # Now moving up

        # Left arm bicep curl movement tracking (optional, remove if not needed)
        if per_l == 100:  # Arm fully extended
            if direction_l == 1:  # Was moving up before
                count += 0.5  # Half rep (down)
                direction_l = 0  # Now moving down
        if per_l == 0:  # Arm fully flexed
            if direction_l == 0:  # Was moving down before
                count += 0.5  # Half rep (up)
                direction_l = 1  # Now moving up

        # Displaying the rep count
        print(f"Count: {int(count)}")
        cv2.rectangle(image, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(image, str(int(count)), (40, 670), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 13)

        # Visual feedback for the curl motion
        color_r = (0, 255, 0) if direction_r == 1 else (255, 0, 0)
        color_l = (0, 255, 0) if direction_l == 1 else (255, 0, 0)

        # Draw progress bars for each arm
        cv2.rectangle(image, (1100, 100), (1175, 400), color_r, 3)
        cv2.rectangle(image, (1100, int(400 - (per_r * 3))), (1175, 400), color_r, cv2.FILLED)

        cv2.rectangle(image, (50, 100), (125, 400), color_l, 3)
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
    cv2.imshow("Bicep Curls", image)
    if cv2.waitKey(5) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
