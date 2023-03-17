import cv2
import sqlite3
import trainner

camera = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Hàm cập nhật tên và ID vào CSDL
def insert(id, name, clas):

    #Kết nối với CSDL:
    conn = sqlite3.connect("STUDENT.db")
    cursor = conn.cursor()

    #Kiểm tra xem bảng dữ liệu của lớp đã tồn tại hay chưa, nếu chưa tạo mới:
    tableName = "CLASS"
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (tableName,))

    if cursor.fetchone():
        #Thêm dữ liệu học sinh vào trong Database
        cmd="INSERT INTO " + tableName + "(STT,NAME, CLASS) Values("+str(id)+",' "+str(name)+" ',' "+str(clas)+" ' )"
        conn.execute(cmd)
        conn.commit()
    else:
        cmd = "CREATE TABLE " + tableName + "(STT integer NOT NULL, NAME text NOT NULL, CLASS text NOT NULL);"
        cursor.execute(cmd)
        conn.commit()
        #Thêm dữ liệu học sinh vào trong Database
        cmd="INSERT INTO " + tableName + "(STT,NAME, CLASS) Values("+str(id)+",' "+str(name)+" ',' "+str(clas)+" ' )"
        conn.execute(cmd)
        conn.commit()
    conn.close()

clas = input('Nhập lớp: ')

while  True:

    sampleNum = 0
    id = input('Nhập số thứ tự của học sinh trong lớp học: ')
    if id == 'q':
        break
    name = input('Nhập tên hoc sinh: ')

    insert(id,name, clas)

    _, img = camera.read()

    while sampleNum <= 50:

        # Đưa ảnh về ảnh xám:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Nhận diện khuôn mặt:
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # Vẽ hình chữ nhật quanh mặt nhận được:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Ghi dữ liệu khuôn mặt vào thư mục dataSet:
            cv2.imwrite('dataSet/Student.' + str(id) + '.' + str(sampleNum) + '.' + str(clas)+ '.jpg', gray[y: y+h, x: x+w])
            #Tăng biến đếm:
            sampleNum = sampleNum + 1

    cv2.imshow('LAY DU LIEU HOC SINH.', img)
    
try:
    camera.release()
    cv2.destroyAllWindows()
except:
    print("Ok!")
try:
    trainner.Trainner()
except:
    print("Không thể trích xuất đặc trưng, hãy chạy chương trình trích xuất!")
