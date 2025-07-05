from django.db import models
from django.contrib.auth.models import User
from accounts.models import HairPhoto


# class WashDay(models.Model):
#     step_name = models.CharField(max_length=100, blank=True, null=True)
#     step_description = models.TextField(blank=True, null=True)


# class Routine(models.Model):
#     daily_routine = models.TextField(blank=True, null=True)
#     washday = models.ManyToManyField(WashDay, blank=True, null=True)
#     monthly_routine = models.TextField(blank=True, null=True)


# class HairAnalysis(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     analysis_report = models.TextField(blank=True, null=True)
#     tips = models.TextField(blank=True, null=True)

#     routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

#     hair_photos = models.ForeignKey(HairPhoto, blank=True, null=True, on_delete=models.CASCADE)

#     timestamp = models.DateTimeField(auto_now_add=True)




# class HairPhoto(models.Model):
#     front = models.ImageField(upload_to='hair_photos/')
#     back = models.ImageField(upload_to='hair_photos/')
#     up_front = models.ImageField(upload_to='hair_photos/')

class HairType(models.Model):
    classification = models.CharField(max_length=10)
    description = models.TextField()

class Characteristics(models.Model):
    length_estimate = models.CharField(max_length=20)
    scalp_visibility = models.TextField()
    protective_style = models.CharField(max_length=50, blank=True, null=True)

class HairCondition(models.Model):
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    insight = models.TextField()

class AnalysisReport(models.Model):
    hair_type = models.OneToOneField(HairType, on_delete=models.CASCADE)
    characteristics = models.OneToOneField(Characteristics, on_delete=models.CASCADE)
    health_score = models.IntegerField()
    conditions = models.ManyToManyField(HairCondition)

class HairTip(models.Model):
    content = models.TextField()

class RoutineStep(models.Model):
    step_name = models.CharField(max_length=100)
    step_description = models.TextField()

class HairRoutine(models.Model):
    daily_routine = models.JSONField()
    monthly_routine = models.JSONField()
    washday_steps = models.ManyToManyField(RoutineStep)

class HairAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    analysis_report = models.ForeignKey(AnalysisReport, on_delete=models.CASCADE)
    tips = models.ManyToManyField(HairTip)
    routine = models.ForeignKey(HairRoutine, on_delete=models.CASCADE)
    hair_photos = models.ForeignKey(HairPhoto, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

