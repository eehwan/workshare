# apps/teams/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Team, Membership, TeamInvitation
from .serializers import TeamSerializer, MembershipSerializer, TeamInvitationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()



class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        본인이 소속된 팀만 조회 가능
        """
        return Team.objects.filter(memberships__user=self.request.user)

    def perform_create(self, serializer):
        """
        팀 생성 시 자동으로 본인을 OWNER로 Membership 추가
        """
        team = serializer.save()
        Membership.objects.create(
            user=self.request.user,
            team=team,
            role=Membership.Role.OWNER
        )

    def perform_destroy(self, instance):
        """
        팀 삭제는 OWNER만 가능
        """
        if not Membership.objects.filter(team=instance, user=self.request.user, role=Membership.Role.OWNER).exists():
            raise PermissionDenied("해당 팀의 OWNER만 삭제할 수 있습니다.")
        instance.delete()


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        본인이 소속된 팀의 멤버만 조회 가능
        """
        return Membership.objects.filter(team__memberships__user=self.request.user)

    def perform_create(self, serializer):
        """
        멤버 추가는 해당 팀의 OWNER만 가능
        """
        team = serializer.validated_data["team"]
        if not Membership.objects.filter(team=team, user=self.request.user, role=Membership.Role.OWNER).exists():
            raise PermissionDenied("팀의 OWNER만 멤버를 추가할 수 있습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        OWNER는 멤버 삭제 가능, 일반 멤버는 자기 자신만 탈퇴 가능
        """
        user = self.request.user
        if instance.user != user:
            if not Membership.objects.filter(team=instance.team, user=user, role=Membership.Role.OWNER).exists():
                raise PermissionDenied("해당 멤버를 삭제할 권한이 없습니다.")
        instance.delete()


class TeamInvitationViewSet(viewsets.ModelViewSet):
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'token'

    def get_queryset(self):
        return TeamInvitation.objects.filter(invited_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny], url_path='accept')
    def accept_invitation(self, request, token=None):
        try:
            invitation = self.get_object()
            if invitation.accepted:
                return Response({"detail": "이미 수락된 초대입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except TeamInvitation.DoesNotExist:
            return Response({"detail": "초대를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(email=invitation.email)
        except User.DoesNotExist:
            return Response({"detail": "해당 이메일 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if Membership.objects.filter(user=user, team=invitation.team).exists():
            return Response({"detail": "이미 팀에 속해 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        Membership.objects.create(user=user, team=invitation.team, role="member")
        invitation.accepted = True
        invitation.save()

        return Response({"detail": "초대 수락 완료"}, status=status.HTTP_200_OK)