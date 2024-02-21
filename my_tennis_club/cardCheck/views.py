from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

# สำหรับแสดงผลรูปภาพบนหน้าเว็บ
from io import BytesIO
import base64

# สำหรับจับข้อความ หรือ ocr
from PIL import Image , ImageEnhance, ImageFilter
import pytesseract


# Computer Vision , OpenCV
import numpy as np
import matplotlib.pyplot as plt
import cv2

 
# MongoDB
from pymongo import MongoClient
import pymongo

# For Upload File
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import fitz
 
# สำหรับไว้ตรวจหา เอาเฉพาะชื่อและนามสกุล ออกจากรูปภาพที่อัพโลหด
import re
import linecache 
 
# 🌺 ข้อควรระวัง ถ้าจะ return ไรไปหน้าเว็บ ต้องใช้ HttpResponse

def testCardCheck(request):
    print("testCardCheck")
    return HttpResponse("Hello world!")

def cardCheck(request):
    # template = loader.get_template('HomePage.html')
    # return HttpResponse(template.render())
    return HttpResponse("Hello world!")

def VideoCapture(request):
    print("VideoCapture click 🌿🌿" )
    cap = cv2.VideoCapture(0)
    while(True):
        # Take each frame
        _, frame = cap.read()
        

        height, width, channels = frame.shape # height = 480 , width =  640
        # Draw a rectangle - top-left at (50,50), bottom-right at (200,200) , (0, 255, 0) = color in BGR format
        # cv2.rectangle(frame, (50, 50), (width-50, height-50), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(5) & 0xFF == 27: # กด esc เพื่อ stop video
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    

    #! frame = ภาพสุดท้ายที่ถ่ายกับ Video มาแล้ว  แปลงภาพเป็นภาพขาวดำ

    # save ภาพ 
    cv2.imwrite('../assets/testImage.png', frame)
    check_text('../assets/test01gray.png')

    # Convert the frame to a base64 string
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')

    # Return the base64 string as part of the JSON response
    return JsonResponse({'frame_base64': frame_base64})


def MainPage(request): # http://127.0.0.1:8000/MainPage/
    print("Start HomePage.html 📦📦")
    

    # check_text("../assets/img-1.png") # path นี้ไว้เช็ก image ที่เอาขึ้น github
    # check_text("../../assets/test03gray.jpg") # path นี้ไว้เช็ก image ที่ไม่ได้ขึ้น githup
    # check_text_Thai_Language("../../assets/test03gray.jpg")   # เช็กภาษาไทย

    return render(request, 'MainPage.html', {
        # 'frame_base64': frame_base64,
    })


 
