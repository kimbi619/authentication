# Generated by Django 4.2.1 on 2023-07-07 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gce", "0002_certificate_institution_admissionrequirement"),
    ]

    operations = [
        migrations.RenameField(
            model_name="institution",
            old_name="institution",
            new_name="name",
        ),
    ]
