# Generated by Django 4.2.6 on 2023-11-18 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='new_believer_school',
            field=models.BooleanField(blank=True, default='', max_length=255, null=True),
        ),
    ]
