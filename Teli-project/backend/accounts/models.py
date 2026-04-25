from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms



class role(models.Model):
    CHOICES = (
                ('superadmin', 'Superadmin'),
                ('manager', 'Manager'),
                ('agent', 'Agent'), 
            )
    name = models.CharField(max_length= 20, blank = False)
    authorisation = models.CharField(max_length= 30, choices = CHOICES)

class Administrator(AbstractUser, models.Model):
    tel = models.CharField(max_length = 20, blank = True)
    address = models.CharField(max_length = 255, blank = True)
    role = models.ForeignKey(role, on_delete=models.CASCADE, null = False)

    def __str__(self):
        return f"nom : {self.username}"
    







