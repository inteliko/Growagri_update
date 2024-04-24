from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Reverted back to TextField
    author_name = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post_images', default='default.jpg')

    def __str__(self):
        return self.title
