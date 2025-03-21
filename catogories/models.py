from django.db import models
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
    tech_stack = models.TextField(max_length=255)
    projecturl = models.TextField(max_length=255)
    achivements = models.TextField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_top_6 = models.BooleanField(default=False)
    is_ongoing = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    user_type = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES, editable=False)

    def __str__(self):
        return f"{self.category.capitalize()}: {self.title}"
    
    def get_tech_stack_list(self):
        """Returns tech stack as a list of items"""
        if not self.tech_stack:
            return []
        return [tech.strip() for tech in self.tech_stack.split(',')]
    
    def get_achievements_list(self):
        """Returns achievements as a list of items"""
        if not self.achivements:
            return []
        return [achievement.strip() for achievement in self.achivements.split(',')]