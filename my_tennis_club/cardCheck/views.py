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
 

# ใช้สำหรับ ดึงชื่อ หรือ นามสกุล
import re

# ใช้สำหรับ เช็กว่า String มีความต่างกันกี่เปอร์เซ็น ,  using SequenceMatcher.ratio()
from difflib import SequenceMatcher 

# ใช้ ดึงข้อมูลจาก JSON string ที่ได้รับจาก JsonResponse
import json

# มาจากไลบรารี่ pip install reportlab เป็น library เรื่อง สร้างไฟล์ PDF และเพิ่มรูปภาพลงในไฟล์ PDF --> ใช้ในฟังชัน ⁡⁢⁢⁣createImageTable⁡ เป็นการสร้าง pdf จากตารางที่ถูกสร้างขึ้น
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# สำหรับย้ายไฟล์เฉยๆ
import shutil

# ใช้อ่าน Excel
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse



from django.http import FileResponse
from django.shortcuts import get_object_or_404

# login_required decorator ของ Django
from django.contrib.auth.decorators import login_required

# env
from dotenv import load_dotenv

from django.shortcuts import redirect


# ใช้วันที่และเวลาสุ่มชือในการ save รุปภาพ 
from datetime import datetime
import uuid


# 🌺 ข้อควรระวัง ถ้าจะ return ไรไปหน้าเว็บ ต้องใช้ HttpResponse




# cardCheck/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) # SignUpForm เป็นฟอร์มที่คุณสร้างขึ้นสำหรับการสมัครสมาชิกใหม่
        if form.is_valid():
            user = form.save() # หากฟอร์มถูกต้อง, บันทึกข้อมูลผู้ใช้ใหม่ในฐานข้อมูลโดยเรียกเมธอด save() ของฟอร์ม ซึ่งจะสร้างออบเจ็กต์ผู้ใช้ใหม่และบันทึกในฐานข้อมูล
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # ใช้เมธอด authenticate ของ Django เพื่อยืนยันตัวตนของผู้ใช้โดยใช้ username และ password. ถ้าข้อมูลถูกต้อง, จะได้ออบเจ็กต์ผู้ใช้ (user) ถ้าไม่ถูกต้อง, จะได้ค่า None
            login(request, user) # ใช้เมธอด login เพื่อเข้าสู่ระบบให้กับผู้ใช้ที่เพิ่งสมัครสมาชิกใหม่
            # ส่งค่า username ใน session
            request.session['username'] = username


            # ต่อMONGO
            try:
                client = pymongo.MongoClient(conn_str)
                print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
            except Exception:
                print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
            myDb = client["pymongo_demo"]
            myCollection = myDb["demo_collection"]
            
            myDoc = {
                "username" : username,
                "list_all": []
            }
            # Insert the document
            res = myCollection.insert_one(myDoc)


            return redirect('login')  # เปลี่ยน 'home' เป็น URL ที่คุณต้องการ
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login
# cardCheck/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) #  form = AuthenticationForm(request, data=request.POST)
        # สร้างออบเจ็กต์ฟอร์ม AuthenticationForm จากข้อมูลที่ผู้ใช้ส่งมาใน request.POST. AuthenticationForm เป็นฟอร์มในตัวของ Django ที่ใช้สำหรับตรวจสอบข้อมูลการเข้าสู่ระบบ
        if form.is_valid():
            # ดึงค่าของ username และ password จาก cleaned_data ซึ่งเป็นข้อมูลที่ผ่านการตรวจสอบและทำความสะอาดแล้ว
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            # ใช้เมธอด authenticate ของ Django เพื่อยืนยันตัวตนของผู้ใช้โดยใช้ username และ password. ถ้าข้อมูลถูกต้อง, จะได้ออบเจ็กต์ผู้ใช้ (user) ถ้าไม่ถูกต้อง, จะได้ค่า None
            if user is not None:
                login(request, user) # ใช้เมธอด login เพื่อเข้าสู่ระบบให้กับผู้ใช้
                # ส่งค่า username ใน session
                request.session['username'] = username
                return redirect('MainPage')  # เปลี่ยน 'home' เป็น URL ที่คุณต้องการให้ผู้ใช้ไปหลังจากเข้าสู่ระบบสำเร็จ
    else:
        # ถ้าคำขอไม่ใช่แบบ POST, สร้างฟอร์ม AuthenticationForm เปล่า ๆ เพื่อให้ผู้ใช้กรอกข้อมูล
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('MainPage')


# โหลด Environment Variables จากไฟล์ .env
load_dotenv()


# ดึงค่า Environment Variable
conn_str = os.getenv('MONGO_CONN_STR')



def testCardCheck(request):
    print("testCardCheck 🥊🥊🥊🥊🥊")
    # สร้างมาเพราะเคยเจอบัคตาม assets/bugs/image1 = เหตุเกิดเพราะ path หรือ ชื่อ image ไม่ถูก

    # Load the image
    # image_path = r"C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club\media\outputImage.png"
    
    image = cv2.imread("./media/outputImage.png"); # . คือ path => C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club
    print("image : ", image); # If output is matrix then image read is successful.  if output is 'None' then either path or name of the image is wrong.
    cv2.imshow("Image", image);
    cv2.waitKey(0);
    cv2.destroyAllWindows();

    return HttpResponse("Success!")

def cardCheck(request):
    # template = loader.get_template('HomePage.html')
    # return HttpResponse(template.render())
    return HttpResponse("Hello world! cardCheck")


# def HomeFirst(request):
#     print("Start HomePage.html 📦📦");
#     return HttpResponse("Hello world!")





# @login_required(login_url='/login/')
# ⁡⁣⁣⁢---- 𝗠𝗮𝗶𝗻 𝗛𝗲𝗿𝗲⁡ ----
def MainPage(request): # http://127.0.0.1:8000/MainPage/
    print("Start HomePage.html 📦📦")

    # คอมเมนด้านล่าง เอาไว้เช็ก method check_text
    # check_text("../assets/img-1.png") # path นี้ไว้เช็ก image ที่เอาขึ้น github

    #? คอมเมนด้านล่างไว้สำหรับเรียกใช้งาน ฟังชัน  clearRecord คือการลบทุกรายชื่อในฐานข้อมูล
    # clearRecord()


    # รูปจากคอมเมนด้านล่าง ที่ชื่อ testImage เป็นรูปถ่ายจาก วิดิโอ สร้างมาเพื่อเช็กเฉยๆ
    # check_text('../assets/testImage.png')


    # check_text("../../assets/test03gray.jpg") # path นี้ไว้เช็ก image ที่ไม่ได้ขึ้น githup , อันนี้แล้วแต่ จะสร้าง หรือไม่สร้างก็ได้ แต่นี่สร้างเพื่อใส่รูปภาพที่เอาขึ้นกิตไม่ได้ เช่น พวก ปชช. 
    # check_text_Thai_Language("../../assets/test03gray.jpg")   # เช็กเวอร์ขั่นภาษาไทย

    username = request.session.get('username', 'GuestTest')  # อ่านค่า username จาก session , ถ้าคีย์ username ไม่มีอยู่ในเซสชัน จะคืนค่า 'Guest' แทน.
    # session ใน Django คือพื้นที่เก็บข้อมูลชั่วคราวสำหรับผู้ใช้ที่สามารถใช้ข้ามคำขอ HTTP ได้ ซึ่งมีประโยชน์ในการเก็บข้อมูลระหว่างการเยี่ยมชมหน้าเว็บต่างๆ ของผู้ใช้.
    return render(request, 'MainPage.html', {'username': username})


