# import tkinter as tk #for GUI
# import customtkinter as ck #enhancing UI

# import pandas as pd # data manipulation
# import numpy as np # data manipulation
# import pickle #loading model

# import mediapipe as mp #detecting pose
# import cv2 #take camera feed and perform computer vision tasks
# from PIL import Image, ImageTk  # working with images

# from landmarks import landmarks #loading landmarks

# # creating basic tkinter window
# window = tk.Tk()
# window.geometry("480x700")
# window.title("weight lift counter") 
# ck.set_appearance_mode("dark")

# #basic UI creation
# classLabel = ck.CTkLabel(window, height=40, font=("verdena", 12), 
#                         width=120 , text_color="black", padx=10)
# classLabel.place(x=10, y=1)
# classLabel.configure(text='STAGE') 

# counterLabel = ck.CTkLabel(window, height=40, font=("verdena", 12),
#                            width=120 , text_color="black", padx=10)
# counterLabel.place(x=160, y=1)
# counterLabel.configure(text='REPS') 

# probLabel  = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , 
#                          text_color="black", padx=10)
# probLabel.place(x=300, y=1)
# probLabel.configure(text='PROB') 

# classBox = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , text_color="black")
# classBox.place(x=10, y=41)
# classBox.configure(text='0') 

# counterBox = ck.CTkLabel(window, height=40, font=("verdena", 12),width=120 , text_color="black")
# counterBox.place(x=160, y=41)
# counterBox.configure(text='0') 

# probBox = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , text_color="black")
# probBox.place(x=300, y=41)
# probBox.configure(text='0') 

# # reset counter when reset button is pressed
# def reset_counter(): 
#     global counter
#     counter = 0 

# button = ck.CTkButton(window, text='RESET', command=reset_counter, 
#                       height=40, width=120 , text_color="white", fg_color="blue")
# button.place(x=10, y=600)

# #frame to show camera feed
# frame = tk.Frame(height=480, width=480)
# frame.place(x=10, y=90) 
# lmain = tk.Label(frame) 
# lmain.place(x=0, y=0) 

# #import drawing_utils module from the mediapipe library.
# #Drawing_utils provides utility functions for drawing landmarks and connections on images.
# mp_drawing = mp.solutions.drawing_utils

# # imports the pose module from the mediapipe library.
# # pose contains the Pose model used for human pose estimation.
# mp_pose = mp.solutions.pose

# # setting minimum confidence level for pose tracking
# pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5) 

# # loading pre-trained model in model variable

# with open('Rep-Tracker-Elite-main\deadlift.pkl', 'rb') as f: 
#     model = pickle.load(f) 

# Video = "final edit.mp4"
# #start video capturing and some variable initilizations
# cap = cv2.VideoCapture(0)
# current_stage = ''
# counter = 0 
# bodylang_prob = np.array([0,0]) 
# bodylang_class = '' 


# # main funtion
# def detect(): 
#     #importing variable in funtion
#     global current_stage
#     global counter
#     global bodylang_class
#     global bodylang_prob 

# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # if frame is read correctly ret is True
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # taking frame from video
#     # ret, frame = cap.read()
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

#     """
#     Pose landmarks are detected using the MediaPipe Pose model.
#     """
#     results = pose.process(image)
#     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
#         mp_drawing.DrawingSpec(color=(106,13,173), thickness=4, circle_radius = 5), 
#         mp_drawing.DrawingSpec(color=(255,102,0), thickness=5, circle_radius = 10)) 

#     try: 
#         #processing landmark and converting them into list for giving input to ML model
#         row = np.array([[res.x, res.y, res.z, res.visibility] 
#                         for res in results.pose_landmarks.landmark]).flatten().tolist()
        
#         # Pose landmarks are flattened into a row and converted into a 
#         # DataFrame for prediction.
#         X = pd.DataFrame([row], columns = landmarks) 
#        #The machine learning model predicts the probability of the current body language (up or down) 
#        #based on pose landmarks.
#         bodylang_prob = model.predict_proba(X)[0]
#         bodylang_class = model.predict(X)[0] 

#         if bodylang_class =="down" and bodylang_prob[bodylang_prob.argmax()] > 0.7: 
#             current_stage = "down" 
#         elif current_stage == "down" and bodylang_class == "up" and bodylang_prob[bodylang_prob.argmax()] > 0.7:
#             current_stage = "up" 
#             counter += 1 

#     except Exception as e: 
#         pass

#     #taking frame from camera, processing them and
#     # converting them to a format suitable to display in tkinter window
#     img = image[:, :460, :] 
#     imgarr = Image.fromarray(img) 
#     imgtk = ImageTk.PhotoImage(imgarr) 
#     lmain.imgtk = imgtk 
#     lmain.configure(image=imgtk)
#     lmain.after(10, detect)  

#     #updating results on screen
#     counterBox.configure(text=counter) 
#     probBox.configure(text=bodylang_prob[bodylang_prob.argmax()]) 
#     classBox.configure(text=current_stage) 

