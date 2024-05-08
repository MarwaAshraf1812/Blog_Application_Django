from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    """
    - The method is used to tell Django how to find the web 
      page that shows details about a specific blog post.
    - The get_absolute_url() method will return the canonical URL of the object.
    - Using the get_absolute_url method, Django can automatically generate a URL 
      like /2023/05/01/my-first-blog/ that takes a visitor directly to this post.
    """
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
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

class Comment(models.Model):
    post = models.ForeignKey(Post,
                            on_delete=models.CASCADE,
                            # The related_name attribute allows you to name the
                            # attribute that you use for the relation 
                            # from the related object back to this one.
                            related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