# 💊💊
# ⁡⁣⁢⁣สร้างตาราง⁡
def createImageTable(request):
    #  ฟังชันนี้จะ อ่าน รายชื่อในฐานข้อมูล แล้วมาแสดงเป็นรูปภาพให้ผู้ใช้โหลดได้
    
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    
    username = request.session.get('username')
    record = myCollection.find_one({"username": username})
    # ในภาพ (image_a4) มี 31 รายชื่อฮ๊าฟฟู๊วววว
    record_count = len(record.get("list_all"));
    
    if (record_count == 0):
        print("ยังไม่มีรายชื่อ")
        return JsonResponse({'NothaveList': True})

    #! Reading all field
    # cursor = myCollection.find()
    cursor = record.get("list_all");
    

    
    image_toPDF = [] # ตัวแปรนี้ไว้เก็บภาพ เพื่อจะเอามาสร้างเป็น pdf

    # ตัวอย่างมีรายชื่อทั้งหมด=33 รายชื่อ ในแต่ละภาพจะเขียนได้แค่ 31 รายชื่อ --> 33 / 31 = 1 ครั้ง รวม 0 ใน for loop ด้วย ก็เท่ากับ จะสร้างภาพขึ้นมา สอง รอบ
    for i in range(0, record_count // 31 + 1):
        print("🐰ྀ🐻ིྀ ", i , record_count)

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
        
        title = ["id_number", "firstname" , "surname", "attendance"]
        for col in range(num_cols):
            x = col * cell_width_distance
            # print("col : ", col , "cell_width_distance : ", cell_width_distance , "x 🍜🍜: " , x)
            # col :  0 cell_width_distance :  52 x 🍜🍜:  0  
            # col :  1 cell_width_distance :  52 x 🍜🍜:  52 #*สังเกตได้ว่า ทั้งสอง คอลัม  x จะห่างเท่ากับ 52 or cell_width_distance
            cv2.line(image_a4, (x, 0), (x, image_a4.shape[0]), (0, 0, 0), 1)

            
            #? คำที่ใช้ในแถวแรกอยู่ตรงนี้
            cv2.putText(image_a4, title[col], (x + 5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        
        # สร้าง iterator จาก list
        cursor_iter = iter(cursor)


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
                    # record = cursor.next() # record {'_id': ObjectId('65f3821a6db989ce8e93d03c'), 'id_number': 64070004, 'student_firstName': 'BlissfulWords', 'student_surName': 'Zenhaven', 'attendance_status': 0}
                    record = next(cursor_iter)
                    record_id_number = str(record['id_number']) # ใส่ string ให้แน่ใจ เพราะฟังชัน cv2.putText รับแค่ string
                    record_student_firstName = record['student_firstName']
                    record_student_surName = record['student_surName']
                    record_attendance_status = record['attendance_status']
                    print("🌊🌊 " , record_id_number)
                

                    # วาดข้อความลงบนภาพ
                    cv2.putText(image_a4, record_id_number, (0+10, y+cell_height_distance-3), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, ) #* เริ่มที่ (x,y) = (0, y+15) เพราะ เราไม่เขียนลงแถวแรกเลยเลือก y = y +15 ส่วน x = 0 เพราะอันนี้คือรหัสนักศึกษาซึ่งเป็น คอลัมแรกในตาราง ข้อความนี้เลยต้องชิดซ้ายของภาพ
                    cv2.putText(image_a4, record_student_firstName, (cell_width_distance+10, y+cell_height_distance-3), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1,)
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
    
        # ปรับขนาดภาพให้เท่ากับกระดาษ A4
        # scaled_image = cv2.resize(image_a4, (800, 900))  # 800 x 1131 คือขนาดที่เหมาะสมต่อการแสดงผล
        scaled_image = cv2.resize(image_a4, (a4_width, a4_height))  # 800 x 1131 คือขนาดที่เหมาะสมต่อการแสดงผล
        
        # แสดงภาพ
        # cv2.imshow('A4 Size Image', scaled_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        
        # ดึงเส้นทางปัจจุบัน
        current_directory = os.getcwd()
        new_directory = 'media' # กำหนดโฟลเดอร์ที่ต้องการ
        full_path = os.path.join(current_directory, new_directory) # รวมเส้นทาง
        # full_path = C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club\media
        image_filename = f'image_{i}.png' # สร้างชื่อไฟล์รูปภาพ
        new_image_path = os.path.join(full_path, image_filename) # สร้างเส้นทางใหม่
        os.makedirs(full_path, exist_ok=True) # สร้างโฟลเดอร์ถ้ายังไม่มี

        # บันทึกไฟล์รูปภาพ
        # cv2.imwrite(new_image_path, scaled_image)
        cv2.imwrite("./media/"+image_filename, scaled_image)
    # ./media/
    # imwrite('../assets/testImage.png', frame)
        # เพิ่มชื่อไฟล์ลงในรายการสำหรับ PDF
        image_toPDF.append(new_image_path)
        # image_toPDF = ['C:\\Users\\User\\Documents\\ปี3\\GIT_CardCheck\\CardCheck\\my_tennis_club\\media\\image_0.png']




    
        # เรียกใช้ฟังก์ชันเพื่อสร้าง PDF
        pdf_filename = 'myListStudent.pdf'
        add_image_to_pdf(pdf_filename, image_toPDF)



        # ย้ายไฟล์ PDF ไปยังโฟลเดอร์ listStudent
        output_pdf_path = os.path.join('media', pdf_filename)
        shutil.move(pdf_filename, output_pdf_path)


        full_path = os.path.join(current_directory, "media")
        directory_PDF_ListStudent = os.path.join(full_path, "myListStudent.pdf") # C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\listStudent\myListStudent.pdf


        

    
        #TODO สร้างลิงก์ไปยังไฟล์ PDF และรายการลิงก์สำหรับไฟล์รูปภาพไปหน้าบ้าน 
        pdf_link = directory_PDF_ListStudent  # ไฟล์ PDF ที่สร้าง ==>  C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\listStudent\myListStudent.pdf
        image_links = image_toPDF  # รายการลิงก์สำหรับไฟล์รูปภาพ ==> ['C:\\Users\\User\\Documents\\Git_ComVi\\CardCheck\\my_tennis_club\\media\\image_0.png', 'C:\\Users\\User\\Documents\\Git_ComVi\\CardCheck\\my_tennis_club\\media\\image_1.png']
        print("🧸🧸 " , pdf_link)


        #TODO จะส่ง excel ไปหน้าบ้านด้วย
        excel_file_name = createExcelFromDB(username, cursor);
        # full_path = os.path.join(current_directory, "media")
        # excel_link = os.path.join(full_path, excel_file_name)


    # สร้าง JSON response ที่มีข้อมูลเพื่อแสดงผลที่ frontend
    response_data = {
        'pdf_link': pdf_link,
        'image_links': image_links, 
        'excel_file_name': excel_file_name
    }

    return JsonResponse(response_data)



def createExcelFromDB(username, list_all):
    # ฟังชันนี้ไว้สร้าง ไฟล์ excel จาก DB เพื่อส่งกลับไปหาผู้ใช้ที่หน้าบ้าน
    # ถูกเรียกใช้โดย def createImageTable
    print("🛒💸💰 createExcelFromDB")
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'{username}_{current_time}.xlsx'
    # name = "North.xlsx"
    

    new_list_all = []
    for items in list_all:
        if items.get("attendance_status")  == 1:
            student_number = {
                "id_number" : items.get("id_number")+"", # รหัสนักศึกษา
                "student_firstName": items.get("student_firstName"),
                "student_surName" : items.get("student_surName"),
                "attendance_status" : "มา", # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
            }
            new_list_all.append(student_number);
        else:
            student_number = {
                "id_number" : items.get("id_number")+"", # รหัสนักศึกษา
                "student_firstName": items.get("student_firstName"),
                "student_surName" : items.get("student_surName"),
                "attendance_status" : "ขาด", # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
            }
            new_list_all.append(student_number);


    # สร้าง DataFrame จากข้อมูล data
    df = pd.DataFrame(new_list_all)

    # กำหนดชื่อคอลัมน์
    df.columns = ['id_number', 'student_firstName', 'student_surName', 'attendance_status']

    # เรียงลำดับคอลัมน์ใหม่
    df = df[['id_number', 'student_firstName', 'student_surName', 'attendance_status']]


    # เชื่อมไฟล์เข้ากับ media folder
    output_excel_path = os.path.join('media', file_name)
    # บันทึกเป็นไฟล์ Excel
    df.to_excel(output_excel_path, index=False)
    return file_name;



#! 𝗠𝗼𝗻𝗴𝗼 𝗧𝗶𝗽 𝗛𝗲𝗿𝗲!!!!!!
def MongoConnect(request):
    # ฟังชันนี้มีเพื่อ เก็บข้อมูลการเชื่อมต่อกับ Mongo ไว้ทั้ง อ่าน อัพเดต ลบ หรือ query 💐

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

    #⁡⁢⁢⁣ ⁡⁢⁢⁣𝗠𝘆 𝗱𝗮𝘁𝗮𝗯𝗮𝘀𝗲⁡⁡⁡
    # student_number = {
    #     "id_number" : number_part, # รหัสนักศึกษา
    #     "student_firstName": first_part,
    #     "student_surName" : second_part,
    #     "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
    # }


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

    #! Reading but Query by student_firstName
    # record = myCollection.find_one({"student_firstName": firstName}) 
    # print(record) # => {'_id': ObjectId('65d4ca7f93805c855c82da41'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Carbon', 'attendance_status': 0}

    #! Reading one Field
    # record_firstName = myCollection.find({}, {"student_firstName": 1})
    #     for record in record_firstName:
    #         print(record.get("student_firstName"))
    
    
    # ⁡⁣⁣⁢#! Count ⁡
    # record_count = myCollection.count_documents({})
    # print(record_count)




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

    #? Update but query by student_firstName and set new value especially attendance_status
    # new_record = myCollection.update_one({"student_firstName": firstName}, {"$set": {"attendance_status": 1}})

    #? Update in new version by filter username and id_number
    # myCollection.update_one(
    # {"username": username, "list_all.id_number": student_id},
    # {"$set": {"list_all.$.attendance_status": 1}} # $ ใช้ในการอ้างถึง element ใน list_all ที่ตรงกับเงื่อนไขค้นหา ซึ่งคือ list_all.id_number เท่ากับ student_id.
    # )


    #* Step 9: Delete the Record
    # query_del = {
    #     "name": "Hello"
    # }
    # record_del = myCollection.delete_one(query_del)
    # #Reading the document after updating
    # record = myCollection.find_one()
    # print(record)

    #* Delete all record
    # result = myCollection.delete_many({})


    return ""


# 💊💊
#* 𝗣𝗗𝗙
def upload_and_convert_pdf(request):
    print("เข้า upload_and_convert_pdf 🌐🌐🌐🌐🌐")
    if request.method == 'POST' and request.FILES['pdf_file']: # ตรวจว่า มีไฟล์ PDF ถูกส่งมา
        # Handle the uploaded PDF file
        uploaded_file = request.FILES['pdf_file'] #  ดึงข้อมูลของไฟล์ PDF ที่ถูกอัปโหลดมา.
        fs = FileSystemStorage() # สร้างอ็อบเจ็กต์ FileSystemStorage ซึ่งเป็นวัตถุที่ช่วยในการจัดการไฟล์ของ Django.
        pdf_filename = fs.save(uploaded_file.name, uploaded_file) # บันทึกไฟล์ PDF ในระบบเก็บข้อมูลของ Django และรับชื่อไฟล์ที่ถูกบันทึก.
        # print(pdf_filename) => resume.pdf

        # Convert PDF to images 
        #  fs.location หรือ ตำแหน่งที่จะเซฟไฟล์ ถูกกำหนดไว้ใน settings.py ซึ่งตำแหน่งนั้นจะแปรไปตามค่าชื่อ MEDIA_ROOT ที่กำหนดไว้ หรือก็คือ fs.location จะเป็นที่ตั้งนี้
        pdf_path = os.path.join(fs.location, pdf_filename) # สร้างเส้นทางสำหรับไฟล์ PDF.
        # print("pdf_path = " + pdf_path) => C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\test2.pdf (ปล.test2คือ เราใส่ pdf ชื่อ test2.pdf มา) 
        image_paths = convert_pdf_to_images(pdf_path) # แปลงไฟล์ PDF เป็นรูปภาพ และได้รับเส้นทางของรูปภาพ.
        # print(image_paths) =>  ['page_1.png', 'page_2.png'] pdfมีหลายหน้า pathก็มีหลายหน้าตาม แต่เราเซฟภาพแค่รูปแรก
        
        try:
            client = pymongo.MongoClient(conn_str)
            print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
        except Exception:
            print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)

        myDb = client["pymongo_demo"]
        myCollection = myDb["demo_collection"]


        # Save the first image as a PNG file (เราเซฟ pdf ไว้ที่ media แต่ Opencv อ่านได้แค่ภาพ เราเลยแปลงจาก pdf เป็น ภาพ ซึ่ง image_path ในที่นี้ก็เป็นตัวแปรของภาพที่ถูกแปลงมาจาก pdf โดยฟังชันแปลงอยู่ด้านบนชื่อ "convert_pdf_to_images" )
        if image_paths:
            # first_page_image_path = image_paths[0] # page_1.png
            # png_path = os.path.join(fs.location, 'output.png') #C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club\media\output.png
            # save_image_as_png(first_page_image_path, png_path) # save_image_as_png(source_path, destination_path) -> เปิด source_path แล้วเซฟเป็นรูป png ตำแหน่งของ ตัวแปร png_path
            # check_text(first_page_image_path)

            page_png_path_url = [] # ตัวแปรนี้ไว้เก็บ path ของ image เพื่อส่งไปยัง frontend ให้ฝั่ง frontend แสดงภาพตามจำนวนหน้า pdf 

            for i, page_image_path in enumerate(image_paths):
                # print(page_image_path) # เก็บชื่อ ไฟลฺ image เอาไว้  , .pdf มีสองหน้าจะ print ออกมาสองรอบ  page_1.png และ  page_2.png
                page_png_path = os.path.join(fs.location, f'page_{i + 1}.png')
                # page_png_path = print path ออกมา สองรอบ ตามจำนวนหน้าในไฟล์ .pdf เช่น C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\page_2.png  และ   C:\Users\User\Documents\Git_ComVi\CardCheck\my_tennis_club\media\page_1.png
                save_image_as_png(page_image_path, page_png_path) # ถ้า pdf ที่ส่งมามีหลายหน้า ก็มาวนลูปเซฟภาพตาม pdf ตรงนี้ 🚀
                

                #  page_image_path = page_1.png (เป็นชื่อภาพ)
                #  fs.location = C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club\media
                #  page_png_path = C:\Users\User\Documents\ปี3\GIT_CardCheck\CardCheck\my_tennis_club\media\page_1.png

                page_png_path_url.append(fs.url(page_image_path))
                #  สร้าง URL สำหรับเข้าถึงไฟล์ 
                # image_url = fs.url(page_image_path)
                # print(image_url) = /media/page_1.png

                #* ตรงนี้เช็ก text แล้ว
                text = check_text(page_image_path)

                #!! นำข้อมูลที่อ่านมา ส่ง เข้าฐานข้อมูล 
                lines = text.splitlines() #  แยกข้อความ text ออกเป็นลิสต์ของบรรทัด แต่ละบรรทัดจะเป็นสตริงแยกต่างหากในลิสต์ lines
                



                #TODO MonGO
                username = request.session.get('username')
                record = myCollection.find_one({"username": username}) 
                # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}
                list_all = record.get('list_all', [])  # ถ้าไม่มีค่า 'list_all' จะกำหนดให้เป็นรายการว่าง



                for line in lines:
                    if len(line) == 0:
                        print("String ว่างเปล่า")
                        continue
                    parts = line.split(' ', 1)
                    # print("parts : ",parts)
                    if len(parts) == 2:
                        number_part, text_part = parts
                        text_part = text_part.replace('-', '').replace('=', '').strip() 
                        subparts = text_part.split(' ', 1)
                        if len(subparts) == 2:
                            first_part, second_part = subparts
                            if '—' in second_part: # แก้ส่วน second ที่บางชื่อจะเป็นแบบนี้ => 64070001 ชื่อ =  HarmonyHub นามสกุล =  — Tranquilwood (ในนามสกุลหรือส่วน second_part มี — ติดอยู่ เลยจำเป็นต้องมีเงื่อนไข เพื่อลบอันนี้ออก)
                                second_part = second_part.split('—', 1)[1].strip()
                            print(number_part, "ชื่อ = ", first_part, "นามสกุล = ", second_part)
                    else:
                        # ถ้าไม่มีข้อมูลในตัวแปร 'number_part' ให้ส่งข้อความแจ้งเตือนกลับ
                        return JsonResponse({'number_part': True})
                    student_number = {
                        "id_number" : number_part+"", # รหัสนักศึกษา
                        "student_firstName": first_part,
                        "student_surName" : second_part,
                        "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
                    }
                    list_all.append(student_number);
                
                    

                    # print("ข้อมูลนศ.ที่จะเก็บลง ฐานข้อมูล => " , student_number) ==> ข้อมูลนศ.ที่จะเก็บลง ฐานข้อมูล =>  {'id_number': '64070254', 'student_firstName': 'Anchisa', 'student_surName': 'Cherdsattayanukul', 'attendance_status': 0}
                    # print(student_number)
            
            myCollection.update_one({"username": username}, {"$set": {"list_all": list_all}})
            


            # return JsonResponse({'page_png_path_url': page_png_path_url , 'allStudent': record_count, 'come':0,"notCome":0 }) # page_png_path_url = [ /media/page_1.png ,  /media/page_2.png ]
            return JsonResponse({'page_png_path_url': page_png_path_url , 'come':0,"notCome":0 }) # page_png_path_url = [ /media/page_1.png ,  /media/page_2.png ]
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


# 💊💊
#* ภาพ 𝗜𝗺𝗮𝗴𝗲
def upload_image(request):
    # หลังจาก Load Image แล้วจะเข้า path นี้

    
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    # print(client.list_database_names())
    
    username = request.session.get('username')
    record = myCollection.find_one({"username": username})

    # ถ้าเท่ากับ 0 คือ ในฐานข้อมูลยังไม่มีรายชื่อใดๆ ซึ่ง เราต้องอัพโหลดก่อน ถึงจะเข้า การอัพโหลดรูปได้
    if len(record.get("list_all")) == 0:
        return JsonResponse({'errorPDF': True})

    if request.method == 'POST' and request.FILES.get('image_file'):
        uploaded_image = request.FILES['image_file']
        fs = FileSystemStorage()
        
        
        # สร้างชื่อภาพให้ไม่เหมือนกัน เพราะลองเหมือนแล้ว หน้าhtmlดันไม่อัพเดตภาพตาม
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f'outputImage_{current_time}.png'
        
        saveImage_path = os.path.join(fs.location, file_name) 
        save_image_as_png(uploaded_image, saveImage_path)
        # print("saveImage_path = " + saveImage_path)
        # print(cv2.imread(saveImage_path))
        text = check_text(file_name) # เช็กข้อความในภาพตรงนี้
        saveImage_url = fs.url(file_name)  # เซฟภาพลงใน outputImage.png

        #⁡⁣⁢⁣TODO ค้นหาแค่ชื่อและนามสกุล จากในภาพตรงนี้ ใช้ทับกับของ 𝗽𝗱𝗳 ไม่ได้เพราะ 𝗽𝗱𝗳 จะมีโครงสร้าง มาให้เลย แต่ 𝗶𝗺𝗮𝗴𝗲 ไม่มี⁡
        # -คิดว่าจะแก้ VideoCapture ให้อัพโหลดภาพลงเครื่อง แล้วมาเข้าฟังชันนี้เลย 
        
        text = is_person_name(text , request)
        response_data = text.content.decode('utf-8')  # แปลง bytes เป็น string
        # => response_data  {"notSureIs": "Imsure", "firstName": "Anchisa", "surName": "Cherdsattayanukul"}
        data_dict = json.loads(response_data)  # แปลง JSON string เป็น Python dictionary
        # JsonResponse({'notSureIs': check_again[1], 'firstName': firstName , 'surName' : surname})

        print("🐚🥥🦀🌊 ", data_dict)

        #  ༘⋆🌷🫧🐱🐾💗 ⋆˙ 
        if data_dict.get("notSureIs") == "Imsure": # มั่นใจชื่อกับนามสกุลมาก
            id_number = chageStatusAttendance(data_dict.get("firstName") , data_dict.get("surName") , True, request) # เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ
            # print(record) # => {'_id': ObjectId('65d4ca7f93805c855c82da41'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Carbon', 'attendance_status': 0}


            return JsonResponse({'saveImage_url': saveImage_url, 'firstName': data_dict.get("firstName"), 'surName': data_dict.get("surName"), "id_number" : id_number})
        elif data_dict.get("notSureIs") == "takeNewPhoto": # takeNewPhoto จับชื่อกับนามสกุลไม่ได้ ให้ถ่ายภาพใหม่
            return JsonResponse({'saveImage_url': saveImage_url, 'newPhoto' : True})
        else: # ไม่มั่นใจ ชื่อ หรือ นามสกุล อย่างใดอย่างนึง 
            id_number = chageStatusAttendance(data_dict.get("firstName") , data_dict.get("surName") , True, request) # เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ
            return JsonResponse({'saveImage_url': saveImage_url, 'firstName': data_dict.get("firstName"), 'surName': data_dict.get("surName"), "id_number" : id_number})


    

            
        return JsonResponse({'error': 'Invalid request'}, status=400)













def check_text(image_name):
    # ได้แก้ให้ image_name คือต้องเป็นชื่อไฟล์ที่อยู่ใน media 
    # ฟังชันนี้ใช้หาตัวอักษรในภาพออกมา โดยตัวอักษรเป็นอังกฤษเท่านั้น ถ้าเป็นภาษาไทยจะอยู่ด้านล่าง("check_text_Thai_Language") ทำไว้เผื่อ แต่ไม่ได้ใช้

    print("Check ตัวอักษร English 🌏🌏🌏🌏")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    print("image_name 🍜 : ", image_name)
    image = cv2.imread("./media/" + image_name)
    # print("image in check text ✅ : ", image) # If output is matrix then image read is successful.  if output is 'None' then either path or name of the image is wrong.

    # ทำการดำเนินการต่อไปที่ต้องการ เช่น ใช้ pytesseract สำหรับการ OCR
    if image is not None:
        # path ไฟล์ภาพนี้จะเอาไว้ ทดลอง
        #! cv2.imwrite('../assets/testImage_Here.png', img)

        # list_dataToDetect = []
        #⁡⁣⁢⁣ แปลงภาพเป็น Grayscale ก่อนที่จะใช้ pytesseract.⁡ เราใช้อันนี้ ก่อนปรับปรุง
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (3,3), 0)
        # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # data_version1 = pytesseract.image_to_string(thresh, lang='eng')
        # print("🚀🚀🚀 thresh แบบเก่าาาาาาาา" , data_version1)
        # list_dataToDetect.append(data_version1)


        # อันใหม่ลองปรับปรุง
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # ทำภาพเป้นขาวดำ
        # สร้างออบเจ็กต์ CLAHE => ใช้เทคนิค Contrast Limited Adaptive Histogram Equalization (CLAHE) เพื่อปรับแสงในภาพให้ดียิ่งขึ้น
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(gray)

        
        # แปลงภาพเป็นสีเทา
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ทำการ Threshold เพื่อแยกตัวอักษรออกจากพื้นหลัง
        _, binary = cv2.threshold(cl1, 128, 255, cv2.THRESH_BINARY_INV)

        # ใช้ Connected Component Analysis เพื่อหาส่วนของตัวอักษร
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

        # สร้าง mask สำหรับตัวอักษร
        mask = np.zeros_like(cl1)

        # ข้าม label 0 ที่เป็น background
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if area > 50:  # กำหนดขนาดขั้นต่ำเพื่อกรอง noise
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # วาดกรอบสี่เหลี่ยมรอบตัวอักษร
                mask[y:y+h, x:x+w] = 255

        # ใช้ mask เพื่อแยกตัวอักษรออกจากภาพต้นฉบับ
        characters = cv2.bitwise_and(cl1, cl1, mask=mask)
        
        # hstack รวมภาพต้นฉบับและภาพหลังจากการปรับแสงเพื่อนำมาแสดงเทียบกัน
        # result = np.hstack((thresh, cl1))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()



        print("")
        print("")
        print("")
        # Perform text extraction
        data_version2 = pytesseract.image_to_string(cl1, lang='eng')
        print("🌴🌴🌴" , data_version2)
        # list_dataToDetect.append(data_version2)



        data_version3 = pytesseract.image_to_string(characters, lang='eng')
        print("🤔🤔🤔" , data_version3)
        # list_dataToDetect.append(data_version3)


        print("")
        






        print("------------ จบการเช็ก ------------")    
    return data_version3






def check_text_For_VideoCapture(image_name):
    # ได้แก้ให้ image_name คือต้องเป็นชื่อไฟล์ที่อยู่ใน media 
    # ฟังชันนี้ใช้หาตัวอักษรในภาพออกมา โดยตัวอักษรเป็นอังกฤษเท่านั้น ถ้าเป็นภาษาไทยจะอยู่ด้านล่าง("check_text_Thai_Language") ทำไว้เผื่อ แต่ไม่ได้ใช้

    print("Check ตัวอักษร English 🌏🌏🌏🌏")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    print("image_name 🍜 : ", image_name)
    image = cv2.imread("./media/" + image_name)
    # print("image in check text ✅ : ", image) # If output is matrix then image read is successful.  if output is 'None' then either path or name of the image is wrong.

    # ทำการดำเนินการต่อไปที่ต้องการ เช่น ใช้ pytesseract สำหรับการ OCR
    if image is not None:
        # path ไฟล์ภาพนี้จะเอาไว้ ทดลอง
        #! cv2.imwrite('../assets/testImage_Here.png', img)

        list_dataToDetect = []
        #⁡⁣⁢⁣ แปลงภาพเป็น Grayscale ก่อนที่จะใช้ pytesseract.⁡ เราใช้อันนี้ ก่อนปรับปรุง
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        data_version1 = pytesseract.image_to_string(thresh, lang='eng')
        print("🚀🚀🚀 thresh แบบเก่าาาาาาาา" , data_version1)
        if data_version1.strip(): # สตริงเปล่าหรือมีแต่ช่องว่าง
            list_dataToDetect.append(data_version1)


        # อันใหม่ลองปรับปรุง
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # ทำภาพเป้นขาวดำ
        # สร้างออบเจ็กต์ CLAHE => ใช้เทคนิค Contrast Limited Adaptive Histogram Equalization (CLAHE) เพื่อปรับแสงในภาพให้ดียิ่งขึ้น
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl1 = clahe.apply(gray)

        
        # แปลงภาพเป็นสีเทา
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ทำการ Threshold เพื่อแยกตัวอักษรออกจากพื้นหลัง
        _, binary = cv2.threshold(cl1, 128, 255, cv2.THRESH_BINARY_INV)

        # ใช้ Connected Component Analysis เพื่อหาส่วนของตัวอักษร
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

        # สร้าง mask สำหรับตัวอักษร
        mask = np.zeros_like(cl1)

        # ข้าม label 0 ที่เป็น background
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if area > 50:  # กำหนดขนาดขั้นต่ำเพื่อกรอง noise
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # วาดกรอบสี่เหลี่ยมรอบตัวอักษร
                mask[y:y+h, x:x+w] = 255

        # ใช้ mask เพื่อแยกตัวอักษรออกจากภาพต้นฉบับ
        characters = cv2.bitwise_and(cl1, cl1, mask=mask)
        
        # hstack รวมภาพต้นฉบับและภาพหลังจากการปรับแสงเพื่อนำมาแสดงเทียบกัน
        # result = np.hstack((thresh, cl1))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()



        print("")
        print("")
        print("")
        # Perform text extraction
        data_version2 = pytesseract.image_to_string(cl1, lang='eng')
        print("🌴🌴🌴" , data_version2)
        if data_version2.strip(): # สตริงเปล่าหรือมีแต่ช่องว่าง
            list_dataToDetect.append(data_version2)
            



        data_version3 = pytesseract.image_to_string(characters, lang='eng')
        print("🤔🤔🤔" , data_version3)
        if data_version3.strip(): # สตริงเปล่าหรือมีแต่ช่องว่าง
            list_dataToDetect.append(data_version3)


        print("")
        






        print("------------ จบการเช็ก ------------")    
    return list_dataToDetect








def check_text_Thai_Language(image_path):
    # เช็กภาษาไทย ไม่ได้ใช้ในเจคนี้แล้ว แต่ทำเสร็จไปแล้ว เลยอยากเก็บไว้
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
    # ฟังชันนี้มีไว้เพื่อ ถ้าอ่านตัวอักษรจากภาพที่ user อัพโหลดมาแล้วเสร็จ จะได้ข้อความยาวๆมา เราก็ต้องมา กรอง เอาชื่อเฉพาะชื่อกับนามสกุล ออกมาจากภาพนั้น แล้วไป ค้นหา ชื่อนศ.คนนี้ใน ฐานข้อมูล จากนั้นเปลี่ยนสถานะใน MongoDB ว่า นศ. คนนี้มาแล้ว
    #! อะไรอะ ไม่เห้นมีใครเรียกใช้เลย
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
    new_record = myCollection.update_one({"student_firstName": firstName}, {"$set": {"attendance_status": 1}})
    record = myCollection.find_one({"student_firstName": firstName})
    print("🍏🍏 record ที่อัพเดตแล้ว")
    print(record) # {'_id': ObjectId('65d36d1794d78286f54ccfcb'), 'name': 'Hello', 'message': 'Welcome to coding 101 with Steve'}

 


    return ""




# 💊💊
# ⁡⁣⁢⁣ฟังชันเช็ก ⁡
def is_person_name(text , request):
    # ฟังนี้ใช้ตรวจหาชื่อคนจาก ข้อความยาวๆ ให้ออกมาเป็น array ที่เก็บคำที่คาดว่าน่าจะเป็นชื่อคน หรือ นามสกุล
    # ถูก image และ viedoCapture เรียกใช้ 

    # print("text : ",text)
    print("🐯 ตรวจหาชื่อคน 🐯")
    # print("request ",request) => request  <WSGIRequest: POST '/upload_image/'>
    
    # ใช้ Regular Expression เพื่อแบ่งข้อความเป็นคำ จาก text ที่เป็น  <class 'str'> จะกลายเป็น <class 'list'>
    words = re.findall(r'\b\w+\b', text)
    print("words : ", words)


    filter_words = []
    for word in words:
        if word == "Date":
            break
        filter_words.append(word)
    
    print("filter_words : ",filter_words)
    words = filter_words 
            

    # สร้าง list สำหรับเก็บชื่อและนามสกุล
    spilt_word_toFind_Name = []
     

    # ตรวจสอบว่าแต่ละคำเป็นชื่อหรือนามสกุล
    for word in words:
        # ตรวจสอบคำที่เป็นชื่อ
        if word.istitle():  # คำที่มีตัวพิมพ์ใหญ่แรกของคำเท่านั้นถือว่าเป็นชื่อ
            spilt_word_toFind_Name.append(word)
        # ตรวจสอบคำที่เป็นนามสกุล
        if word.isupper():  # คำที่มีทุกตัวอักษรเป็นตัวพิมพ์ใหญ่ถือว่าเป็นนามสกุล
            spilt_word_toFind_Name.append(word)
    

    maybe_real_firstNameAndsurName = [] # เก็บคำที่มีโอกาสสูงมากว่าจะเป็น ชื่อ หรือ นามสกุล ทำเพื่อจะเอาไว้ให้เข้าตรวจสอบก่อน
    
    
    # ถ้ามีคำว่า Name Miss Lastname สามคำนี้คือชัวร์มาก ว่าต่อจากนี้จะเป็น ชื่อ และ นามสกุล
    
    # ค้นหาว่าคำตามนี้ไหม #? Miss , Lastname ถ้าใช่ ให้เก็บ คำตัวถัดไปด้วย เพราะ ในบัตรปชช. จะเป็นข้อความต่อไปนี้ Miss แล้วตามด้วยชื่อ แสดงว่าหลัง miss ก็คือชื่อ
    for i in range(len(words) - 1):  # เพื่อป้องกัน Index Error, ลูปถึงตัวก่อนสุดท้าย
        if words[i] in ["Miss", "Lastname"]:
            maybe_real_firstNameAndsurName.append(words[i + 1])
                

    # ค้นหาว่าคำตามนี้ไหม #? Name , Last  
    for i in range(len(words) - 1):  # เพื่อป้องกัน Index Error, ลูปถึงตัวก่อนสุดท้าย
        if words[i] in ["Name", "Last"]:
            maybe_real_firstNameAndsurName.append(words[i + 2])
             
     
    print("🎴🎴 => ก่อนเอาตัวอักษรตัวเดี่ยวออก ", spilt_word_toFind_Name) # ['Thai', 'National', 'ID', 'Card', 'Identification', 'Number', 'Qua', 'Name', 'Miss', 'Sirlkorn', 'Lastname', 'Na', 'Ubon', 'NLA']
  
    #  ลบ คำที่เป็นแค่ พยัญชนะ ตัวเดียวออกจาก array
    deleteAlpha_words = [word for word in words if len(word) > 1 or word.isalpha()]
    print(deleteAlpha_words) # ['9192410919914', 'Thai', 'National', 'ID', 'Card', 'amkrtwakemu', '2097', '02090', '36', 'Identification', 'Number', 'damauasfeana', 'a', 'asnd', 'Qua', 'Name', 'Miss', 'Sirlkorn', 'Lastname', 'Na', 'Ubon', 'iaiuf', '30', 'NLA', '2546']


    new_spilt_word_toFind_Name = [] # ['Identificatien', 'Nurabes', 'BUNNA', 'Name', 'Miss', 'Lastname', 'Maliyam', 'Bate', 'Riri', 'Nov', 'Nov', 'Tad', 'TBAB', 'Pave', 'Expery', 'intummadee', 'Maliyam', 'intummadee']
    for word in spilt_word_toFind_Name:
        if len(word) > 2 and word not in ["Miss", "Name", "Last" , "Lastname", "Identificatien" , "National", "Card", "Thai", "Number" , "Identification"]:
            new_spilt_word_toFind_Name.append(word)
        
    print("🏀")
    print(new_spilt_word_toFind_Name) # ['Sogn', 'TET', 'Sanleehaher', 'Thel', 'Numbor', 'Intummadee', 'Maliyam']


    #! ต่อฐานข้อมูล

    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
     
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]

    username = request.session.get('username') # => test 
    record = myCollection.find_one({"username": username})



    #! Reading but Query by student_firstName
    # record = myCollection.find_one({"student_firstName": firstName}) 
    # print(record) # => {'_id': ObjectId('65d4ca7f93805c855c82da41'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Carbon', 'attendance_status': 0}

    firstName = ""
    surName = ""
    #! Reading the document อ่าน all record
    
    print("---- ༘⋆🌷🫧💭₊˚ෆ ----")
    cursor = record.get("list_all") # => ได้array 1 ตัวที่ข้างในมีรายชื่อนศ.ที่เป็น object เก็บไว้อยู่ [{'id_number': '64070002', 'student_firstName': 'TranquilLingua', 'student_surName': 'Harmonycrest', 'attendance_status': 0}]

    # cursor = myCollection.find()
    for record in cursor:
        for word in new_spilt_word_toFind_Name: # ['𝗤𝘂𝗮', '𝗦𝗶𝗿𝗹𝗸𝗼𝗿𝗻', '𝗨𝗯𝗼𝗻', '𝗡𝗟𝗔']
            if word == str(record.get("student_firstName")): # ตรงนี้เอา array ที่ผ่านการกรองมาแล้ว ไปเช็กกับชื่อที่อยู่ในฐานข้อมูล 
                firstName = word
                # print("student_firstName  " , word)
            if word == str(record.get("student_surName")): # ตรงนี้เอา array ที่ผ่านการกรองมาแล้ว ไปเช็กกับ นามสกุล ที่อยู่ในฐานข้อมูล 
                surName = word
                # print("student_surName  " , word)

    print("🔥 ชื่อของผมก็คือ : ", firstName , "นามสกุลคือ : ", surName)

   


    check_again = []

    #  ['Vesussdidausssisy', 'The', 'Gunso', 'Aes', 'Intummade', 'Maliyam', 'Reiua']
    # 🔥 ชื่อของผมก็คือ :   นามสกุลคือ :  Maliyam


    record_firstName = []
    record_surName = []
    # print("======== 🥇🥇🥇")
    # for items in cursor:
    #     print("ชื่อ => ", items.get("student_firstName") , " นามสกุล => " , items.get("student_surName"))
    #     record_firstName.append(items.get("student_firstName"));
    #     record_surName.append(items.get("student_surName"));

    
    
    if firstName == "":
        print("🎙️🎙️", new_spilt_word_toFind_Name)

        # record_firstName = list(myCollection.find({}, {"student_firstName": 1})) # แสดงแค่ค่า student_firstName เท่านั้น โดย 1 หมายถึงให้แสดงฟิลด์นี้
        similarity_ratio = []
        for word in new_spilt_word_toFind_Name:
            for record in record_firstName:
                res = SequenceMatcher(None, word,record).ratio()
                # print("res =", res)
                if res >= 0.85:
                    # print("word:", word, "record_fistName:", record.get("student_firstName"))
                    similarity_ratio.append(record)
                    firstName = record
                    print(res)
        print("🎙️🎙️ Name : ",similarity_ratio)
        # ถ้าเปรัยบเทียบความต่างแล้ว สรุปก็ไม่ได้สักค่าที่จะใช้ได้ ก็จะไม่ append  
        if len(similarity_ratio) != 0:
            # เราเช็ก FistName มาจากการเทียบด้วย percent แล้ว แต่เรายังไม่มั่นใจ นามสกุล เลยต้องเอานามสกุลไปตรวจสอบอีกที
            # record = myCollection.find_one({"student_firstName": firstName}) # {'_id': ObjectId('65d59171f8d8e5ca03393c15'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Maliyam', 'attendance_status': 0}
            record = myCollection.find_one({"username": username, "list_all.student_firstName": firstName})
            # print(record.get("student_surName"))
            if surName == "":
                check_again.append(record.get("student_surName"))
                check_again.append("surName")

        
    
    if surName == "":
        print("🩴🩴", new_spilt_word_toFind_Name)
        # record_surName = list(myCollection.find({}, {"student_surName": 1}))
        similarity_ratio = []
        for word in new_spilt_word_toFind_Name:
            for record in record_surName:
                res = SequenceMatcher(None, word, record).ratio()
                # print("res =", res)
                if res >= 0.85:
                    # print("word:", word, "record_surName:", record.get("student_surName"))
                    similarity_ratio.append(record)
                    surName = record
                    print(res)
        print("🩴🩴 surName : ", similarity_ratio)
        # ถ้าเปรัยบเทียบความต่างแล้ว สรุปก็ไม่ได้สักค่าที่จะใช้ได้ ก็จะไม่ append 
        if len(similarity_ratio) != 0:
            # เราเช็ก SurName มาจากการเทียบด้วย percent แล้ว แต่เรายังไม่มั่นใจเรื่อง ชื่อ เลยต้องเอาชื่อไปตรวจสอบอีกที
            # record = myCollection.find_one({"student_surName": surName})
            record = myCollection.find_one({"username": username, "list_all.student_surName": surName})
            print(record)
            if firstName == "":
                check_again.append(record.get("student_firstName"))
                check_again.append("firstName")

        
    

    print("🔥 ชื่อของผมก็คือ : ", firstName , "นามสกุลคือ : ", surName)
    
    

    # มีส่วนที่ไม่แน่ใจ แค่ ชื่อ หรือ นามสกุล
    if len(check_again) != 0: 
        print("🃜🃚🃖🃁🂭🂺 ไม่แน่ใจ " , check_again[1] , " : " , check_again[0]) # 🃜🃚🃖🃁🂭🂺 ไม่แน่ใจ surName  :  Maliyam
        if check_again[1] == "firstName":
            return JsonResponse({'notSureIs': check_again[1], 'firstName': check_again[0] , 'surName' : surName})
        elif check_again[1] == "surName":
            return JsonResponse({'notSureIs': check_again[1], 'firstName': firstName , 'surName' : check_again[0]})
    
    
    if firstName != "" and surName != "" and len(check_again) == 0:
        # มั่นใจมากๆๆ เพราะได้ทั้งชื่อ และ นามสกุล
        # record = myCollection.find_one({"student_firstName": firstName}) 
        record = myCollection.find_one({"username": username, "list_all.student_firstName": firstName})
        # print(record) # => {'_id': ObjectId('65d4ca7f93805c855c82da41'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Carbon', 'attendance_status': 0}

        return JsonResponse({'notSureIs': "Imsure", 'firstName': firstName , 'surName' : surName})

    # เราไม่มั่นใจสักตัว ไม่ได้ทั้งชื่อและนามสกุล เลยจะบอกให้ ผู้ใช้ ถ่ายภาพใหม่ 
    else: # firstName == "" and surName == "":
        return JsonResponse({'notSureIs': "takeNewPhoto"})



