# Generated by Django 5.0.6 on 2024-05-26 18:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Aut", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="people",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="static/images/"),
        ),
        migrations.AddField(
            model_name="user",
            name="father_name",
            field=models.CharField(
                default=django.utils.timezone.now,
                max_length=80,
                verbose_name="Отчество",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=50, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=80, verbose_name="Фамилия"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
