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
    # CustomUser,
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



# class QuizTakingViewSet(viewsets.ModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer
#     permission_classes = [permissions.AllowAny] # change to isAuthenticated

#     @action(detail=True, methods=['get'])
#     def start(self, request, pk=None):
#         quiz = self.get_object()

        

#         if not quiz.is_active:
#             return Response(
#                 {"error": "This quiz is not currently active"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         participant, created = Participant.objects.get_or_create(
#             user=request.user,
#             quiz=quiz,
#             defaults={"is_completed": False}
#         )
#         return Response({"quiz": QuizSerializer(quiz).data})



class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        question_id = request.data.get("question_id")
        choice_id = request.data.get("choice_id")

        try:
            question = Question.objects.get(id=question_id, quiz_id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Invalid Question Id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            choice = Choice.objects.get(id=choice_id)
        except Choice.DoesNotExist:
            return Response({"error": "Invalid Choice Id"}, status=status.HTTP_400_BAD_REQUEST)

        if choice.is_correct():
            # is_correct = True
            return Response({"message": "Correct Answer"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Incorrect Answer"}, status=status.HTTP_200_OK)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.AllowAny]

# class OrganizationRegistrationView(generics.CreateAPIView):
#     serializer_class = OrganizationSerializer
#     permission_classes=[permissions.AllowAny]

class QuizListCreateView(generics.ListCreateAPIView):
    # queryset = Quiz.objects.all()

    serializer_class = QuizSerializer
    # permission_classes = [IsQuizCreator]
    def get_queryset(self):
        quizzes_queryset = Quiz.objects.all()
        return quizzes_queryset
        # if self.request.user.user_type == 'CREATOR':
        #     return Quiz.objects.filter(quiz_creator__organization=self.request.user.organization)
        # return Quiz.objects.none()
    
    # def perform_create(self, serializer):
    #     quiz_creator = QuizCreator.objects.get(user=self.request.user)
    #     serializer.save(quiz_creator=quiz_creator)

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizSubmissionView(generics.CreateAPIView):
    serializer_class = QuizResultSerializer

    def create(self, request, *args, **kwargs):
        # Get quiz_id from URL param <int:quiz_id>
        quiz_id = kwargs.get("quiz_id") 
        try:
            # Get or create participant
            participant, created = Participant.objects.get_or_create(
                user=request.user,
                quiz_id=quiz_id,
                defaults={"is_completed": False}
            )

            # Process answers
            answers_data = request.data.get("answers", {})
            for question_id, answers_data in answers_data.items():
                question = Question.objects.get(id=question_id)

                #Create participant answer based on question type
                if question.type in ["SC", "MC", "B"]:
                    answer_obj = ParticipantAnswer.objects.create(
                        participant=participant,
                        question=question,
                    )

                    # Handle selected choices
                    if isinstance(answers_data, list):
                        answer_obj.selected_choices.set(answers_data)
                    else:
                        answer_obj.selected_choices.set([answers_data])
                else:
                    # Text Question
                    ParticipantAnswer.objects.create(
                        participant=participant,
                        question=question,
                        text_response = answers_data
                    )

            # Calculate score
            total_questions = participant.quiz.questions.count()
            correct_answers = sum(1 for answer in participant.participantanswer_set.all()
                                  if answer.is_correct())
            score = round((correct_answers / total_questions) * 100)

            # Create Quiz Result
            quiz_result = QuizResult.objects.create(
                quiz_id=quiz_id,
                participant=participant,
                score=score
            )

            # Mark participant as completed
            participant.is_completed = True
            participant.save()

            serializer = self.get_serializer(quiz_result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class QuizCreatorListCreateView(generics.ListCreateAPIView):
    queryset = QuizCreator.objects.all()
    serializer_class = QuizCreatorSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
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







# class StartQuizView(generics.RetrieveAPIView):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer
#     # permission_classes = [permissions.IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         quiz = self.get_object()

#         if not quiz.is_active:
#             return Response(
#                 {"error": "This quiz is not currently active"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         if Participant.objects.filter(user=request.user, quiz=quiz).exists():
#             participant = Participant.objects.get(user=request.user, quiz=quiz)
#             if participant.is_completed:
#                 return Response(
#                     {"error": "You have already completed this quiz"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
        
#         participant, created = Participant.objects.get_or_create(
#             user=request.user,
#             quiz=quiz,
#             defaults={"is_completed": False}
#             )

#         # Set quiz time if first participant
#         if not quiz.start_time:
#             quiz.start_time = timezone.now()
#             quiz.save()

#         # Calculate time remaining
#         time_elapsed = timezone.now() - quiz.start_time
#         time_remaining = (quiz.time_limit - time_elapsed).total_seconds()

#         serializer = self.get_serializer(quiz)

#         context = {
#             "quiz": serializer.data,
#             "time_remaining": time_remaining,
#             "participant": ParticipantSerializer(participant).data
#         }

#         # return Response(serializer.data)
#         return render(request, "quiz/quiz.html", context)

    

