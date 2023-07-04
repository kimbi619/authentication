from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator 

class Student(models.Model):
    name = models.CharField(_("student name"), max_length=256, null=False, blank=False)
    
class Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    subject = models.CharField(_("subject title"), max_length=256, null=False, blank=False)
    grade = models.CharField(_("grade for the course"), max_length=1, null=False, blank=True)
    level = models.CharField(_("Ordinary or advanced Level"), max_length=15, null=False, blank=False)
    education = models.CharField(_("Education type, grammar, technical or commercial"), max_length=25, blank=False, null=False)

class Certificate(models.Model):
    student_name = models.CharField(_("Name of the student"), max_length=256)
    subject = models.ImageField(_("gce certificate"), upload_to='images/')