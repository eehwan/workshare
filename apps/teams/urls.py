# apps/teams/urls.py

from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, MembershipViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"memberships", MembershipViewSet)

urlpatterns = router.urls
