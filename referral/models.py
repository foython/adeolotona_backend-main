from django.db import models
import uuid
from accounts.models import UserProfile
# Create your models here.


class Referral(models.Model):
    referred_by  = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, 
            blank=True, related_name='referred_users')
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)


    def save(self, *args, **kwargs):
            if not self.referral_code:
                # Generate a unique referral code here (e.g., using UUID or a custom function)
                self.referral_code = generate_unique_referral_code() 
            super().save(*args, **kwargs)



def generate_unique_referral_code():
    return str(uuid.uuid4())[:8].upper() 