# apps/teams/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MembershipViewSet, TeamInvitationViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"memberships", MembershipViewSet)
router.register(r"team-invitations", TeamInvitationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