def is_person_name_Video(textList, username, record):
    print("🌈 is_person_name_Video 🌈")

    cursor = record.get("list_all")
    firstName = ""
    surName = ""

    similarity_ratio=[]
    # หา ชื่อก่อน เพราะ ต้องเปรียบเทียบแต่ละคำใน db คือมันทำพร้อมกันไม่ได้
    for text in textList:
        words = re.findall(r'\b\w+\b', text) # words ได้ลิสมา จากตอนแรกเป็นสตริงยาวๆของ text
        for data in cursor: # data = {'_id': ObjectId('65d59171f8d8e5ca03393c15'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Maliyam', 'attendance_status': 0}
            # SequenceMatcher = เปรียบเทียบความคล้ายคลึงกันระหว่างสองสตริง (string)
            for word in words:
                res = SequenceMatcher(None, word, data.get("student_firstName")).ratio()
                # print("res =", res)
                if res >= 0.85:
                    # print("word:", word, "record_surName:", record.get("student_surName"))
                    similarity_ratio.append(data.get("student_firstName"))
                    firstName = data.get("student_firstName")
                    print("res ค่าเปรียบเทียบได้เท่ากับ = " , res)


    # อันนี้เช็กนามสกุลฮ๊าฟฟฟ
    for text in textList:
        words = re.findall(r'\b\w+\b', text) # words ได้ลิสมา จากตอนแรกเป็นสตริงยาวๆของ text
        for data in cursor: # data = {'_id': ObjectId('65d59171f8d8e5ca03393c15'), 'id_number': '64070257', 'student_firstName': 'Intummadee', 'student_surName': 'Maliyam', 'attendance_status': 0}
            # SequenceMatcher = เปรียบเทียบความคล้ายคลึงกันระหว่างสองสตริง (string)
            for word in words:
                res = SequenceMatcher(None, word, data.get("student_surName")).ratio()
                # print("res =", res)
                if res >= 0.85:
                    # print("word:", word, "record_surName:", record.get("student_surName"))
                    similarity_ratio.append(data.get("student_surName"))
                    surName = data.get("student_surName")
                    print("res ค่าเปรียบเทียบได้เท่ากับ = " , res)
    

    
    print("🩴🩴 firstName : ", firstName)
    print("🩴🩴 surName : ", surName)

    if firstName != "" and surName != "":
        return JsonResponse({'notSureIs': "Imsure", 'firstName': firstName , 'surName' : surName})
    else:
        return JsonResponse({'notSureIs': "takeNewPhoto"})





