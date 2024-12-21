from rest_framework import generics, permissions, viewsets
from quiz.api.serializers import *
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


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [permissions.IsAuthenticated]

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizCreatorViewSet(viewsets.ModelViewSet):
    queryset = QuizCreator.objects.all()
    serializer_class = QuizCreatorSerializer


# class QuestionListView(generics.ListCreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer


# class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ParticipantListView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class ParticipantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class QuizResultListView(generics.ListAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer


class QuizResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer