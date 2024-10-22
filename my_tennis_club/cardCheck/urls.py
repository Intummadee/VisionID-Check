from django.urls import path
from . import views

 

urlpatterns = [
    path('testCardCheck/', views.testCardCheck, name='testCardCheck'),
    path('clearRecord/', views.clearRecord, name='clearRecord'),
    # name คือ แค่เป็นการกำหนดชื่อเส้นทาง (URL pattern) เพื่อให้ง่ายต่อการอ้างอิงใน code อื่น ๆ
    # views.cardCheck คือ  function ที่จะถูกเรียกใช้เมื่อมีการเรียก URL '/cardCheck/'. ctrl + คลิ๊ก เข้าไปดูได้
    # http://127.0.0.1:8000/cardCheck/ 
    path('cardCheck/', views.cardCheck, name='cardCheck'),
    # path('MainPage/', views.MainPage, name='MainPage'),
    path('VideoCapture/', views.VideoCapture, name="VideoCapture"),
    path('upload_and_convert_pdf/', views.upload_and_convert_pdf, name='upload_and_convert_pdf'),  
    path('upload_image/', views.upload_image, name='upload_image'),
    path('createImageTable/', views.createImageTable, name='createImageTable'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('checkStatus/', views.checkStatus, name='checkStatus'),
    path('search/', views.search, name='search'),
    path('edit_status/', views.edit_status, name='edit_status'),
    path('', views.MainPage, name='MainPage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]