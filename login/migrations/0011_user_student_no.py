# Generated by Django 3.1.7 on 2021-05-14 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_remove_user_student_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='student_no',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='login.customuser'),
        ),
    ]
