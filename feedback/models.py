from django.db import models

class Feedback(models.Model):
    SCHOOL_CHOICES = [
        ('SOT', 'School of Technology'),
        ('SOS', 'School of Sciences'),
    ]

    parent_name = models.CharField(max_length=255)
    keep_anonymous = models.BooleanField(default=False)

    parent_email = models.EmailField()
    school = models.CharField(max_length=3, choices=SCHOOL_CHOICES)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent_email} to {self.get_school_display()}"
