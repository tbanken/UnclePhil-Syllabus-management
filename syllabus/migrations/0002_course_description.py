# Generated by Django 3.1.3 on 2020-12-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syllabus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.CharField(default='', max_length=400),
        ),
    ]