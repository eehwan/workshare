# apps/feedbacks/models.py

from django.db import models
from apps.works.models import Work
from django.conf import settings


class Feedback(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="feedbacks")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="feedbacks"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)  # 피드백 반영 완료 여부

    def __str__(self):
        return f"Feedback by {self.author} on {self.work.title}"
