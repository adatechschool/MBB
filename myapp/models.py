# myapp\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Role(models.Model):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'Regular User'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Extension du modèle utilisateur Django avec des champs personnalisés.
    """
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, related_name='users')

    class Meta:
        db_table = '"User"'

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='follower_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table = '"Follow"'

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(
        User, through='Like', related_name='liked_posts')
    hashtags = models.ManyToManyField(
        'Hashtag', through='PostHashtag', related_name='posts')

    class Meta:
        db_table = '"Post"'

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"Comment"'

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        db_table = '"Like"'

    def __str__(self):
        return f"Like by {self.user.username} on post {self.post.id}"


class Media(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    MEDIA_TYPES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
    ]
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='media')
    media_url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"Media"'

    def __str__(self):
        return f"{self.media_type} for post {self.post.id}"


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '"Hashtag"'

    def __str__(self):
        return self.name


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'hashtag')
        db_table = '"PostHashtag"'

    def __str__(self):
        return f"Post {self.post.id} - Hashtag {self.hashtag.name}"


class Session(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sessions')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = '"Session"'

    def __str__(self):
        return f"Session for {self.user.username}"

    def is_expired(self):
        return timezone.now() > self.expires_at