# 💊💊
def chageStatusAttendance(firstName , surName , isCome, request):
    # ฟังชันนี้มีไว้เพื่อ เปลี่ยนสถานะ ของนักศึกษา ว่า มาเข้าสอบไหม
    print("˙✧˖°📷 ⋆｡˚꩜  เข้าฟังชันเปลี่ยนสถานะการเข้าเรียนของ ", firstName , surName , " มาเข้าสอบไหม = " , isCome)

    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)

    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]

    username = request.session.get('username')
    record = myCollection.find_one({"username": username})

    if isCome == True:
        # ได้รับชื่อและนามสกุลมา วิธีคือ ให้หาเรดคอร์ดที่ตรงตามชื่อและนามสกุลแล้วเปลี่ยนสถานะ จากนั้นก้ส่ง idNumberกลับไปด้วย เพราะฝั่งหน้าเว็บเราใช้
        for items in record.get("list_all"):
            if((items.get("student_firstName")==firstName) and (items.get("student_surName")==surName)):
                try:
                    myCollection.update_one(
                    {"username": username, "list_all.id_number": items.get("id_number")},
                    {"$set": {"list_all.$.attendance_status": 1}} # $ ใช้ในการอ้างถึง element ใน list_all ที่ตรงกับเงื่อนไขค้นหา ซึ่งคือ list_all.id_number เท่ากับ student_id.
                    )
                    return items.get("id_number")
                except Exception as e:
                    print(f"An error occurred: {e}") # f , f-string , formatted string literals = ช่วยให้การใส่ค่าตัวแปรลงในสตริง
                    return JsonResponse({'error': f'มีเหตุขัดข้องในการอัพเดตข้อมูลลงฐานข้อมูล ' + {e}}, status=500)
 




