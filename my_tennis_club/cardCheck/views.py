from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# 
from io import BytesIO
import base64

# Computer Vision
import numpy as np
import matplotlib.pyplot as plt
import cv2




def testCardCheck(request):
    return HttpResponse("Hello world!")

def cardCheck(request):
    # template = loader.get_template('HomePage.html')
    # return HttpResponse(template.render())
    return HttpResponse("Hello world!")


def plot(request):
    cap = cv2.VideoCapture(0)
    while True:
        #* Take each frame
        _, frame = cap.read()
        #* ภาพถูกแปลงจากรูปแบบสี BGR (Blue, Green, Red) เป็น HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #* define range of blue color in HSV , กำหนดเกณฑ์สีที่สนใจ (Thresholding): กำหนดค่าสีที่ต้องการให้เป็นสีขาว (255) และสีที่ไม่สนใจให้เป็นสีดำ (0) ใน Mask
        # lower_blue = np.array([110, 50, 50])
        # upper_blue = np.array([130, 255, 255])

        #* Threshold the HSV image to get only blue colors, สีน้ำเงินมีค่า Hue อยู่ในช่วง 110-130 องศา ทำให้รู้ว่าเอาสีนํ้าเงิน
        #* lower_blue = ค่าต่ำสุดในช่วงสีที่ต้องการ threshold. , upper: ค่าสูงสุดในช่วงสีที่ต้องการ threshold.
        # mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #* cv2.inRange ทำหน้าที่สร้าง binary mask ที่ให้ค่าสีขาว (255) ในส่วนที่ตรงตามขีดความสูง (threshold) และค่าสีดำ (0) ในส่วนที่ไม่ตรงตามขีดความสูงนั้น.


        #* Bitwise-AND ระหว่าง Mask และ ภาพต้นฉบับ เพื่อให้ได้ภาพที่มีเฉพาะสีที่เราสนใจเท่านั้น.
        # res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()

    #* frame = ภาพสุดท้ายที่ถ่ายกับ Video มาแล้ว 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray Frame', gray_frame)
    cv2.waitKey(1)

    # Convert the frame to base64 encoding
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return render(request, 'plot.html', {
        'frame_base64': frame_base64,
    })