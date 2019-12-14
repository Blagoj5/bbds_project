from django.db import models
from django.utils.text import slugify

from django.db import models
from datetime import datetime

class Programs(models.Model):
    athlete_name = models.CharField(max_length=50)
    athlete_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    program_name = models.CharField(max_length=50)
    program_category = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200,unique=True, null=False)
    is_published = models.BooleanField(default=False)
    list_date = models.DateField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'

    def __str__(self):
        return self.athlete_name + "'s "+ self.program_category + " " + self.program_name

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.athlete_name + " "  + self.program_category + " " + self.program_name)
        return super().save(*args, **kwargs)

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
        return self.program_id.athlete_name + "'s " + self.program_id.program_name + ' ' + self.day_title + 'Day ' + str(self.for_day)
