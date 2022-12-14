# Generated by Django 3.1.7 on 2021-05-13 14:35

from django.db import migrations, models
import login.models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('roll_no', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=255)),
                ('student_email', models.EmailField(max_length=255, unique=True, validators=[login.models.valid_email])),
                ('date_of_entry', models.DateField()),
                ('time_of_entry', models.TimeField()),
                ('warden_name', models.CharField(max_length=256)),
                ('warden_email', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Record_Table',
            },
        ),
    ]
