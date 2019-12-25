from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Programs(models.Model):
    athlete_name = models.CharField(max_length=50)
    athlete_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    program_name = models.CharField(max_length=50)
    program_category = models.CharField(max_length=50)
    program_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    users = models.ManyToManyField(
        User, 
        through='Program_User',
        through_fields=('program', 'user'),
        blank=True,
    )
    slug = models.SlugField(max_length=200,unique=True, null=False)
    is_published = models.BooleanField(default=False)
    list_date = models.DateField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'program'
        verbose_name_plural = 'programs'
        constraints = [
            models.CheckConstraint(check=models.Q(program_duration__gt=0), name='program_duration_gt_0'),
            models.CheckConstraint(check=models.Q(program_duration__lte=9), name='program_duration_lte_9'),
        ]

    def __str__(self):
        return self.athlete_name + "'s "+ self.program_category + " " + self.program_name

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.athlete_name + " "  + self.program_category + " " + self.program_name)
        return super().save(*args, **kwargs)

class Program_User(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    # defint string method in order to return proper name 


class Program(models.Model):
    program_id = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    for_day = models.PositiveSmallIntegerField(blank=False)
    week = models.PositiveSmallIntegerField(blank=False)
    day_title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
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
            models.CheckConstraint(check=models.Q(for_day__lte=7), name='for_day_lte_7'),
            models.CheckConstraint(check=models.Q(week__gt=0), name='week_gt_0'),
            models.CheckConstraint(check=models.Q(week__lte=9), name='week_lte_9'),
        ]
    def __str__(self):
        return self.program_id.athlete_name + "'s " + self.program_id.program_name + ' ' + self.day_title + 'Day ' + str(self.for_day)
