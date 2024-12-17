from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

QUESTION_TYPE = (
    ("SC", "single choice"),
    ("MC", "multiple choice"),
    ("T", "text"),
    ("B", "Boolean"),
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
    time_limit = models.DurationField(default=timedelta(minutes=30))
    quiz_creator = models.ForeignKey(QuizCreator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    type = models.CharField(max_length=2, choices=QUESTION_TYPE, default="SC")
    order = models.PositiveIntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"Question {self.id}: {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=200) # text of the choice
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class ParticipantAnswer(models.Model):
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.CASCADE) # for SC/MC/B(boolean)
    text_response = models.CharField(max_length=200) # For text questions
    is_correct = models.BooleanField(default=False) # track if answer is the correct one

    def save(self, *args, **kwargs):
        if self.choice:
            self.is_correct = self.choice.is_correct
        elif self.text_response:
            self.is_correct = self.text_response.strip().lower() == self.question.text.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.choice:
            return f"Answer to {self.question.text}: {self.choice.text}"
        return f"Answer to {self.question.text}: {self.text_response}"


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"
