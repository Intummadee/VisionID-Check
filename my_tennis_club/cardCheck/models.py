from django.db import models


# Navigate to the /my_tennis_club/ folder and run this command --> py manage.py makemigrations members

# กรณีอยากดูตาราง พิมคำสั่ง python manage.py sqlmigrate cardCheck 0001

class cardCheck(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)