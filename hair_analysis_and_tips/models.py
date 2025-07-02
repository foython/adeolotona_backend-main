from django.db import models
from django.contrib.auth.models import User
from accounts.models import HairPhoto


class WashDay(models.Model):
    step_name = models.CharField(max_length=100, blank=True, null=True)
    step_description = models.TextField(blank=True, null=True)


class Routine(models.Model):
    daily_routine = models.TextField(blank=True, null=True)
    washday = models.ManyToManyField(WashDay, blank=True, null=True)
    monthly_routine = models.TextField(blank=True, null=True)


class HairAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    analysis_report = models.TextField(blank=True, null=True)
    tips = models.TextField(blank=True, null=True)

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)

    hair_photos = models.ForeignKey(HairPhoto, blank=True, null=True, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
