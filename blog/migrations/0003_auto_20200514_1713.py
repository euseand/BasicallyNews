# Generated by Django 3.0.6 on 2020-05-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200514_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='email',
        ),
        migrations.AlterField(
            model_name='post',
            name='time_stamp',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]