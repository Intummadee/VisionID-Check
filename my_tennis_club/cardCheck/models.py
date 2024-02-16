from django.db import models

# กรณีอยากดูตาราง พิมคำสั่ง python manage.py sqlmigrate cardCheck 0001

class cardCheck(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)