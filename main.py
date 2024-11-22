import cv2
import mediapipe as mp
import time
import serial

# Initialize Serial communication (adjust COM port and baud rate as needed)
arduino = serial.Serial('COM3', 9600, timeout=1)

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
blink_threshold = 0.25  # Threshold for eye aspect ratio
closed_time_limit = 5   # Seconds to trigger alert

# Helper function to calculate eye aspect ratio
def calculate_aspect_ratio(landmarks, indices):
    left_point = landmarks[indices[0]]
    right_point = landmarks[indices[1]]
    top_point = landmarks[indices[2]]
    bottom_point = landmarks[indices[3]]

    horizontal_distance = ((right_point.x - left_point.x) ** 2 + (right_point.y - left_point.y) ** 2) ** 0.5
    vertical_distance = ((top_point.x - bottom_point.x) ** 2) ** 0.5

    return vertical_distance / horizontal_distance

# Webcam setup
cap = cv2.VideoCapture(0)
closed_start_time = None

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame horizontally for a natural selfie view
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract eye landmarks
                left_eye = [33, 133, 159, 145]  # Change these based on your framework
                right_eye = [362, 263, 386, 374]  # Adjust as needed

                left_ratio = calculate_aspect_ratio(face_landmarks.landmark, left_eye)
                right_ratio = calculate_aspect_ratio(face_landmarks.landmark, right_eye)

                avg_ratio = (left_ratio + right_ratio) / 2

                if avg_ratio < blink_threshold:
                    if closed_start_time is None:
                        closed_start_time = time.time()
                    elif time.time() - closed_start_time >= closed_time_limit:
                        print("Eyes closed for too long! Triggering alert.")
                        arduino.write(b'ALERT\n')
                else:
                    closed_start_time = None
                    arduino.write(b'RESET\n')  # Reset alert state
        cv2.imshow("Driver Monitoring", frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Exiting...")

cap.release()
cv2.destroyAllWindows()
arduino.close()
