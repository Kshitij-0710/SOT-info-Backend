from django.db import models

class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Research(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
