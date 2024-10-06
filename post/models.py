from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can publish posts'),
            ('can_view_private', 'Can view private posts')
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title
