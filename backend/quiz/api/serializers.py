from rest_framework import serializers
from quiz.models import (
    Organization,
    Quiz,
    QuizCreator,
    Question,
    Choice,
    Participant,
    ParticipantAnswer,
    QuizResult,
)

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "title", "description", "time_limit", "quiz_creator", "created_at", "start_time", "is_active"
        ]


class QuizCreatorSeializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCreator
        fields = ["user, organization"]


class QuestionSeializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class ChoiceSeializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class ParticipantSeializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class ParticipantAnswer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantAnswer
        fields = "__all__"


class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = "__all__"
