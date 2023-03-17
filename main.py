#Khai báo các thư viện sử dụng trong chương trình:
import cv2
import gspread
import sqlite3
import numpy as np

from datetime import datetime
from gspread.exceptions import WorksheetNotFound
from gspread.exceptions import SpreadsheetNotFound

auth = gspread.service_account(filename='service_account.json')

#Thay đổi gmail tại đây:
mail = 'youremail@gmail.com'

#Khởi tạo camera:
camera = cv2.VideoCapture(0)

#Khởi tạo bộ module phát hiện khuôn mặt người theo chuẩn haarcascade:
face_detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Khởi tạo module trích xuất đặc trưng:
trainner_module = cv2.face.LBPHFaceRecognizer_create()

#Đọc dữ liệu đầu vào của tệp trainner:
trainner_module.read("recognizer/trainner.yml")

#Khai báo các biến về màu sắc để tiện sử dụng:
textColor = (0, 255, 0)
lineColor = (255, 0, 0)
textFont = cv2.FONT_HERSHEY_COMPLEX
lastName = None

#Hàm trả về giá trị ngày giờ hiện tại:
def DateAndTime():

    date_time = datetime.now()

    month = date_time.month
    day = date_time.day
    year = date_time.year
    time = date_time.strftime("%H:%M:%S")
    
    return day, month, year, time

#Hàm chuyển dữ  liệu vào trong excel:
def excelCommit(clas, id, name):

    day, month, year, time = DateAndTime()
    date = str(day)+ "/" + str(month) + "/" + str(year)
    Ssheet_name = "DIEM DANH ngay " + date

    try:
        Ssheet = auth.open(Ssheet_name)
    except SpreadsheetNotFound:
        Ssheet = auth.create(Ssheet_name)
        Ssheet.share(mail, perm_type='user', role='writer')
    try:
        WSheet = Ssheet.worksheet(clas)
    except WorksheetNotFound:
        WSheet = Ssheet.add_worksheet(str(clas), 100, 10)

    if WSheet.find(name) == None:
        WSheet.update_cell(int(id)+1, 1, id)
        WSheet.update_cell(int(id)+1, 2, name)
        WSheet.update_cell(int(id)+1, 3, clas)
        WSheet.update_cell(int(id)+1, 4, date)
        WSheet.update_cell(int(id)+1, 5, time)
    else:
        pass

#Hàm lấy thông tin của đối tượng gắn với ID => Hàm trả về 2 kết quả là tên và lớp học của học sinh:
def getInfor(id):

    CSDL = sqlite3.connect("STUDENT.db")
    dia_chi = CSDL.execute("SELECT * FROM CLASS WHERE STT=" + str(id))
    thong_tin = None
    for row in dia_chi:
        thong_tin = row
    CSDL.close()
    
    name = thong_tin[1]
    clas = thong_tin[2]

    return name, clas

while True:

    #Đọc từng khung hình thông qua camera:
    _, frame = camera.read()

    #Chuyển hình ảnh thành màu xám:
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Tìm vị trí của khuôn mặt có trong bức ảnh:
    faces =  face_detect.detectMultiScale(grayImg, 1.5, 3)

    for  (x, y, h,  w) in faces:

        #Vẽ hình xung quanh khuôn mặt tìm được:
        cv2.rectangle(frame, (x, y), (x+w, y+h), lineColor, 2)

        #Nhận diện khuôn mặt trả về ID và độ chính xác:
        id, precision = trainner_module.predict(grayImg[y: y+h, x: x+w])

        #Nếu độ sai khác nhỏ thì lấy thông tin người dùng:
        if precision <= 50:
            name, clas = getInfor(id)
            if lastName != name:
                excelCommit(clas, id, name)
            lastName = name
            cv2.putText(frame, name + " - " + clas, (x, y+h+30), textFont, 1, textColor, 1)
        else:
            cv2.putText(frame, "Khong co thong tin!", (x, y + h + 30), textFont, 1, textColor, 1)

    cv2.imshow("HE THONG DIEM DANH.", frame)
    if cv2.waitKey(1)  & 0xff == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()