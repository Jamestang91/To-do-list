from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# user name: jquery293 email: jquery123@email.com pass:jq0987654321
from django.utils import timezone


class Task(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True, default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True, default=timezone.now)
    complete = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if not self.start_time:
            self.start_time = timezone.now()
        if not self.end_time:
            self.end_time = timezone.now()
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError("Start time must be earlier than end time.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
