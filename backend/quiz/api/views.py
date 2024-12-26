from rest_framework import generics, permissions, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
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


def api_root(request):
    return render(request, "quiz/base.html")


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [permissions.IsAuthenticated]

class OrganizationRegistrationView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes=[]

class QuizTakingViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.AllowAny] # change to isAuthenticated

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        quiz = self.get_object()

        

        if not quiz.is_active:
            return Response(
                {"error": "This quiz is not currently active"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participant, created = Participant.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            defaults={"is_completed": False}
        )
        return Response({"quiz": QuizSerializer(quiz).data})

class StartQuizView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        serializer = self.get_serializer(quiz)
        # return Response(serializer.data)
        return render(request, "quiz/quiz.html", {"quiz": serializer.data})

    

class QuizListView(generics.ListAPIView):
    # queryset = Quiz.objects.all()

    serializer_class = QuizSerializer
    def get_queryset(self):
        quizzes_queryset = Quiz.objects.all()
        return quizzes_queryset

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