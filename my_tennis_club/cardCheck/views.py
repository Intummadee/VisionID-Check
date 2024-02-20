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
    check_text("../../assets/test03gray.jpg") # path นี้ไว้เช็ก image ที่ไม่ได้ขึ้น githup
    # check_text_Thai_Language("../../assets/test03gray.jpg")   # เช็กภาษาไทย

    return render(request, 'MainPage.html', {
        # 'frame_base64': frame_base64,
    })


#! Mongo Tip Here!!!!!!
def MongoConnect(request):
    # ฟังชันนี้มีเพื่อ เก็บข้อมูลการเชื่อมต่อกับ Mongo ไว้ทั้ง อ่าน อัพเดต ลบ หรือ query 💐
    conn_str = "mongodb+srv://kataroja1:kataroja7899@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
    # conn_str = "mongodb+srv://kataroja1:<passwordInMyDiscord>@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"

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


    #! Reading the document
    # record = myCollection.find_one()
    # print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'This is pymongo demo'}

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
            png_path = os.path.join(fs.location, 'output.png') # ตัวนี้คือกำหนด path ที่จะเซฟ และชื่อ ไฟล์ เพื่อใช้บรรทัดล่าง 
            # print(png_path) => C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\output.png
            save_image_as_png(image_paths[0], png_path) # บันทึกรูปภาพแรกจากรายการ image_paths เป็นไฟล์ PNG ที่ตำแหน่งที่กำหนด.
            text = check_text(png_path)
            # ถ้า pdf ที่ส่งมามีหลายหน้า ก็มาวนลูปเซฟภาพตาม pdf ตรงนี้ 🚀

            conn_str = "mongodb+srv://kataroja1:kataroja7899@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
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


            #!! นำข้อมูลที่อ่านมา ส่ง เข้าฐานข้อมูล 
            print("data ที่ได้มาจากการอ่าน ไฟล์ .pdf")
            words = [word for line in text.splitlines() for word in line.split()]
            print(words)
            for i in range(0, len(words), 3):
                # ใช้เลข 3 เพราะ ตารางไฟล์ที่ upload เข้ามา มี สาม คอลัมคือ รหัสนักศึกษา , ชื่อ , นามสกุล
                # print(words[i], words[i + 1], words[i + 2]) 
                # 64070257 Hydro Carbon
                
                student_number = {
                    "id_number" : words[i], # รหัสนักศึกษา
                    "student_fistName": words[i + 1],
                    "student_surName" : words[i + 2],
                    "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
                }
                print("ข้อมูลนศ.ที่จะเก็บลง ฐานข้อมูล => " , student_number)
                # Insert the document
                
                # res = myCollection.insert_one(student_number)
                # print(res.inserted_id)



            


            # #!TODO Create a document / record
            # myDoc = {
            #     "id_number" : "Hello", # รหัสนักศึกษา
            #     "student_fistName": "This is pymongo demo",
            #     "student_surName" : "",
            #     "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
            # }
            # # Insert the document
            # res = myCollection.insert_one(myDoc)
            # print(res.inserted_id)




            png_url = fs.url('output.png') # fs.url = สร้าง URL ที่เชื่อมโยงไปยังไฟล์ 'output.png' ใน FileSystemStorag
            # print(png_url) => /media/output.png
            return JsonResponse({'png_url': png_url})
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
            check_text(saveImage_path) # เช็กข้อความในภาพตรงนี้
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
        checkStudentCome(data)
    

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
    # ถูกเรียกใช้โดย ฟังชัน check_text
    # ฟังชันนี้มีไว้เพื่อ ถ้าอ่านตัวอักษรจากภาพที่ user อัพโหลดมาแล้วเสร็จ จะได้ข้อความยาวๆมา เราก็ต้องมา กรอง เอาชื่อเฉพาะชื่อกับนามสกุล ออกมาจากภาพนั้น แล้วไป ค้นหา ชื่อนศ.คนนี้ใน ฐานข้อมูล จากนั้นเปลี่ยนสถานใน MongoDB ว่า นศ. คนนี้มาแล้ว
    conn_str = "mongodb+srv://kataroja1:kataroja7899@cluster0.0yrfv3l.mongodb.net/?retryWrites=true&w=majority"
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
    print("🍏🍏")
    print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'Welcome to coding 101 with Steve'}

   
    


    return ""

