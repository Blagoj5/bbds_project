# Generated by Django 3.0 on 2019-12-15 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingprograms', '0008_auto_20191214_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='programs',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]