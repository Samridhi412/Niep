# Generated by Django 3.1.7 on 2021-05-15 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_auto_20210515_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='warden_email',
        ),
    ]
