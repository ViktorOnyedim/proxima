from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email", "first_name", "last_name"]
        extra_kwags = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return User

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


class QuizCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCreator
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class ChoiceSeializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class ParticipantSerializer(serializers.ModelSerializer):
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
