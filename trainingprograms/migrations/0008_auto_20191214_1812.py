# Generated by Django 3.0 on 2019-12-14 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingprograms', '0007_auto_20191214_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='week',
            field=models.PositiveSmallIntegerField(),
        ),
    ]