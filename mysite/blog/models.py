from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # the date will be saved automatically when creating an object.
    created = models.DateTimeField(auto_now_add=True)
    # the date will be updated automatically when saving an object.
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        """ t it should sort results by the publish field 
        in descending order by default when you query the database.
        """
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish'],)
        ]
        
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    def __str__(self):
        return self.title
    