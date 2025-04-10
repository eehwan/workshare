# apps/works/models.py

from django.db import models
from apps.projects.models import Project
from django.conf import settings


class Work(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="works")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="works_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return f"{self.title} ({self.project.name})"
