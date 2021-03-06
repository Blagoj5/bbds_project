# Generated by Django 3.0 on 2019-12-09 19:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programName', models.CharField(max_length=50)),
                ('programCategory', models.CharField(max_length=50)),
                ('athleteName', models.CharField(max_length=50)),
                ('athletePhoto', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d')),
                ('is_published', models.BooleanField(default=False)),
                ('list_date', models.DateField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'program',
                'verbose_name_plural': 'programs',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_day', models.PositiveSmallIntegerField()),
                ('day_title', models.CharField(max_length=50)),
                ('ex1', models.CharField(max_length=50)),
                ('reps1', models.CharField(default='3x10', max_length=25)),
                ('ex2', models.CharField(max_length=50)),
                ('reps2', models.CharField(default='3x10', max_length=25)),
                ('ex3', models.CharField(max_length=50)),
                ('reps3', models.CharField(default='3x10', max_length=25)),
                ('ex4', models.CharField(blank=True, max_length=50)),
                ('reps4', models.CharField(blank=True, max_length=25)),
                ('ex5', models.CharField(blank=True, max_length=50)),
                ('reps5', models.CharField(blank=True, max_length=25)),
                ('ex6', models.CharField(blank=True, max_length=50)),
                ('reps6', models.CharField(blank=True, max_length=25)),
                ('ex7', models.CharField(blank=True, max_length=50)),
                ('reps7', models.CharField(blank=True, max_length=25)),
                ('program_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='trainingprograms.Programs')),
            ],
            options={
                'verbose_name': 'program',
                'verbose_name_plural': 'program',
            },
        ),
    ]
