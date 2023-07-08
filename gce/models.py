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



class Institution(models.Model):
    name = models.CharField(_("name of the institution"), max_length=256, blank=False, null=False)
    purpose = models.CharField(_("Purpose of the setring requirement"), max_length=256, blank=True, null=True)
    level = models.CharField(_("Level of requirement: Advanced or Ordinary"), max_length=256, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    # @property
    # def requirements(self):
    #     return self.requirements_set.all()

class AdmissionRequirement(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='admission_requirements')
    subject = models.CharField(_("required subject title"), max_length=256, blank=False, null=False)
    grade = models.CharField(_("required grade for the subject"), max_length=256, blank=False, null=False)

    def __str__(self):
        return self.subject + " - " + self.grade