def createImageTable(request):
    #  ฟังชันนี้จะ อ่าน รายชื่อในฐานข้อมูล แล้วมาแสดงเป็นรูปภาพให้ผู้ใช้โหลดได้
    
    conn_str = "mongodb+srv://kataroja1:kataroja7899@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    
    # ขนาดจริงของกระดาษ A4 (210 x 297 มม.)
    # a4_width, a4_height = 210, 297
    a4_width, a4_height = 700, 800

    # สร้างภาพพื้นหลังสีขาวขนาด A4
    image_a4 = np.ones((a4_height, a4_width, 3), dtype=np.uint8) * 255

    # กำหนดขนาดของตาราง #! ถ้าจะเปลี่ยนจำนวนพวกนี้ ต้องระวังเรื่องการเขียนตัวอักษร เพราะบางตัวเลข เราใส่มือไป 
    num_rows = 31
    num_cols = 4
    # กำหนดตาราง ดังนี้ num_rows = 20 and num_cols = 4  คำตอบ ==>  cell_width_distance = 52  , cell_height_distance = 14
    cell_width_distance = image_a4.shape[1] // num_cols + 8 # .shape[1] = ความกว้าง หารด้วย จำนวนคอลัมทั้งหมด
    cell_height_distance = image_a4.shape[0] // num_rows # .shape[0] = ความสูง หารด้วย จำนวนแถวทั้งหมด
    # image_a4.shape[1] = 210 , image_a4.shape[0] = 297

    #! Reading the document
    cursor = myCollection.find()
        
    for row in range(num_rows + 1):
        y = row * cell_height_distance # เรามีความห่างของแต่ละแถว เท่ากับ cell_height_distance ทำให้ถ้าอยากได้แถวที่ สาม ก็เอาเลข 3 ไปคูณ กับระยะห่างระหว่างแถว ก็จะได้ แถวสามออกมา
        # print("row : ", row , "cell_height_distance : ", cell_height_distance , "y 🪁🪁: " , y)
        # row :  0 cell_height_distance :  14 y 🪁🪁:  0
        # row :  1 cell_height_distance :  14 y 🪁🪁:  14
        cv2.line(image_a4, (0, y), (image_a4.shape[1], y), (0, 0, 0), 1)

        # เขียนข้อความลงในทุกคอลัมน์ของแถว
        # range(start, stop) ถ้าเป็น range(num_cols + 1) หมายถึง startเริ่มต้นเป็น 0 เลย เหมือนเขียนแค่ stop อย่างเดียว
        if(row != 0): #เราจะไม่เขียนลง แถวแรก เพราะแถวแรกจะใส่หัวเรื่องแทน
            # for col in range(num_cols): # จำนวนคอลัม = 4 
            #     x = col * cell_width_distance 
                
            try:
                record = cursor.next()
                record_id_number = record['id_number']
                record_student_fistName = record['student_fistName']
                record_student_surName = record['student_surName']
                record_attendance_status = record['attendance_status']
                # print("🌊🌊 " , record_id_number)
            

                # วาดข้อความลงบนภาพ
                cv2.putText(image_a4, record_id_number, (0+10, y+cell_height_distance-3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, ) #* เริ่มที่ (x,y) = (0, y+15) เพราะ เราไม่เขียนลงแถวแรกเลยเลือก y = y +15 ส่วน x = 0 เพราะอันนี้คือรหัสนักศึกษาซึ่งเป็น คอลัมแรกในตาราง ข้อความนี้เลยต้องชิดซ้ายของภาพ
                cv2.putText(image_a4, record_student_fistName, (cell_width_distance+10, y+cell_height_distance-3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1,)
                cv2.putText(image_a4, record_student_surName, (cell_width_distance*2+10, y+cell_height_distance-3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, )
                #TODO cv2.putText(image_a4, record_attendance_status, (cell_width_distance*3+10, y+cell_height_distance+1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, )
                if(record_attendance_status == 0): # 0 = ไม่ได้เข้าสอบ , 1 = เข้าสอบ   #? เครื่องหมายอยากให้ ความกว้าง = 15 , ความสูง = 10
                    # วาดเครื่องหมายกากบาท - ขาดสอบ ❌
                    cv2.line(image_a4, (cell_width_distance*3+10,  y+cell_height_distance-5), (cell_width_distance*3+20, y+cell_height_distance-15), (0, 0, 255), 1, cv2.LINE_AA) 
                    cv2.line(image_a4, (cell_width_distance*3+10,  y+cell_height_distance-15), (cell_width_distance*3+20, y+cell_height_distance-5), (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    # วาดเครื่องหมายถูก - เข้าสอบ ✅
                    cv2.line(image_a4, (cell_width_distance*3+10,  y+cell_height_distance-5), (cell_width_distance*3+20, y+cell_height_distance-15), (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.line(image_a4, (cell_width_distance*3+10,  y+cell_height_distance-5), (cell_width_distance*3+7, y+cell_height_distance-8), (0, 255, 0), 1, cv2.LINE_AA)
            except StopIteration:
                # มันจะเกินมา เพราะจากตาราง เลยต้องมี การดัก ตัวนี้ไว้ , StopIteration แสดงว่า Cursor ไม่มีข้อมูลเพิ่มเติม
                break

    title = ["id_number", "firstname" , "surname", "attendance"]
    for col in range(num_cols):
        x = col * cell_width_distance
        # print("col : ", col , "cell_width_distance : ", cell_width_distance , "x 🍜🍜: " , x)
        # col :  0 cell_width_distance :  52 x 🍜🍜:  0  
        # col :  1 cell_width_distance :  52 x 🍜🍜:  52 #*สังเกตได้ว่า ทั้งสอง คอลัม  x จะห่างเท่ากับ 52 or cell_width_distance
        cv2.line(image_a4, (x, 0), (x, image_a4.shape[0]), (0, 0, 0), 1)

         
        #? คำที่ใช้ในแถวแรกอยู่ตรงนี้
        cv2.putText(image_a4, title[col], (x + 5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
 

    # ปรับขนาดภาพให้เท่ากับกระดาษ A4
    # scaled_image = cv2.resize(image_a4, (800, 900))  # 800 x 1131 คือขนาดที่เหมาะสมต่อการแสดงผล
    scaled_image = cv2.resize(image_a4, (a4_width, a4_height))  # 800 x 1131 คือขนาดที่เหมาะสมต่อการแสดงผล

    # แสดงภาพ
    cv2.imshow('A4 Size Image', scaled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return HttpResponse("Hello world!")



#! Mongo Tip Here!!!!!!
def MongoConnect(request):
    # ฟังชันนี้มีเพื่อ เก็บข้อมูลการเชื่อมต่อกับ Mongo ไว้ทั้ง อ่าน อัพเดต ลบ หรือ query 💐
    conn_str = "mongodb+srv://kataroja1:<YourPassword>@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"

    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)


    # Create a DB
    myDb = client["pymongo_demo"]
    # Create a collection
    myCollection = myDb["demo_collection"]
    print(client.list_database_names())


    #!TODO Create a document / record
    # myDoc = {
    #     "name" : "Hello",
    #     "message": "This is pymongo demo"
    # }
    # # Insert the document
    # res = myCollection.insert_one(myDoc)
    # print(res.inserted_id)


    #! Reading the document อ่านแค่ rocord เดียว
    # record = myCollection.find_one()
    # print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'This is pymongo demo'}

    #! Reading the document อ่าน all record
    # cursor = myCollection.find()
    # for record in cursor:
    #     print(record)

    #! Reading but Query by student_fistName
    # record = myCollection.find_one({"student_fistName": firstName}) 
    # print(record) # => {'_id': ObjectId('65d4ca7f93805c855c82da41'), 'id_number': '64070257', 'student_fistName': 'Intummadee', 'student_surName': 'Carbon', 'attendance_status': 0}

    #? Updating the record 
    # query = {
    #     "message":"This is pymongo demo"
    # }
    # new_val = {
    #     "$set": {"message":"Welcome to coding 101 with Steve"}
    # }
    # new_record = myCollection.update_one(query, new_val)
    # record = myCollection.find_one()
    # print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'Welcome to coding 101 with Steve'}

    #? Update but query by student_fistName and set new value especially attendance_status
    # new_record = myCollection.update_one({"student_fistName": firstName}, {"$set": {"attendance_status": 1}})

    #* Step 9: Delete the Record
    # query_del = {
    #     "name": "Hello"
    # }
    # record_del = myCollection.delete_one(query_del)
    # #Reading the document after updating
    # record = myCollection.find_one()
    # print(record)


    return ""

#* PDF
def upload_and_convert_pdf(request):
    print("เข้า upload_and_convert_pdf")
    if request.method == 'POST' and request.FILES['pdf_file']: # ตรวจว่า มีไฟล์ PDF ถูกส่งมา
        # Handle the uploaded PDF file
        uploaded_file = request.FILES['pdf_file'] #  ดึงข้อมูลของไฟล์ PDF ที่ถูกอัปโหลดมา.
        fs = FileSystemStorage() # สร้างอ็อบเจ็กต์ FileSystemStorage ซึ่งเป็นวัตถุที่ช่วยในการจัดการไฟล์ของ Django.
        pdf_filename = fs.save(uploaded_file.name, uploaded_file) # บันทึกไฟล์ PDF ในระบบเก็บข้อมูลของ Django และรับชื่อไฟล์ที่ถูกบันทึก.
        # print(pdf_filename) => resume.pdf

        # Convert PDF to images 
        #  fs.location หรือ ตำแหน่งที่จะเซฟไฟล์ ถูกกำหนดไว้ใน settings.py ซึ่งตำแหน่งนั้นจะแปรไปตามค่าชื่อ MEDIA_ROOT ที่กำหนดไว้ หรือก็คือ fs.location จะเป็นที่ตั้งนี้
        pdf_path = os.path.join(fs.location, pdf_filename) # สร้างเส้นทางสำหรับไฟล์ PDF.
        # print("pdf_path = " + pdf_path) => C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\test2.pdf เราใส่ pdf ชื่อ test2.pdf มา
        image_paths = convert_pdf_to_images(pdf_path) # แปลงไฟล์ PDF เป็นรูปภาพ และได้รับเส้นทางของรูปภาพ.
        # print(image_paths) =>  ['page_1.png', 'page_2.png'] pdfมีหลายหน้า pathก็มีหลายหน้าตาม แต่เราเซฟภาพแค่รูปแรก
        
        # Save the first image as a PNG file
        if image_paths:

            first_page_image_path = image_paths[0]
            png_path = os.path.join(fs.location, 'output.png') 
            save_image_as_png(first_page_image_path, png_path)
            # check_text(first_page_image_path)

            page_png_path_url = [] # ตัวแปรนี้ไว้เก็บ path ของ image เพื่อส่งไปยัง frontend ให้ฝั่ง frontend แสดงภาพตามจำนวนหน้า pdf 

            for i, page_image_path in enumerate(image_paths):
                # print(page_image_path) # เก็บชื่อ ไฟลฺ image เอาไว้  , .pdf มีสองหน้าจะ print ออกมาสองรอบ  page_1.png และ  page_2.png
                page_png_path = os.path.join(fs.location, f'page_{i + 1}.png')
                # page_png_path = print path ออกมา สองรอบ ตามจำนวนหน้าในไฟล์ .pdf เช่น C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\page_2.png  และ   C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\page_1.png
                save_image_as_png(page_image_path, page_png_path) # ถ้า pdf ที่ส่งมามีหลายหน้า ก็มาวนลูปเซฟภาพตาม pdf ตรงนี้ 🚀

                page_png_path_url.append(fs.url(page_image_path))

                #* ตรงนี้เช็ก text แล้ว
                text = check_text(page_png_path)
                # print("text " , text)

                # conn_str = "mongodb+srv://kataroja1:<YourPassword>@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
                # try:
                #     client = pymongo.MongoClient(conn_str)
                #     print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
                # except Exception:
                #     print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)

                # # Create a DB
                # myDb = client["pymongo_demo"]
                # # Create a collection
                # myCollection = myDb["demo_collection"]
                # print(client.list_database_names())


                print(text)
                #!! นำข้อมูลที่อ่านมา ส่ง เข้าฐานข้อมูล 
                lines = text.splitlines()
                for line in lines:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        number_part, text_part = parts
                        text_part = text_part.replace('-', '').replace('=', '').strip() 
                        subparts = text_part.split(' ', 1)
                        if len(subparts) == 2:
                            first_part, second_part = subparts
                            if '—' in second_part: # แก้ส่วน second ที่บางชื่อจะเป็นแบบนี้ => 64070001 ชื่อ =  HarmonyHub นามสกุล =  — Tranquilwood (ในนามสกุลหรือส่วน second_part มี — ติดอยู่ เลยจำเป็นต้องมีเงื่อนไข เพื่อลบอันนี้ออก)
                                second_part = second_part.split('—', 1)[1].strip()
                            print(number_part, "ชื่อ = ", first_part, "นามสกุล = ", second_part)
                    student_number = {
                        "id_number" : number_part, # รหัสนักศึกษา
                        "student_fistName": first_part,
                        "student_surName" : second_part,
                        "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
                    }
                    #TODO Insert the document
                    # res = myCollection.insert_one(student_number)
                    # print(res.inserted_id)

                    # print("ข้อมูลนศ.ที่จะเก็บลง ฐานข้อมูล => " , student_number) ==> ข้อมูลนศ.ที่จะเก็บลง ฐานข้อมูล =>  {'id_number': '64070254', 'student_fistName': 'Anchisa', 'student_surName': 'Cherdsattayanukul', 'attendance_status': 0}
                    # print(student_number)
            
            return JsonResponse({'page_png_path_url': page_png_path_url}) # page_png_path_url = [ /media/page_1.png ,  /media/page_2.png ]
        return JsonResponse({'error': 'Invalid request'}, status=400)

def convert_pdf_to_images(pdf_path):
    images = []
    doc = fitz.open(pdf_path)
    
    for page_number in range(doc.page_count):
        page = doc[page_number]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_path = f'page_{page_number + 1}.png'
        img.save(img_path)
        images.append(img_path)
    
    return images

def save_image_as_png(source_path, destination_path):
    img = Image.open(source_path)
    img.save(destination_path, 'PNG')


#* ภาพ Image
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        uploaded_image = request.FILES['image_file']
        fs = FileSystemStorage()
        image_filename = fs.save(uploaded_image.name, uploaded_image)
        # print(image_filename) ==> Database.png ได้ชื่อไฟล์ออกมา
        image_path = os.path.join(fs.location, image_filename) 
        # print("image_path = " + image_path) => C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\74b05-16299573593572-800.avif
        if image_path:
            saveImage_path = os.path.join(fs.location, 'outputImage.png') 
            save_image_as_png(image_path, saveImage_path)
            text = check_text(saveImage_path) # เช็กข้อความในภาพตรงนี้

            #⁡⁣⁢⁣TODO ค้นหาแค่ชื่อและนามสกุล จากในภาพตรงนี้ ใช้ทับกับของ pdf ไม่ได้เพราะ pdf จะมีโครงสร้าง มาให้เลย แต่ image ไม่มี⁡
            # -คิดว่าจะแก้ VideoCapture ให้อัพโหลดภาพลงเครื่อง แล้วมาเข้าฟังชันนี้เลย 
            
            print(text)
            




            saveImage_url = fs.url('outputImage.png') 
            return JsonResponse({'saveImage_url': saveImage_url})
        return JsonResponse({'error': 'Invalid request'}, status=400)

def check_text(image_path):
    print("Check ตัวอักษร English 🌏🌏🌏🌏")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # image_path = '../assets/' + Image_name
    image = cv2.imread(image_path)
    # ทำการดำเนินการต่อไปที่ต้องการ เช่น ใช้ pytesseract สำหรับการ OCR

    if image is not None:
        # path ไฟล์ภาพนี้จะเอาไว้ ทดลอง
        #! cv2.imwrite('../assets/testImage_Here.png', img)

        # แปลงภาพเป็น Grayscale ก่อนที่จะใช้ pytesseract.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Perform text extraction
        data = pytesseract.image_to_string(thresh, lang='eng')
        print(data)
        print("------------ จบการเช็ก ------------")    

    return data

def check_text_Thai_Language(image_path):
    print("Check ตัวอักษร Thailand 🇹🇭 🇹🇭 ⋆｡˚ ✈︎ ✈️ ⋆")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image = cv2.imread(image_path)
    # print(image)
    if image is not None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Perform text extraction
        text = pytesseract.image_to_string(thresh, lang='tha')  #Specify language to look after!
        # --psm 6 หมายถึง Sparse text. Tesseract จะพยายามแยกแยะข้อความในภาพที่มีการเว้นระยะทางและข้อความที่มีช่องว่างอยู่รอบ ๆ ข้อความ
        print(text)

    return text

def checkStudentCome(text):
    # ฟังชันนี้จะถูกเรียกใช้โดย ฟังชัน check_text
    # ฟังชันนี้มีไว้เพื่อ ถ้าอ่านตัวอักษรจากภาพที่ user อัพโหลดมาแล้วเสร็จ จะได้ข้อความยาวๆมา เราก็ต้องมา กรอง เอาชื่อเฉพาะชื่อกับนามสกุล ออกมาจากภาพนั้น แล้วไป ค้นหา ชื่อนศ.คนนี้ใน ฐานข้อมูล จากนั้นเปลี่ยนสถานใน MongoDB ว่า นศ. คนนี้มาแล้ว
    conn_str = "mongodb+srv://kataroja1:<YourPassword>@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
    print(" ---- uploadMongoDB ⛱️⛱️⛱️ ---- ")
    
    lines = text.splitlines()
    # หากมีบรรทัดที่ 6
    if len(lines) >= 7:
        line_6_words = lines[5].split()  # แยกคำในบรรทัดที่ 6 ที่มีชื่อ
        line_7_words = lines[6].split()  # แยกคำในบรรทัดที่ 7 ที่มีนามสกุล
        if line_6_words:
            firstName = line_6_words[-1]
            print("ชื่อของฉันคือ •ᴗ• :", firstName) # Intummadee
        if line_7_words:
            surName = line_7_words[-1]
            print("นามสกุลของฉันคือ (> <) :", surName) # Maliyam


    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)

    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    
    #? Updating the record 
    new_record = myCollection.update_one({"student_fistName": firstName}, {"$set": {"attendance_status": 1}})
    record = myCollection.find_one({"student_fistName": firstName})
    print("🍏🍏 record ที่อัพเดตแล้ว")
    print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'Welcome to coding 101 with Steve'}

   
    


    return ""

