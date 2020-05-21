from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass

# Alternative is to use choices if data is static, but this looks cleaner
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#choices
class Subject(models.Model):
    subject = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.subject}"

class Level(models.Model):
    group = models.CharField(max_length=16)
    level = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.group} {self.level}"

class Question(models.Model):
    title = models.CharField(max_length=128, null=True)
    content = models.CharField(max_length=2000) # ~350-400 words
    image = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userqns")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subjectqns")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="lvlqns")
    datetime_created = models.DateTimeField(auto_now_add=True)
    saved_by = models.ManyToManyField(User, blank=True, related_name="savedqns")

    def __str__(self):
        return f"{self.user}: {self.content}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="qnans")
    content = models.TextField()    # Trying out TextField instead of CharField
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userans")
    datetime_created = models.DateTimeField(auto_now_add=True)
    upvoted_by = models.ManyToManyField(User, blank=True, related_name="upvotedans")
    downvoted_by = models.ManyToManyField(User, blank=True, related_name="downvotedans")
    # upvotes = models.PositiveIntegerField(default=0)
    # downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} answered: {self.content}"