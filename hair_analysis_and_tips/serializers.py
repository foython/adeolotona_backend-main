from rest_framework import serializers
from .models import *
from accounts.models import HairPhoto, UserProfile



class HairPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairPhoto
        fields = ['id', 'front', 'back', 'up_front']

# class WashDaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WashDay
#         fields = ['id', 'step_name', 'step_description']

# class RoutineSerializer(serializers.ModelSerializer):
#     washday = WashDaySerializer(many=True, required=False)

#     class Meta:
#         model = Routine
#         fields = ['id', 'daily_routine', 'washday', 'monthly_routine']


# class HairAnalysisSerializer(serializers.ModelSerializer):
#     # routine = RoutineSerializer()
#     hair_photos = HairPhotoSerializer()

#     class Meta:
#         model = HairAnalysis
#         fields = ['id', 'user', 'analysis_report', 'tips', 'routine', 'hair_photos', 'timestamp']


class HairTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairType
        fields = '__all__'

class CharacteristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristics
        fields = '__all__'

class HairConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairCondition
        fields = '__all__'

class AnalysisReportSerializer(serializers.ModelSerializer):
    hair_type = HairTypeSerializer()
    characteristics = CharacteristicsSerializer()
    conditions = HairConditionSerializer(many=True)

    class Meta:
        model = AnalysisReport
        fields = '__all__'

class HairTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairTip
        fields = '__all__'

class RoutineStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineStep
        fields = '__all__'

class HairRoutineSerializer(serializers.ModelSerializer):
    washday_steps = RoutineStepSerializer(many=True)

    class Meta:
        model = HairRoutine
        fields = '__all__'

class HairAnalysisSerializer(serializers.ModelSerializer):
    analysis_report = AnalysisReportSerializer()
    tips = HairTipSerializer(many=True)
    routine = HairRoutineSerializer()
    hair_photos = HairPhotoSerializer()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = HairAnalysis
        fields = '__all__'



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
