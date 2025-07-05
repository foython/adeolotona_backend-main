from rest_framework import serializers
from .models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    referred_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Referral
        fields = ['id', 'referred_by', 'referral_code']
        read_only_fields = ['referral_code']

    def create(self, validated_data):
        # The referral_code will be auto-generated in the model's save method
        return super().create(validated_data)
