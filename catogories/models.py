from django.db import models
from django.contrib.postgres.fields import ArrayField
from authentication.models import User

class Form(models.Model):
    CATEGORY_CHOICES = [
        ('achievement', 'Achievement'),
        ('research', 'Research'),
        ('project', 'Project'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    team_members = models.TextField(max_length=255)
    # Changed from TextField to ArrayField
    tech_stack = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    projecturl = models.TextField(max_length=255)
    # Changed from TextField to ArrayField
    achivements = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_top_6 = models.BooleanField(default=False)
    is_ongoing = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    user_type = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.category.capitalize()}: {self.title}"

