from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator 

class OLevelGen(models.Model):
    name = models.CharField(_("student name"), max_length=256, null=False, blank=False)
    subject_count = models.IntegerField(null=False,  validators=[MinValueValidator(4), MaxValueValidator(33)])
    points = models.IntegerField(null=False, validators=[MinValueValidator(4), MaxValueValidator(33)])
    