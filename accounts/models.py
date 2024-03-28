from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    working_hours_per_day = models.PositiveSmallIntegerField(default=8) 

    def __str__(self):
        return self.user.username