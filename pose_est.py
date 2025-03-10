import cv2
import numpy as np

# Load the predefined dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)

# Load the detector parameters
parameters = cv2.aruco.DetectorParameters()

# Your camera calibration data
camera_matrix = np.array([[782.60463393,   0.,         324.90380285],
                          [  0.  ,       792.77890853, 196.10454981],
                          [  0.   ,        0.  ,         1.        ]], dtype=np.float32)

dist_coeffs = np.array([-1.03967761e+00,  1.60002918e+01, -1.53119948e-02,  1.94590094e-02, -7.84282284e+01], dtype=np.float32)

# Start capturing video from the webcam
cap = cv2.VideoCapture(2)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Estimate the pose of each marker
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_coeffs)

        for i in range(len(ids)):
            # Draw the detected marker and its axis
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)

    # Display the resulting frame
    cv2.imshow('ArUco Marker Pose Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()