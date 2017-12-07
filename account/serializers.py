from rest_framework import serializers
from account.models import User


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email_id', 'profile_picture_url', 'first_name', 'last_name')
