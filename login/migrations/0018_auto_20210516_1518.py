# Generated by Django 3.1.7 on 2021-05-16 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20210516_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date_of_entry',
            field=models.DateField(unique=True),
        ),
    ]