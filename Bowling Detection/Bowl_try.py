'''
    While The Video Feed is one and at a specific moments it stops,
    PRess Q to move Frame By Frame in time and reach when the condition is,
    satisfied and the video resumes.
'''



import cv2
import mediapipe as mp
import numpy as np
import datetime


# The Function for Calculating Angles 
def calculate_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)

    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)

    if(angle>180.0):
        angle=360-angle
    return angle




mp_drawing=mp.solutions.drawing_utils
mp_pose=mp.solutions.pose

cap=cv2.VideoCapture("output.avi")
cap.set(3,640)
cap.set(4,480)
frames=cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps=cap.get(cv2.CAP_PROP_FPS)
print(frames)
print(fps)
counterfps=0
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    stage=None
    counter=0
    while cap.isOpened():
        ret,frame=cap.read()

        #Recolor Image
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable=True
        #Make Detection
        result=pose.process(image)

        #Recolor back to BGR
        image.flags.writeable=False
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        #Extract LandMarks
        try:
            landmarks=result.pose_landmarks.landmark
            # print(landmarks)
        except:
            pass

        # we have a map for working with different landmarks
        # for lndmrk in mp_pose.PoseLandmark:
        #     print(lndmrk)

        #We can get a specific land mark
        # print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])q

        #to get the index of the landmark of LEFT SHOULDER IN THIS INSTACNE
        # print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])

        '''
            Exracting The Shoulder X and Y corrdinate for calculating angle and we will repeat the steps for elbow and wrist.
        '''
        left_shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,]

        left_elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        left_wrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


        angle_for_hip=calculate_angle(left_shoulder,left_shoulder,left_elbow)

        #Calculating angle
        angle=calculate_angle(left_shoulder,left_elbow,left_wrist)


        #Render
        print(mp_pose.POSE_CONNECTIONS)
        mp_drawing.draw_landmarks(image,result.pose_landmarks,mp_pose.POSE_CONNECTIONS,mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),mp_drawing.DrawingSpec(color=(0,0,255),thickness=2,circle_radius=2))



        first_coor=(tuple(np.multiply(left_shoulder,[1280,720]).astype(int)))
        sec_coor=(tuple(np.multiply(left_wrist,[1280,720]).astype(int)))

        if counter> 316 and counter<331:
            if(angle>200):
                pass
            else:
                cv2.line(image,(first_coor[0],first_coor[1]),(sec_coor[0],sec_coor[1]),(255,0,0),2)

                cv2.putText(image,f"Current angle is {angle}",(100,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
                cv2.imshow("Mediapipe Feed",image)
                cv2.waitKey(0)

            # cv2.putText(image,str(angle),tuple(np.multiply(left_elbow,[1280,720]).astype(int)),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,123),1,cv2.LINE_AA)


            # cv2.putText(image,str(angle_for_hip),tuple(np.multiply(left_shoulder,[640,480]).astype(int)),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,123),1,cv2.LINE_AA)

            
        else:
            cv2.imshow("Mediapipe Feed",image)
        if(cv2.waitKey(1) & 0xFF== ord('q')):
            break

        counter+=1
        # print(counter)
    cap.release()
    cv2.destroyAllWindows()

# print(counter)


##320-330