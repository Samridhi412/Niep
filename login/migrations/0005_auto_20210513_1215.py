# Generated by Django 3.1.7 on 2021-05-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20210513_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userotp',
            name='otp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
