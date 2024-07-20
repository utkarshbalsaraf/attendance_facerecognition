import os
import pickle
import bbox
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# creating and connecting the database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "enter your",
    'storageBucket': "enter your"
})

bucket = storage.bucket()

# WebCam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# imported baground
imgBackground = cv2.imread('Resources/background.png')

# imported mode images
FolderModePath = 'Resources/Modes'
modePathList = os.listdir(FolderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(FolderModePath, path)))

# load the encoded file
print("Loading encoded file")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentID = encodeListKnownWithIds
print("encoded file loaded")

modeType = 0
counter = 0
id = -1
imgStud = []

# main loop
while True:
    success, img = cap.read()
    # resizing live images
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # converting video frames fron cv format to face_recognition format
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # finding the face location
    fcurrentFrm = face_recognition.face_locations(imgS)
    # finding encodings of current video frames
    encodeCurrentFrm = face_recognition.face_encodings(imgS, fcurrentFrm)

    # inserting Background and WebCam and Mode Images
    # background
    imgBackground[162:162 + 480, 55:55 + 640] = img
    # mode images
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if fcurrentFrm:#for coming back to active mode if there is no face
    # matching the encoding of current frame to the known face list
        for encodeFace, faceLoc in zip(encodeCurrentFrm, fcurrentFrm):
            # face matching
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            # distance matching , lower distance is better
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("matches", matches)


            # getting the index of matched person
            matchIndex = np.argmin(faceDist)

            # getting the ID of matched person
            if matches[matchIndex]:

                # creating real time face detection box using cvzone and bbox
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                # creating conditions to show desired mode
                id = studentID[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"LOADING",(275,400))
                    cv2.imshow("Face Recognition", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

            if counter != 0:
                if counter == 1:
                    # retrieving and showing info of an ID if it's a match
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    # retrieving image of the matched student
                    blob = bucket.get_blob(f'image/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStud = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    # updating Attendance
                    datetimeObj = datetime.strptime(studentInfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
                    secondElps = (datetime.now()-datetimeObj).total_seconds()

                    if secondElps > 60:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:
                # changing mode to mark after attendance has been taken
                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['Course']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    # centering the name unconditional of its length
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # inserting image
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStud   

                counter += 1

                # after attendance is marked the page will go to first page
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStud = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # webcam
    cv2.imshow("Face Recognition", imgBackground)
    cv2.waitKey(1)

