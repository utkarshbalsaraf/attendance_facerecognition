import cv2
import face_recognition
import pickle
import os
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

# imported student images
FolderPath = 'image'
PathList = os.listdir(FolderPath)
imgList = []
studentID = []
# split by id and picture format then isert into studentID
for path in PathList:
    imgList.append(cv2.imread(os.path.join(FolderPath, path)))
    studentID.append(os.path.splitext(path)[0])

    # when encoding known images we will also uplode them to database using bucket and blob
    fileName = f'{FolderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(len(imgList))


# finding encodes of images in 128 codes using face_recognition in loop
def findEncodings(EncdImgList):
    encodeList = []
    for img in EncdImgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# encoding known images for validation
print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownwithId = [encodeListKnown, studentID]
print("Encoding Complete...")
print(len(encodeListKnown))

# creating file and inserting the data of students
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownwithId, file)
file.close()
print("file saved")
