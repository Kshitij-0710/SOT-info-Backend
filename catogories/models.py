from django.db import models

class Form(models.Model):
    CATEGORY_CHOICES = [
        ('achievement', 'Achievement'),
        ('research', 'Research'),
        ('project', 'Project'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.capitalize()}: {self.title}"
