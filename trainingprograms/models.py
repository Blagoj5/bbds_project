from django.db import models
from datetime import datetime

class Programs(models.Model):
    programName = models.CharField(max_length=50)
    programCategory = models.CharField(max_length=50)
    athleteName = models.CharField(max_length=50)
    athletePhoto = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    day = models.PositiveSmallIntegerField(unique=True)
    is_published = models.BooleanField(default=False)
    list_date = models.DateField(default=datetime.now, blank = True)
    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'
    def __str__(self):
        return self.athleteName + "'s " + self.programName

class Program(models.Model):
    program_id = models.ForeignKey(Programs, on_delete=models.CASCADE)
    for_day = models.ForeignKey(Programs, to_field='day', on_delete=models.CASCADE, related_name='for_day')
    day_title = models.CharField(max_length=50)
    ex1 = models.CharField(max_length=50)
    ex2 = models.CharField(max_length=50)
    ex3 = models.CharField(max_length=50)
    ex4 = models.CharField(max_length=50, blank=True)
    ex5 = models.CharField(max_length=50, blank=True)
    ex6 = models.CharField(max_length=50, blank=True)
    ex7 = models.CharField(max_length=50, blank=True)
    reps1 = models.CharField(max_length=25)
    reps2 = models.CharField(max_length=25)
    reps3 = models.CharField(max_length=25)
    reps4 = models.CharField(max_length=25, blank=True)
    reps5 = models.CharField(max_length=25, blank=True)
    reps6 = models.CharField(max_length=25, blank=True)
    reps7 = models.CharField(max_length=25, blank=True)
    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'program'
    def __str__(self):
        return self.day_title + 'Day ' + self.for_day
