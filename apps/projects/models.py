# apps/projects/models.py

from django.db import models
from apps.teams.models import Team
from django.conf import settings


class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ("team", "name")  # 같은 팀 내에서 중복 이름 금지

    def __str__(self):
        return f"{self.name} ({self.team.name})"
