from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    avatar = models.ImageField(upload_to='images/avatars', width_field=None, height_field=None, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, default='')

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    body = models.TextField(max_length=1000, null=False, blank=False)
    image = models.ImageField(upload_to='images/post', width_field=None, height_field=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
