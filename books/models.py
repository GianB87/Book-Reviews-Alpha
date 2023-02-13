from django.db import models
#from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.
from django.urls import reverse
from ckeditor.fields import RichTextField

from posts.models import Post
from users.models import Profile
class Book(models.Model): # always name new model as singular
    # Data to send
    class Suit(models.IntegerChoices):
        NOT_RATED = 0
        DO_NOT_READ = 1
        VERY_BAD = 2
        BAD = 3
        MEDIOCRE = 4    
        SO_SO = 5
        FINE = 6
        GOOD = 7
        VERY_GOOD = 8
        GREAT = 9
        MASTERWORK = 10
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    isbn = models.CharField(max_length=20, null=True, blank=True) 
    rate = models.IntegerField(default=0, null=False, blank=False, choices=Suit.choices)
    summary = RichTextField(null=True, blank=True)
    review = RichTextField(null=True, blank=True)
    youtube_link = models.CharField(max_length=2000, null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    
    # Data from api
    title = models.CharField(max_length=200) 
    authors = models.CharField(max_length=500, null=True, blank=True) # error because initially i am receiving a list
    image_link = models.CharField(max_length=2000, null=True, blank=True)
    def __str__(self):
        return self.title + ' | ' + str(self.authors)
    class Meta:
        ordering = ['-review_date']
    def get_absolute_url(self):
        return reverse("book", kwargs={"pk": self.pk})

class ReviewBook(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = RichTextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'post']]

    def __str__(self):
        return self.value
# class CommentBook(models.Model):
#     post = models.ForeignKey(Post, related_nane="comment", on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)    
#     def __str__(self):
#         return '%s - %s' % (self.post.title, self.name)
    