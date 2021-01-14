from django.db import models

from my_velov_assistant.users.models import User


class ApiCall(models.Model):
    """Log the call to the APIs"""

    api_name = models.CharField(max_length=20, null=False, default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.api_name} api called at {self.called_at:%H:%M %Y-%m-%d} by {self.created_by}"
