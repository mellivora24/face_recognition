import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):

    # Lấy tất cả các file trong thư mục
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]

    #tao danh sach de chua cac khuon mat
    faceSamples=[]

    #Tao danh sach luu ID
    Ids=[]

    #Duyet tat ca cac hinh anh
    for imagePath in imagePaths:
        if (imagePath[-3:]=="jpg"):

            #Tai hinh anh va chuyen sang mau xam
            pilImage=Image.open(imagePath).convert('L')

            #Chuyen doi hinh anh thanh mang(dang so)
            imageNp=np.array(pilImage,'uint8')

            #Dua ra ID tu hinh anh
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces=detector.detectMultiScale(imageNp)

            #Phát hiện khuôn mặt trong khung hình và gán ID cho khuôn mặt đó
            for (x,y,w,h) in faces:
                faceSamples.append(imageNp[y:y+h,x:x+w])
                Ids.append(Id)
    return faceSamples,Ids

def Trainner():

    # Lấy các khuôn mặt và ID từ thư mục dataSet
    faceSamples,Ids = getImagesAndLabels('dataSet')

    # Train model để trích xuất đặc trưng các khuôn mặt và gán với từng học sinh
    recognizer.train(faceSamples, np.array(Ids))

    # Lưu model
    recognizer.save('recognizer/trainner.yml')
    print("Trích xuất đặc trưng thành công!")

