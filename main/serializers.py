from rest_framework import serializers
from .models import Profile

class AsyncProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'device_id', 'permission']