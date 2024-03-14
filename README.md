# CardCheck 



<img width="100%" height="60%" src="https://github.com/Intummadee/CardCheck/blob/main/assets/MainPage.png?raw=true">

<img width="50%" height="60%" src="https://github.com/Intummadee/CardCheck/blob/main/assets/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%99%E0%B8%B1%E0%B8%81%E0%B8%A8%E0%B8%B6%E0%B8%81%E0%B8%A9%E0%B8%B2.png?raw=true">


## 📚 **Initialize** 

สร้าง Environment 
```python -m venv env```

activate Environment 
--> 👉 ```env\Scripts\activate```
ถ้ารันได้จะมีคำว่า (env) ต่อหน้า PS ใน terminal

-สร้างไฟล์ app.py

## ⚡ **Library** 
```
python -m pip install numpy
python -m pip install scipy
python -m pip install matplotlib
python -m pip install opencv-python
python -m pip install opencv-contrib-python
pip install pytesseract
pip install reportlab
python -m pip install pandas
python -mpip install openpyxl

```

-Option กรณีถูก WARNING ให้อัพเดตเวอร์ชั่น
```python -m pip install --upgrade pip```


⚡ Install Django
```python -m pip install Django```

-Option คำสั่ง check ว่าลง django หรือยัง
```django-admin --version```
--> รันแล้วได้ 4.2.10

create Project
```django-admin startproject my_tennis_club```

คำสั่งรัน !!!
```js
env\Scripts\activate
cd my_tennis_club (อย่าลืมว่าต้องอยู่ใน my_tennis_club)
python manage.py runserver
```


```
เปิด Path นี้ --> http://127.0.0.1:8000/MainPage/
```

สร้าง App 
```
python manage.py startapp cardCheck
```

---

# ใช้งาน MongoDB
https://account.mongodb.com/account/login?n=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F65d359c147d94142e1d9fb54&nextHash=%23metrics%2FreplicaSet%2F65d35a0f89492b3df0336104%2Fexplorer%2Fpymongo_demo%2Fdemo_collection%2Ffind&signedOut=true

Source : https://www.youtube.com/watch?v=GJCKIGeK3qc
```JS
python -m pip install "pymongo[srv]"
```


# Upload file
```
pip install pymupdf Pillow
```

---

# Tesseract วิธีทำให้อ่านข้อความภาษาไทย

https://gist.github.com/dogterbox/7c0ed7387a388f5e13afd00f0cb8cd50
ดาวน์โหลด raw file ของเว็บนี้ https://github.com/tesseract-ocr/tessdata_best/blob/main/tha.traineddata ลงในที่ที่เก็บ ```\Tesseract-OCR\tessdata folder```

---

# ฝั่งFrontEnd
-https://github.com/atisawd/boxicons

-https://boxicons.com/

-https://css-loaders.com/progress/

---

## Extension แนะนำให้โหลดใน Vs code สำหรับอ่าน comment 
- Better-comments
- Comment Styler



เข้าไปใน views ที่อยู่ใน cardCheck_project
```
from django.shortcuts import render
from django.http import HttpResponse

def cardCheck(request):
    return HttpResponse("Hello world!")
```

---

-Create a file named ```urls.py``` in the same folder as the views.py file, and type this code in it:
```
from django.urls import path
from . import views

urlpatterns = [
    path('cardCheck/', views.cardCheck, name='cardCheck'),
]
```

---

เข้าไปในไฟล์ ```urls.py``` ภายใน folder  my_tennis_club
```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('cardCheck.urls')), # เส้นทางหลักที่จะ include เส้นทางจาก members.urls
    path('admin/', admin.site.urls),
]
```

---

สร้าง templates
```
cd cardCheck
mkdir templates
cd templates
```
สร้าง ```HomePage.html```
```
<!DOCTYPE html>
<html>
<body>

<h1>Hello World!</h1>
<p>Welcome to my first Django project!</p>

</body>
</html>
```

---


ดูไฟล์ชื่อ ```settings.py``` ในโฟลเดอร์ ```my_tennis_club```  
แล้วแก้ต่อไปนี้  
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cardCheck'
]
```
แล้ว Run ใหม่อีกครั้ง

---

ไปเพิ่มในไฟล์ models.py ในโฟลเดอร์ cardCheck
```
from django.db import models
class cardCheck(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
```

---

แล้วรันใหม่
```python manage.py makemigrations cardCheck```
มีภาพใน assets ชื่อ img-1

## รันคำสั่ง 💥
- เข้าไปรันใน Path CardCheck\my_tennis_club> python manage.py migrate
```
python manage.py migrate
```
## Path ที่ถูกใช้ในเว็บ 🌈
```http://127.0.0.1:8000/MainPage```

---

ดูเรื่องคำสั่ง Insert ข้อมูล ได้ต่อที่ --> https://www.w3schools.com/django/django_insert_data.php




สร้าง Folder เพื่อเก็บไฟล์แยกใน Project templates
```
mkdir templates
mkdir static\css
```

---

## ข้อจำกัด
1. ไฟล์ที่อัพโหลด ต้องเป็น pdf เท่านั้น และ ขนาดตัวอักษรในไฟล์ควรมากกว่า 18
2. ตารางใน excel ควรจะชิดกันให้มากที่สุด เพื่อที่จะได้จับข้อความเป็นประโยคเดียวกัน เช่น  64070257 Hydro Carbon ถ้าแต่ละ column ในตารางห่างกันมากเกินไป ชื่อสามอย่างนี่ก็จะแยกออกจากกันไม่รวมในแถวเดียวกันได้ สามารถดูตัวอย่างภาพได้ใน example_image
3. ภาพที่ได้ต้องมีความชัด มีแสงสว่างเพียงพอ ระยะห่างจากกล่องไม่มากเกินไป หรือ น้อยเกินไป
4. บัตรที่ความเงา อย่าง บัตรประชาชน ไม่ควรถ่ายให้ติดเงามากเกินไป เพราะโปรแกรมจะไม่จับข้อความตรงที่มีเงา

---

# อ้างอิง
-สำหรับ ใช้ computer vision OCR ในการตรวจหาข้อความในภาพ
https://github.com/UB-Mannheim/tesseract/wiki

-MongoDB and Python
https://www.youtube.com/watch?v=GJCKIGeK3qc

-How to Install Tesseract OCR on Windows and use it with Python
https://www.youtube.com/watch?v=GMMZAddRxs8

-Stackoverflow
https://stackoverflow.com/questions/37745519/use-pytesseract-ocr-to-recognize-text-from-an-image
https://stackoverflow.com/questions/21104664/extract-all-bounding-boxes-using-opencv-python


Python – Extract names from string with python Regex
-https://itecnote.com/tecnote/python-extract-names-from-string-with-python-regex/


Python | Similarity metrics of strings
-https://www.geeksforgeeks.org/python-similarity-metrics-of-strings/


using SequenceMatcher.ratio()
-https://www.geeksforgeeks.org/python-similarity-metrics-of-strings/

---