# 💊💊
def clearRecord(request):
    # ฟังชันนี้มีไว้เพื่อ drop รายชื่อทั้งหมดออกจากฐานข้อมูล
    print("clearRecorddddddddddddddddddddddddd 🏳‍🌈")
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]

    username = request.session.get('username')
    # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}

    myCollection.update_one({"username": username}, {"$set": {"list_all": []}})


    return HttpResponse("Hi")

def add_image_to_pdf(pdf_filename, images):
    # เป็นฟังชันสำหรับ สร้าง pdf จากรูปภาพ
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    for image in images:
        c.drawImage(image, 0, 0, width=letter[0], height=letter[1])
        c.showPage()

    c.save()





# ตัวแปรกับฟังชันด้านล่าง ไว้ใช้สำหรับ การใช้เมาส์คลิ๊กไปที่ video
ix, iy = -1, -1
mode_Click = False
width, height = 640, 480  # กำหนดค่าเริ่มต้นหรือค่าที่ต้องการให้ width และ height
def click_photograph(event, x, y, flags, param):
    global ix, iy, drawing, mode_Click

    if event == cv2.EVENT_LBUTTONDOWN:
        if width-140 <= x <= width-10 and height-50 <= y <= height-10:
            # print("Capture Photo ♛♛")
            mode_Click = True



    
