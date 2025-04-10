# apps/teams/views.py

from rest_framework import viewsets
from .models import Team, Membership
from .serializers import TeamSerializer, MembershipSerializer
from rest_framework.permissions import IsAuthenticated


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
