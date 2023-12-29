
#--------------------------package import-------------------------------
import os
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image,ImageTk
import sqlite3
import csv
#import Attendance_code
username_entry = None
password_entry = None
root = None  # Declare root as a global variable

# Create SQLite database and table if they don't exist
conn = sqlite3.connect("Attendance.db")
cursor = conn.cursor()

#---------------------------Attendance-Camera------------------------------
#def attendance():
   # Attendance_code.runAttendence_code
#---------------------------escape-button function------------------------------
def quit(*args):
     root.destroy()
#---------------------------Main-Frame-------------------------------
root = Tk()
root.geometry("600x600")
#root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("<Escape>", quit)
root.bind("x", quit)

f1=Frame()
f1.place(x=0,y=0,width=1200,height=700)
#---------------------------registration window-----------------------------
def registration():
    frame=Frame(root)
    frame.place(x=0,y=0,width=1200,height=700)
    background_label = Label(frame, image=background_photo)
    background_label.place(x=0,y=0,width=1200,height=700)

    un=Label(frame, text="Username:",font=("Arial", 13))
    un.place(x=300,y=200)
    em=Label(frame, text="Email:",font=("Arial", 13)) 
    em.place(x=300,y=300) 
    up=Label(frame, text="Password:",font=("Arial", 13))
    up.place(x=300,y=400)

    username_entry = Entry(frame,font=("Arial", 13))
    username_entry.place(x=450,y=200,width=140,height=20)
    email_entry = Entry(frame,font=("Arial", 13))
    email_entry.place(x=450,y=300,width=140,height=20)
    password_entry = Entry(frame, show="*",font=("Arial", 13))
    password_entry.place(x=450,y=400,width=140,height=20)
    button2 = Button(frame, text="Back",command=lambda: destroy_frame(frame))
    button2.place(x=300,y=600,width=120,height=60)
    label_entry = Label(frame, text="Enter Image Name:")
    label_entry.place(x=300,y=500)

    entry_name = Entry(frame)
    entry_name.place(x=450,y=500,width=140,height=20)

    #register data setting
    
    #register 

    button_capture = Button(frame, text="Capture and Save", command=lambda: capture_and_save(entry_name))
    button_capture.place(x=600,y=500,width=150,height=60)
    def create_table(cursor):
        try:
            cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
            conn.commit()
            print("Table 'users' created successfully.")
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return False


    def register_user():
        #global conn, cursor
    # Get values from entry widgets
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

    # Validate the input
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields must be filled out")
            return

    # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE name=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

    # Insert user data into the SQLite database
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            print("User registered successfully.")
            messagebox.showinfo("Registration Successful", "User registered successfully!")

        # Open the login module after successful registration
            #open_login_window(username)

        except sqlite3.Error as e:
            print("SQLite error:", e)
            messagebox.showerror("Error", "Failed to register user")

# Create SQLite database and table if they don't exist
        #conn = sqlite3.connect("Attendance.db")
        #cursor = conn.cursor()

# Create the table (if not already created)
        create_table(cursor)


    button3 = Button(frame, text="Register",command=register_user )
    button3.place(x=780,y=500,width=120,height=60)
    
#---------------------------back-to-home--------------------------
def destroy_frame(frame):
    # Destroy the current frame to switch back to the home screen
    frame.destroy()
    home()     
#---------------------------capture to register-------------------------
def capture_and_save(entry_name):
    # Open a video capture object (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()

    # Release the video capture object
    cap.release()

    if ret:
        # Specify the folder path to save the image
        folder_path = r'E:\pythondemo\MLProject\AttendanceProject\images1'

        # Construct the file path to save the image
        file_name = entry_name.get()
        if not file_name:
            file_name = "captured_image"

        file_path = os.path.join(folder_path, f"{file_name}.png")

        # Save the image
        cv2.imwrite(file_path, frame)

        print(f"Image saved to: {file_path}")
        messagebox.showinfo("Success", "Image successfully captured and saved!")

    else:
        print("Failed to capture image.")


background_image = Image.open('E:\pythondemo\MLProject\AttendanceProject\img1.png')
background_photo = ImageTk.PhotoImage(background_image)
#---------------------------Login-window---------------------------
def addOPC(frame2):    
    opcam = Button(frame2, text="Open Camera", font=('', '14'), bg='white', fg='black', borderwidth=2, padx=5, pady=5, command=OpenCam)
    opcam.place(x=780,y=200,width=120,height=60)

