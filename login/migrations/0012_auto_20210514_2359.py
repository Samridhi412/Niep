# Generated by Django 3.1.7 on 2021-05-14 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_user_student_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student_no',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.customuser'),
        ),
    ]
