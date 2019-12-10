from django.db import models

from django.db import models
from datetime import datetime

class Programs(models.Model):
    programName = models.CharField(max_length=50)
    programCategory = models.CharField(max_length=50)
    athleteName = models.CharField(max_length=50)
    athletePhoto = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    is_published = models.BooleanField(default=False)
    list_date = models.DateField(default=datetime.now, blank=True)
    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'
    def __str__(self):
        return self.athleteName + "'s " + self.programName

class Program(models.Model):
    program_id = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    for_day = models.PositiveSmallIntegerField()
    day_title = models.CharField(max_length=50)
    ex1 = models.CharField(max_length=50)
    reps1 = models.CharField(max_length=25, default='3x10')
    ex2 = models.CharField(max_length=50)
    reps2 = models.CharField(max_length=25, default='3x10')
    ex3 = models.CharField(max_length=50)
    reps3 = models.CharField(max_length=25, default='3x10')
    ex4 = models.CharField(max_length=50, blank=True)
    reps4 = models.CharField(max_length=25, blank=True)
    ex5 = models.CharField(max_length=50, blank=True)
    reps5 = models.CharField(max_length=25, blank=True)
    ex6 = models.CharField(max_length=50, blank=True)
    reps6 = models.CharField(max_length=25, blank=True)
    ex7 = models.CharField(max_length=50, blank=True)
    reps7 = models.CharField(max_length=25, blank=True)
    
    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'program'
        constraints = [
            models.CheckConstraint(check=models.Q(for_day__gt=0), name='for_day_gt_0'),
        ]
    def __str__(self):
        return self.day_title + 'Day ' + str(self.for_day)
