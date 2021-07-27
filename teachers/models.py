from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True)
    room_number = models.CharField(max_length=15)
    subjects_taught = models.ManyToManyField(Subject)

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        return self.email

    def __str__(self):
        return self.get_full_name()
