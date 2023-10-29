import numpy as np

import cv2
import mediapipe

def calculate_angle(a, b, c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    
    return angle


cap = cv2.VideoCapture(0)

mp_pose = mediapipe.solutions.pose
mp_drawing = mediapipe.solutions.drawing_utils

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
count = 0
flag = 0
while True:
  ret, image = cap.read()

  results = pose.process(image)

  try:
    landmarks = results.pose_landmarks.landmark
    l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    if (l_shoulder and l_elbow and l_wrist):
        print(l_shoulder, l_elbow, l_wrist)
        angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
        print(angle)
        if angle > 150:
            flag = 1
        if flag == 1 and angle < 50:
            count += 1
            flag = 0
        if count == 5:
           print("5 curls")
           exit()


  except Exception as e:
    pass
  mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(456666, thickness=2, circle_radius=2),  mp_drawing.DrawingSpec(334343, thickness=2, circle_radius=2)) 
  mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
  mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
  cv2.imshow('MediaPipe Pose', image) 
  if cv2.waitKey(10) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
