from django.db import models
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import timedelta
from django.conf import settings

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
        return f"{self.user.username} at {self.organization.name}"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    time_limit = models.DurationField(default=timedelta(minutes=30))
    quiz_creator = models.ForeignKey(QuizCreator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

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
    text_response = models.CharField(max_length=200) # For text questions
    # choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.CASCADE) # for SC/MC/B(boolean)
    selected_choices = models.ManyToManyField(Choice, blank=True, related_name='answers') # for SC/MC/B(boolean)

    # is_correct = models.BooleanField(default=False) # track if answer is the correct one
    def is_correct(self):
        if self.question.type == "T":
            correct_answers = Choice.objects.filter(question=self.question, is_correct=True)
            if correct_answers:
                return self.text_response.lower() == correct_answers.first().text.lower()
            return False
        elif self.question.type == "SC" or self.question.type == "MC" or self.question.type == "B":
            correct_choices = set(Choice.objects.filter(question=self.question, is_correct=True))
            answered_choices = set(self.selected_choices.all())
            if self.question.type == "SC" or self.question.type == "B":
                return len(answered_choices) == 1 and correct_choices == answered_choices
            else:
                return correct_choices == answered_choices
        return False

    def __str__(self):
        if self.text_response:
            return f"Answer for {self.question.text}: {self.text_response}"
        return f"Answer for {self.question.text}: {', '.join([choice.text for choice in self.selected_choices.all()])}"
    

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}"

class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant.user.username} scored {self.score} in {self.quiz.title}"