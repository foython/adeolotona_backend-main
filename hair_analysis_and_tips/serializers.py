from rest_framework import serializers
from .models import HairAnalysis, Routine, WashDay
from accounts.models import HairPhoto, UserProfile



class HairPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairPhoto
        fields = ['id', 'front', 'back', 'up_front']

class WashDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WashDay
        fields = ['id', 'step_name', 'step_description']

class RoutineSerializer(serializers.ModelSerializer):
    washday = WashDaySerializer(many=True, required=False)

    class Meta:
        model = Routine
        fields = ['id', 'daily_routine', 'washday', 'monthly_routine']


class HairAnalysisSerializer(serializers.ModelSerializer):
    routine = RoutineSerializer()
    hair_photos = HairPhotoSerializer()

    class Meta:
        model = HairAnalysis
        fields = ['id', 'user', 'analysis_report', 'tips', 'routine', 'hair_photos', 'timestamp']


class UserProfileHairDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'hair_porosity', 'hair_texture', 'hair_density', 'hair_growth_rate', 'hair_concerns',
            'current_hair_product', 'current_conditioner', 'current_styling_product',
            'current_product_satisfection', 'hair_goals',
            'hair_elasticity', 'hair_thickness', 'checmical_treatment', 'heat_tool_usage',
            'scalp_condition', 'climate', 'water_type', 'dietary_factors', 'lifestyle_factors',
            'styling_habits', 'styling_method_regularly_used', 'how_often_wear_protective_wears'
        ]
