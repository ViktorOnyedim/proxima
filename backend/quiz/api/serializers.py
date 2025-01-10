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
# from django.contrib.auth import get_user_model
# User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2",]
        # extra_kwags = {
        #     "first_name": {"required": True},
        #     "last_name": {"required": True},
        # }

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
            # first_name=validated_data["first_name"],
            # last_name=validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "type",
            "order",
            "quiz",
            "choices",
        ]

    def create(self, validated_data):
        choices_data = validated_data.pop("choices", [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choices", [])
        choices = instance.choices.all()
        choices = list(choices)
        instance.text = validated_data.get("text", instance.text)
        instance.type = validated_data.get("type", instance.type)
        instance.order = validated_data.get("order", instance.order)
        instance.save()

        for choice_data in choices_data:
            choice = choices.pop(0)
            choice.text = choice_data.get("text", choice.text)
            choice.is_correct = choice_data.get("is_correct", choice.is_correct)
            choice.save()

        return instance

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id", "title", "description", "time_limit", "quiz_creator", "questions", "is_active"
        ]


class QuizCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizCreator
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
