# Generated by Django 4.2.2 on 2023-06-23 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('craftapi', '0002_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.CharField(max_length=5000),
        ),
    ]
