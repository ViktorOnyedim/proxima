from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

QUESTION_TYPE = (
    ("single choice", "single choice")
    ("multiple choice", "multiple choice"),
    ("text", "text"),
    ("boolean", "boolean")
)

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class QuizCreator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    time_limit = models.DurationField(default=timedelta(minues=30))
    quiz_creator = models.ForeignKey(QuizCreator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(max_length=300)
    type = models.CharField(choices=QUESTION_TYPE, default="single choice")
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Question {self.id}: {self.text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200)
    isCorrect = models.BooleanField(default=False)

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    