# 💊💊
def VideoCapture(request):
# ฟังชันนี้คือ ฟันชันถ่ายวิดิโอ ที่จะมีปุ่มกดถ่ายภาพ อยู่ใน fram video ให้เอาเมาส์ไปคลิ๊ก ส่วนวิธีปิด video คือกด esc

    print("VideoCapture 🏰🏰₊˚⊹♡🎠✨")
    

    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    # print(client.list_database_names())
    

    username = request.session.get('username')
    record = myCollection.find_one({"username": username}) 
    # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}


    # ถ้าเท่ากับ 0 คือ ในฐานข้อมูลยังไม่มีรายชื่อใดๆ ซึ่ง เราต้องอัพโหลดก่อน ถึงจะเข้า การอัพโหลดรูปได้
    if record.get('list_all', []) == 0:
        return JsonResponse({'errorPDF': True})

    global mode_Click  # Declare mode_Click as a global variable

    print("VideoCapture click 🌿🌿" )
    cap = cv2.VideoCapture(0)

    # ดึงค่าความละเอียดสูงสุดของกล้อง
    max_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    max_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ตั้งค่าความละเอียดของวิดีโอให้เป็นค่าสูงสุด
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, max_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, max_height)
    print(f"Resolution set to: {max_width}x{max_height}")

    
    cv2.namedWindow("CardCheck")
    cv2.setMouseCallback("CardCheck", click_photograph)
    # กำหนดขนาดหน้าต่าง video
    
    firstName = "FirstName: "
    surName = "SurName: "
    statusCheck = ""
    color = (255, 0, 0)

    while(True):
        # Take each frame
        ret, frame = cap.read()

        if not ret:
            return HttpResponse("Failed to capture image", status=500)

        # Flip the frame (ซ้ายขวา) ไม่เอาแล้วเพราะถ้า flip ภาพปชช.ก็จะกลับซ้ายขวาตาม ทำให้ จับ text ไม่ได้
        # frame = cv2.flip(frame, 1)
        

        height, width, channels = frame.shape # height = 480 , width =  640
        # Draw a rectangle - top-left at (50,50), bottom-right at (200,200) , (0, 255, 0) = color in BGR format
        # cv2.rectangle(frame, (50, 50), (width-50, height-50), (0, 255, 0), 2)

        # ⁡⁣⁢⁢​‌‌‍สร้างปุ่มถ่ายภาพ
        # Draw a rectangle กว้าง 130 สูง 40
        cv2.rectangle(frame, (width-140, height-50), (width-10, height-10), (255, 255, 255), -1)
        cv2.putText(frame, "Capture Photo", (width-120, height-25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(frame, f"{statusCheck}", (10, height-35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(frame, f"{firstName} {surName}", (10, height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, ), 1)


        # Display the resulting frame
        cv2.imshow('CardCheck', frame)

        # ถ้าเป็น true คือ คลิ๊กที่ปุ่ม capture Photo
        if mode_Click == True:
            print("จับภาพ ༼ つ ◕_◕ ༽つ🍰🍔🍕")
            
            cv2.imwrite('./media/testImage.png', frame)
            
            text = check_text_For_VideoCapture("testImage.png") # เช็กข้อความในภาพตรงนี้
            text = is_person_name_Video(text , username , record)
            response_data = text.content.decode('utf-8')  # แปลง bytes เป็น string
            data_dict = json.loads(response_data)  # แปลง JSON string เป็น Python dictionary
            # JsonResponse({'notSureIs': check_again[1], 'firstName': firstName , 'surName' : surname})
            # print(data_dict)
            

            #  ༘⋆🌷🫧🐱🐾💗 ⋆˙ 
            if data_dict.get("notSureIs") == "Imsure": # มั่นใจชื่อกับนามสกุลมาก
                chageStatusAttendance(data_dict.get("firstName") , data_dict.get("surName") , True , request) # เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ
                print(" # เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ ")
                firstName = firstName + data_dict.get("firstName")
                surName = surName + data_dict.get("surName")
                statusCheck = "Pass"
                color = (0, 255 , 0)

                
            elif data_dict.get("notSureIs") == "takeNewPhoto": # takeNewPhoto จับชื่อกับนามสกุลไม่ได้ ให้ถ่ายภาพใหม่
                # ค่าที่ได้ = {'notSureIs': 'takeNewPhoto'}
                print(" # takeNewPhoto จับชื่อกับนามสกุลไม่ได้ ให้ถ่ายภาพใหม่ ")
                statusCheck = "Please take a new photo."
                color = (0, 0 , 255)

                
            else: # ไม่มั่นใจ ชื่อ หรือ นามสกุล อย่างใดอย่างนึง 
                chageStatusAttendance(data_dict.get("firstName") , data_dict.get("surName") , True , request) # เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ
                print("# เปลี่ยนสถานะให้นักศึกษา มาเข้าสอบ")
                firstName = firstName + data_dict.get("firstName")
                surName = surName + data_dict.get("surName")
                statusCheck = "Pass"
                color = (0, 255 , 0)

                
            mode_Click = False




        if cv2.waitKey(5) & 0xFF == 27: # กด esc เพื่อ stop video
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return HttpResponse("ปิดกล้องเรียบร้อย", status=200)




# 💊💊
def upload_excel(request):
    # ฟังชันนี้คือ user อัพโหลดไฟล์ excel จากหน้าบ้าน แล้วจะมาเข้าฟังชันนี้เพื่อ เก็บรายชื่อจาก excel เข้า MongoDB
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        if excel_file and excel_file.name.endswith('.xlsx'):
            
            data = pd.read_excel(excel_file) # Read data from Excel file into a DataFrame using pandas


            # ! เชื่อม DB
            try:
                client = pymongo.MongoClient(conn_str)
                print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
            except Exception:
                print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
            myDb = client["pymongo_demo"]
            myCollection = myDb["demo_collection"]
            username = request.session.get('username')
            record = myCollection.find_one({"username": username})
            list_collect = []

            # สร้างลิสต์เพื่อเก็บข้อมูลแต่ละคอลัมน์ แล้วแยกชื่อ รหัส นามสกุลออกจากกัน
            column1 = data.iloc[:, 0].tolist()  # Extracting data from the first column
            column2 = data.iloc[:, 1].tolist()  # Extracting data from the second column
            column3 = data.iloc[:, 2].tolist()  # Extracting data from the third column
            
            # แยกข้อมูลในแต่ละบรรทัดและจัดเก็บลงในลิสต์ของแต่ละคอลัมน์
            for i in range(len(column1)):
                student_number = {
                    "id_number" : str(column1[i]), # รหัสนักศึกษา
                    "student_firstName": column2[i],
                    "student_surName" : column3[i],
                    "attendance_status" : 0, # 0 คือ ไม่ได้เข้าสอบ , 1 = นักศึกษาเข้าสอบแล้ว
                }
# student_number เช่น {'id_number': 64070257, 'student_firstName': 'Intummadee', 'student_surName': 'Maliyam', 'attendance_status': 0}
                # TODO Insert the document
                list_collect.append(student_number)
             
            try:
                # Update the document with username matching the logged-in user
                result = myCollection.update_one(
                    {"username": username},
                    {"$push": {"list_all": {"$each": list_collect}}}
                )

                if result.modified_count > 0:
                    return JsonResponse({'message': 'File uploaded successfully'})
            except Exception as e:
                print("Failed to update document in MongoDB:", e)
                return HttpResponse("Failed to update document in MongoDB.", status=500)
                                    
            
        else:
            return JsonResponse({'error': 'Invalid file format. Please upload an Excel file.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# 💊💊
def checkStatus(request):
    # ฟังชันนี้คือ เช็กสถานะนักศึกษา ว่ามีนศ.ทั้งหมดกี่คน ใครมาแล้วบ้าง ใครยังไม่มา

    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)


    # Create a DB
    myDb = client["pymongo_demo"]
    # Create a collection
    myCollection = myDb["demo_collection"]
    

    username = request.session.get('username')
    record = myCollection.find_one({"username": username})
    # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}

    record_count = len(record.get("list_all"))
    print(record_count)

    count_come = 0;
    for item in record.get("list_all"):
        if(item.get("attendance_status") == 1):
            count_come+=1;
    # record ex. {'_id': ObjectId('6666f6c1925f9f1cacff1b2c'), 'id_number': '64070001', 'student_firstName': 'HarmonyHub', 'student_surName': 'Tranquilwood', 'attendance_status': 0}


    return JsonResponse({'allStudent': record_count, 'come': count_come,"notCome": record_count-count_come  })


# 💊💊
def search(request):
    # ฟังชันนี้มีเพื่อ ดูข้อมูลของนศ.ตามรหัสนักศึกษาที่ป้อนเข้ามาใน request.GET
    student_id = request.GET.get('studentId', None) # None คือค่าเริ่มต้นถ้าไม่มี studentId , ได้ค่ามาเป้น string ทีมีแต่ตัวเลข
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]
    

    username = request.session.get('username')
    record = myCollection.find_one({"username": username})
    # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}
    
    # เช็กตรวจดูว่าในฐานข้อมูลมี รายชื่อ นศ.ให้ค้นหาไหม
    if(len(record.get("list_all")) == 0):
        return JsonResponse({'error': "countZero"})

    for item in record.get("list_all"):
        # print(item);
        if(item.get('id_number') == student_id):
            print("YEssss °•🪸🪼⁠〰°•  " + student_id)
            response_data = {
                'id_number': item.get('id_number'),
                'student_firstName': item.get('student_firstName'),
                'student_surName': item.get('student_surName'),
                'attendance_status': item.get('attendance_status')
            }
            return JsonResponse(response_data)


    return JsonResponse({'error': "notFound"})




# 💊💊
def edit_status(request):
    # ฟังชันนี้ไว้แก้สถานะให้นักศึกษาคนนี้เป็น มาเข้าสอบ จากการกดไอคอนแก้ไข หลังจาก search หานศ.จากรหัสนศ.
    
    try:
        client = pymongo.MongoClient(conn_str)
        print("เทสเชื่อมต่อMongo ผ่านจ้าา ⚛️⚛️⚛️⚛️⚛️")
    except Exception:
        print("เทสเชื่อมต่อMongo เกิด Error = " + Exception)
    myDb = client["pymongo_demo"]
    myCollection = myDb["demo_collection"]

    student_id = request.GET.get('studentId', None) # None คือค่าเริ่มต้นถ้าไม่มี studentId , ได้ค่ามาเป้น string ทีมีแต่ตัวเลข
    # print("student_id : " , student_id)

    username = request.session.get('username')
    # print(record) -> {'_id': ObjectId('6671b048f77540b98d593b56'), 'username': 'test', 'list_all': []}

    
    # ตรวจสอบก่อนว่า ก่อนการเปลี่ยนแปลง นศ.คนนี้มาแล้วหรือยัง หรือ ยังไม่มา
    old_attendance_status = 0
    record = myCollection.find_one({"username": username})
    for items in record.get("list_all"):
        if(items.get("id_number") == student_id):
            old_attendance_status = items.get("attendance_status")
    print("old_attendance_status : 🏡🏡 ", old_attendance_status)
    
    if old_attendance_status == 0:
        new_attendance_status = 1
    else:
        new_attendance_status = 0

    myCollection.update_one(
    {"username": username, "list_all.id_number": student_id},
    {"$set": {"list_all.$.attendance_status": new_attendance_status}} # $ ใช้ในการอ้างถึง element ใน list_all ที่ตรงกับเงื่อนไขค้นหา ซึ่งคือ list_all.id_number เท่ากับ student_id.
    )
    print("====")
    print("new_attendance_status : 🏡 " , new_attendance_status)

    return HttpResponse(new_attendance_status)