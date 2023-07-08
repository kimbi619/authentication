# Generated by Django 4.2.1 on 2023-07-07 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gce", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Certificate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "student_name",
                    models.CharField(
                        max_length=256, verbose_name="Name of the student"
                    ),
                ),
                (
                    "subject",
                    models.ImageField(
                        upload_to="images/", verbose_name="gce certificate"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Institution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        max_length=256, verbose_name="name of the institution"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdmissionRequirement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        max_length=256, verbose_name="required subject title"
                    ),
                ),
                (
                    "grade",
                    models.CharField(
                        max_length=256, verbose_name="required grade for the subject"
                    ),
                ),
                (
                    "institution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gce.institution",
                    ),
                ),
            ],
        ),
    ]