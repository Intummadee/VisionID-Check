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
    # cap = cv2.VideoCapture(0)
    # while True:
    #     # Take each frame
    #     _, frame = cap.read()
    #     # Convert BGR to HSV
    #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     # define range of blue color in HSV
    #     lower_blue = np.array([110, 50, 50])
    #     upper_blue = np.array([130, 255, 255])

    #     # Threshold the HSV image to get only blue colors
    #     mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #     # Bitwise-AND mask and original image
    #     res = cv2.bitwise_and(frame, frame, mask=mask)

    #     cv2.imshow('frame', frame)
    #     cv2.imshow('mask', mask)
    #     cv2.imshow('res', res)
    #     k = cv2.waitKey(5) & 0xFF
    #     if k == 27:
    #         break
    # cv2.destroyAllWindows()

    # # Convert the frame to base64 encoding
    # _, buffer = cv2.imencode('.jpg', frame)
    # frame_base64 = base64.b64encode(buffer).decode('utf-8')

    return render(request, 'plot.html', {
        # 'frame_base64': frame_base64,
    })