# Generated by Django 3.0 on 2019-12-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainingprograms', '0009_auto_20191215_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='programs',
            name='program_duration',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='programs',
            constraint=models.CheckConstraint(check=models.Q(program_duration__gt=0), name='program_duration_gt_0'),
        ),
        migrations.AddConstraint(
            model_name='programs',
            constraint=models.CheckConstraint(check=models.Q(program_duration__lte=9), name='program_duration_lte_9'),
        ),
    ]
