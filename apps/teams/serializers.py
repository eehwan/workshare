from rest_framework import serializers
from .models import Team, Membership
from django.contrib.auth import get_user_model

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "description", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # username 표시용

    class Meta:
        model = Membership
        fields = ["id", "user", "role", "joined_at"]
