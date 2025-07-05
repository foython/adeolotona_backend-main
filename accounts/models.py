from django.db import models
from django.contrib.auth.models import User
import random
import string





class HairPhoto(models.Model):
    front = models.ImageField(upload_to="hair_photos")
    back = models.ImageField(upload_to="hair_photos")
    up_front = models.ImageField(upload_to="hair_photos")



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20, blank=True, null=True)

    # otp related
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(default=0)


    # subscription related
    is_subscribed = models.BooleanField(default=False)
    subsciption_expires_on = models.DateTimeField(blank=True, null=True)
    subscription_status = models.CharField(max_length=100, default="freemium")
    subscription_id = models.CharField(max_length=100, blank=True, null=True)

    # provider
    auth_provider = models.CharField(max_length=20, default="normal")



    # on boarding data
    hair_porosity = models.CharField(max_length=100, blank=True, null=True)
    hair_texture = models.CharField(max_length=100, blank=True, null=True)
    hair_density = models.CharField(max_length=100, blank=True, null=True)
    hair_growth_rate = models.CharField(max_length=100, blank=True, null=True)
    hair_concerns = models.CharField(max_length=100, blank=True, null=True)
    current_hair_product = models.CharField(max_length=100, blank=True, null=True)
    current_conditioner = models.CharField(max_length=100, blank=True, null=True)
    current_styling_product = models.CharField(max_length=100, blank=True, null=True)
    current_product_satisfection = models.CharField(max_length=100, blank=True, null=True)
    hair_goals = models.CharField(max_length=100, blank=True, null=True)
    hair_photos = models.ManyToManyField(HairPhoto, blank=True) 


    # in app hair data
    hair_elasticity = models.CharField(max_length=100, blank=True, null=True)
    hair_thickness = models.CharField(max_length=100, blank=True, null=True)
    checmical_treatment = models.CharField(max_length=100, blank=True, null=True)
    heat_tool_usage = models.CharField(max_length=100, blank=True, null=True)
    scalp_condition = models.CharField(max_length=100, blank=True, null=True)
    climate = models.CharField(max_length=100, blank=True, null=True)
    water_type = models.CharField(max_length=100, blank=True, null=True)
    dietary_factors = models.CharField(max_length=100, blank=True, null=True)
    lifestyle_factors = models.CharField(max_length=100, blank=True, null=True)
    styling_habits = models.CharField(max_length=100, blank=True, null=True)
    styling_method_regularly_used = models.CharField(max_length=100, blank=True, null=True)
    how_often_wear_protective_wears = models.CharField(max_length=100, blank=True, null=True)




    def generate_otp(self):
        otp = ''.join(random.choices(string.digits, k=4))
        self.otp = otp
        self.save()
        return otp
    

    def __str__(self):
        return self.user.username