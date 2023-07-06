# Generated by Django 4.2.2 on 2023-07-06 05:58

import datetime
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_otp_date_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator], verbose_name='username'),
        ),
        migrations.AlterField(
            model_name='otp',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 6, 5, 58, 22, 420928, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=12, unique=True, validators=[django.core.validators.MinLengthValidator(12, 'Please Enter 10 digit mobile phone number')]),
        ),
    ]