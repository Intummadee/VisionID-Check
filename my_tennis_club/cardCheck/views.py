from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

# สำหรับแสดงผลรูปภาพบนหน้าเว็บ
from io import BytesIO
import base64

# สำหรับจับข้อความ หรือ ocr
from PIL import Image
import pytesseract


# Computer Vision , OpenCV
import numpy as np
import matplotlib.pyplot as plt
import cv2

 


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
        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(5) & 0xFF == 27: # กด esc เพื่อ stop video
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    #* frame = ภาพสุดท้ายที่ถ่ายกับ Video มาแล้ว  แปลงภาพเป็นภาพขาวดำ
    












    # Convert the frame to a base64 string
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')

    # Return the base64 string as part of the JSON response
    return JsonResponse({'frame_base64': frame_base64})


def MainPage(request):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    img = cv2.imread('../assets/img-1.png')
    # ทำการดำเนินการต่อไปที่ต้องการ เช่น ใช้ pytesseract สำหรับการ OCR
    if img is not None:
        # แปลงภาพเป็น Grayscale ก่อนที่จะใช้ pytesseract.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        print("🌏🌏🌏🌏")
        print(text)

    return render(request, 'MainPage.html', {
        # 'frame_base64': frame_base64,
    })


