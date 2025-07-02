from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, HairPhoto

class HairPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairPhoto
        fields = ['id', 'front', 'back', 'up_front']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    hair_photos = HairPhotoSerializer(many=True, read_only=True)  # Serialize the many-to-many relationship

    class Meta:
        model = UserProfile
        fields = [
            'user', 
            'full_name', 
            'email', 
            'is_verified', 
            'auth_provider', 
            'otp', 
            'is_subscribed', 
            'subsciption_expires_on', 
            'subscription_status',
            'subscription_id',
            'hair_porosity', 
            'hair_texture', 
            'hair_density', 
            'hair_growth_rate', 
            'hair_concerns', 
            'current_hair_product', 
            'current_conditioner', 
            'current_styling_product', 
            'current_product_satisfection', 
            'hair_goals', 
            'hair_elasticity', 
            'hair_thickness', 
            'checmical_treatment', 
            'heat_tool_usage', 
            'scalp_condition', 
            'climate', 
            'water_type', 
            'dietary_factors', 
            'lifestyle_factors', 
            'styling_habits', 
            'styling_method_regularly_used', 
            'how_often_wear_protective_wears',
            'hair_photos'
        ]
