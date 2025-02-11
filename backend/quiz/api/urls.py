from django.urls import path, include
from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
# router.register(r"quiz-taking", api_views.QuizTakingViewSet)

app_name = 'quiz'
urlpatterns = [
    path("", include(router.urls)),

    path("home", api_views.api_root, name="api_root"),

    path("user/", api_views.UserDetailView.as_view(), name="user_detail"),
    path("register/", api_views.RegisterView.as_view(), name="register"),

    # quizzes
    path("quiz/", api_views.QuizListCreateView.as_view(), name="quiz_list"),
    path("quiz/<int:pk>/", api_views.QuizDetailView.as_view(), name="quiz_detail"),
    # path("quiz/<int:pk>/start/", api_views.StartQuizView.as_view(), name="start_quiz"),
    path("quiz/<int:quiz_id>/submit/", api_views.QuizSubmissionView.as_view(), name="submit_quiz"),
    path("quiz/<int:pk>/results/<int:result_id>/", api_views.QuizResultDetailView.as_view(), name="quiz_result_detail"),

    # Questions
    path("questions/", api_views.QuestionListCreateView.as_view(), name="question_list"),
    path("questions/<int:pk>/", api_views.QuestionDetailView.as_view(), name="question_detail"),


    # Participants
    path("participants/", api_views.ParticipantListView.as_view(), name="participant_list"),
    path("participants/<int:pk>/", api_views.ParticipantDetailView.as_view(), name="participant_detail"),

    # Participants Quiz Results
    path("participants/<int:participant_pk>/quiz-results/", api_views.QuizResultListView.as_view(), name="quiz_result_list"),
    path("participants/<int:participant_pk>/quiz-results/<int:pk>/", api_views.QuizResultDetailView.as_view(), name="quiz_result_detail"),
]