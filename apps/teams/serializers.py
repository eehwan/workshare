from rest_framework import serializers
from .models import Team, Membership, TeamInvitation
from django.core.mail import send_mail
from django.conf import settings


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "description", "created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # username 표시용

    class Meta:
        model = Membership
        fields = ["id", "user", "role", "joined_at"]


class TeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = ["id", "team", "email", "invited_by", "token", "accepted", "created_at"]
        read_only_fields = ["id", "invited_by", "token", "accepted", "created_at"]

    def validate_email(self, value):
        team_id = self.initial_data.get("team")
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("해당 이메일로 가입된 유저가 존재하지 않습니다.")

        if team_id:
            if Membership.objects.filter(user=user, team_id=team_id).exists():
                raise serializers.ValidationError("해당 유저는 이미 이 팀의 멤버입니다.")
            if TeamInvitation.objects.filter(email=value, team_id=team_id, accepted=False).exists():
                raise serializers.ValidationError("이미 초대 요청이 존재합니다.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["invited_by"] = request.user
        invitation = TeamInvitation.objects.create(**validated_data)

        # 초대 수락 링크
        domain = getattr(settings, "FRONTEND_DOMAIN")
        invite_link = f"{domain}/invite/accept/{invitation.token}/"

        # 이메일 전송
        send_mail(
            subject="[WorkShare] 팀 초대장이 도착했습니다!",
            message=(
                f"{request.user.email} 님이 당신을 '{invitation.team.name}' 팀에 초대했습니다.\n\n"
                f"초대 수락 링크: {invite_link}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
        )

        return invitation
