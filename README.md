# CardCheck 
 
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
```
cd my_tennis_club (อย่าลืมว่าต้องอยู่ใน my_tennis_club)
python manage.py runserver
```


สร้าง App 
```
python manage.py startapp cardCheck
```

---

# ใช้งาน MongoDB
Source : https://www.youtube.com/watch?v=GJCKIGeK3qc
```JS
python -m pip install "pymongo[srv]"
```


# Upload file
```
pip install pymupdf Pillow
```

---

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

รันคำสั่ง 
```
python manage.py migrate
```


ดูเรื่องคำสั่ง Insert ข้อมูล ได้ต่อที่ --> https://www.w3schools.com/django/django_insert_data.php




สร้าง Folder เพื่อเก็บไฟล์แยกใน Project templates
```
mkdir templates
mkdir static\css
```

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

---