# detect() #calling detecting funtion
# window.mainloop() #continuously running mainloop

import tkinter as tk #for GUI
import customtkinter as ck #enhancing UI

import pandas as pd # data manipulation
import numpy as np # data manipulation
import pickle #loading model

import mediapipe as mp #detecting pose
import cv2 #take camera feed and perform computer vision tasks
from PIL import Image, ImageTk  # working with images

from landmarks import landmarks #loading landmarks

# creating basic tkinter window
window = tk.Tk()
window.geometry("480x700")
window.title("weight lift counter") 
ck.set_appearance_mode("dark")

#basic UI creation
classLabel = ck.CTkLabel(window, height=40, font=("verdena", 12), 
                        width=120 , text_color="black", padx=10)
classLabel.place(x=10, y=1)
classLabel.configure(text='STAGE') 

counterLabel = ck.CTkLabel(window, height=40, font=("verdena", 12),
                           width=120 , text_color="black", padx=10)
counterLabel.place(x=160, y=1)
counterLabel.configure(text='REPS') 

probLabel  = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , 
                         text_color="black", padx=10)
probLabel.place(x=300, y=1)
probLabel.configure(text='PROB') 

classBox = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , text_color="black")
classBox.place(x=10, y=41)
classBox.configure(text='0') 

counterBox = ck.CTkLabel(window, height=40, font=("verdena", 12),width=120 , text_color="black")
counterBox.place(x=160, y=41)
counterBox.configure(text='0') 

probBox = ck.CTkLabel(window, height=40, font=("verdena", 12), width=120 , text_color="black")
probBox.place(x=300, y=41)
probBox.configure(text='0') 

# reset counter when reset button is pressed
def reset_counter(): 
    global counter
    counter = 0 

button = ck.CTkButton(window, text='RESET', command=reset_counter, 
                      height=40, width=120 , text_color="white", fg_color="blue")
button.place(x=10, y=600)

#frame to show camera feed
frame = tk.Frame(height=480, width=480)
frame.place(x=10, y=90) 
lmain = tk.Label(frame) 
lmain.place(x=0, y=0) 

#import drawing_utils module from the mediapipe library.
#Drawing_utils provides utility functions for drawing landmarks and connections on images.
mp_drawing = mp.solutions.drawing_utils

# imports the pose module from the mediapipe library.
# pose contains the Pose model used for human pose estimation.
mp_pose = mp.solutions.pose

# setting minimum confidence level for pose tracking
pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5) 

# loading pre-trained model in model variable
with open('C:\Users\9254g\OneDrive\Desktop\MajorProject_main\Mini_project_Yoga-master\Rep-Tracker-Elite-main\Rep-Tracker-Elite-main\deadlift.pkl', 'rb') as f: 
    model = pickle.load(f) 

Video = "final edit.mp4"
#start video capturing and some variable initilizations
cap = cv2.VideoCapture(0)
current_stage = ''
counter = 0 
bodylang_prob = np.array([0,0]) 
bodylang_class = '' 


# main funtion
def detect(): 
    #importing variable in funtion
    global current_stage
    global counter
    global bodylang_class
    global bodylang_prob 

    # taking frame from video
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    """
    Pose landmarks are detected using the MediaPipe Pose model.
    """
    results = pose.process(image)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(106,13,173), thickness=4, circle_radius = 5), 
        mp_drawing.DrawingSpec(color=(255,102,0), thickness=5, circle_radius = 10)) 

    try: 
        #processing landmark and converting them into list for giving input to ML model
        row = np.array([[res.x, res.y, res.z, res.visibility] 
                        for res in results.pose_landmarks.landmark]).flatten().tolist()
        
        # Pose landmarks are flattened into a row and converted into a 
        # DataFrame for prediction.
        X = pd.DataFrame([row], columns = landmarks) 
       #The machine learning model predicts the probability of the current body language (up or down) 
       #based on pose landmarks.
        bodylang_prob = model.predict_proba(X)[0]
        bodylang_class = model.predict(X)[0] 

        if bodylang_class =="down" and bodylang_prob[bodylang_prob.argmax()] > 0.7: 
            current_stage = "down" 
        elif current_stage == "down" and bodylang_class == "up" and bodylang_prob[bodylang_prob.argmax()] > 0.7:
            current_stage = "up" 
            counter += 1 

    except Exception as e: 
        pass

    #taking frame from camera, processing them and
    # converting them to a format suitable to display in tkinter window
    img = image[:, :460, :] 
    imgarr = Image.fromarray(img) 
    imgtk = ImageTk.PhotoImage(imgarr) 
    lmain.imgtk = imgtk 
    lmain.configure(image=imgtk)
    lmain.after(10, detect)  

    #updating results on screen
    counterBox.configure(text=counter) 
    probBox.configure(text=bodylang_prob[bodylang_prob.argmax()]) 
    classBox.configure(text=current_stage) 

detect() #calling detecting funtion
window.mainloop() #continuously running mainloop