def login():
    def user_login_db():
        username = username_entry.get()
        password = password_entry.get()

        # Validate the input
        if not username or not password: 
            messagebox.showerror("Error", "Both username and password are required")
            return

        # Check if the provided username and password exist in the database
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            messagebox.showinfo("Login Successful", "Welcome, {}!".format(username))
            addOPC(frame)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    # Add your actual login logic here
            # For simplicity, let's assume a successful login for any input
            return True
    frame=Frame(root)
    frame.place(x=0,y=0,width=1200,height=700)
    background_label = Label(frame, image=background_photo)
    background_label.place(x=0,y=0,width=1200,height=700)

    un=Label(frame, text="Username:",font=("Arial", 13))
    un.place(x=300,y=200)
    up=Label(frame, text="Password:",font=("Arial", 13))
    up.place(x=300,y=250)
    username_entry = Entry(frame,font=("Arial", 13))
    username_entry.place(x=450,y=200,width=140,height=20)
    password_entry = Entry(frame, show="*",font=("Arial", 13))
    password_entry.place(x=450,y=250,width=140,height=20)
    #login_btn = Button(frame, text="login",command=Attendance_code.runAttendence_code)
    login_btn = Button(frame, text="login", command=user_login_db)
    login_btn.place(x=650,y=200,width=120,height=60)
    button2 = Button(frame, text="Back",command=lambda: destroy_frame(frame))
    button2.place(x=300,y=600,width=120,height=60)
        
    '''def check_login(frame):
        if actual_login_function():
            messagebox.showinfo("Login Successful", "Welcome!")
            frame.destroy()  # Close the login window
            Attendance_code.runAttendence_code()'''

    


#---------------------------Home-window---------------------------
def OpenCam():
    images = []
    path = 'E:\pythondemo\MLProject\AttendanceProject\images1'
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    #def markAttendance(name):
    def markAttendance(name):
    # Specify the path to your CSV file
        file_path = r'E:\pythondemo\MLProject\AttendanceProject\Ettendance.csv'

    # Read existing data from the file
        with open(file_path, 'r') as f:
             myDataList = f.readlines()

    # Get the current date and time
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        time_string = now.strftime('%H:%M:%S')

    # Check if there is an existing entry for the current date and name
        existing_entry = any(f'{name},{date_string}' in line for line in myDataList)

        if existing_entry:
        # If an entry exists, update the exit time if the gap is at least 6 hours
            for i, line in enumerate(myDataList):
                if f'{name},{date_string}' in line:
                    entry_time_str = line.split(',')[2].strip()
                    entry_time = datetime.strptime(entry_time_str, '%H:%M:%S')
                    time_difference = now - entry_time

                    if time_difference >= timedelta(hours=6):
                    # Update the exit time
                        myDataList[i] = f'{name},{date_string},{time_string},{entry_time_str}\n'
                    else:
                        print(f'Error: Exit time cannot be marked within 6 hours of entry for {name} on {date_string}.')
        else:
            # If no existing entry, add a new entry
            with open(file_path, 'a') as f:
                f.write(f'{name},{date_string},{time_string},,\n')  # Initialize Exit column with an empty value

    def markAttendance(name):
        with open('E:\pythondemo\MLProject\AttendanceProject\Ettendance.csv', 'r') as f:
            myDataList = f.readlines()

    # Check if there is an existing entry for the current date
        now = datetime.now()
        date_string = now.strftime('%Y-%m-%d')
        existing_entry = any(f'{name},{date_string}' in line for line in myDataList)

    # If no existing entry, add a new one
        if not existing_entry:
            with open('E:\pythondemo\MLProject\AttendanceProject\Ettendance.csv', 'a') as f:
                time_string = now.strftime('%H:%M:%S')
                f.write(f'\n{name},{date_string},{time_string}')
    

    encodeListKnown = findEncoding(images)
    print('Encoding Complete')

    # Create a tkinter window for displaying video feed
    video_window = Toplevel(root)
    video_window.title("Video Feed")
    video_frame = Label(video_window)
    video_frame.pack()

    cap = cv2.VideoCapture(0)
    
    while True:
        success, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1, x1, y2, x2 = faceLoc
                y1, x1, y2, x2 = y1 * 4, x1 * 4, y2 * 4, x2 * 4
                cv2.rectangle(img, (x1, y2), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        # Convert the OpenCV image to a format suitable for tkinter
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (800, 600))
        photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        video_frame.config(image=photo)
        video_frame.photo = photo
        root.update()

#---------------------------face-recognition---------------------------
def home():

    background_label = Label(f1, image=background_photo)
    background_label.place(x=0,y=0,width=1200,height=700)
    root.title("MARK YOUR ATTENDANCE")
    root.geometry('1200x700')

    reg_btn= Button(f1, text="register",command=registration)
    reg_btn.place(x=550,y=200,width=120,height=60)
    login_btn = Button(f1, text="login",command=login)
    login_btn.place(x=650,y=200,width=120,height=60)
    



home()
root.mainloop()