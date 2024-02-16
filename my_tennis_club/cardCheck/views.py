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
    print("testCardCheck")
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


    # left = 150 
    # top = 150; 
    # right = 450 
    # bottom = 450; 

    # rectangle_frame = cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3)

    # #* frame = ภาพสุดท้ายที่ถ่ายกับ Video มาแล้ว 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Apply GaussianBlur to reduce noise and help contour detection
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # If the polygon has 4 vertices, it's likely a rectangle
        if len(approx) == 4:
            # Draw the rectangle around the contour
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
    
    # Display the result
    cv2.imshow("Detected Rectangles", frame)
    cv2.waitKey(5) & 0xFF
    cv2.destroyAllWindows()


    # Convert the frame to base64 encoding
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return render(request, 'plot.html', {
        'frame_base64': frame_base64,
    })