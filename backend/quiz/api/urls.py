from django.urls import path, include
from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
router.register(r"questions", api_views.QuestionViewSet)
router.register(r"quiz-taking", api_views.QuizTakingViewSet)

app_name = 'quiz'
urlpatterns = [
    path("register/", api_views.RegisterView.as_view(), name="auth_register"),

    # quizzes
    path("quizzes/", api_views.QuizListView.as_view(), name="quiz_list"),
    path("quizzes/<int:pk>/", api_views.QuizDetailView.as_view(), name="quiz_detail"),

    # Questions
    # path("questions/", api_views.QuestionListView.as_view(), name="question_list"),
    # path("questions/<int:pk>/", api_views.QuestionDetailView.as_view(), name="question_detail"),
    path("", include(router.urls)),


    # Participants
    path("participants/", api_views.ParticipantListView.as_view(), name="participant_list"),
    path("participants/<int:pk>/", api_views.ParticipantDetailView.as_view(), name="participant_detail"),

    # Participants Quiz Results
    path("participants/<int:participant_pk>/quiz-results/", api_views.QuizResultListView.as_view(), name="quiz_result_list"),
    path("participants/<int:participant_pk>/quiz-results/<int:pk>/", api_views.QuizResultDetailView.as_view(), name="quiz_result_detail"),
]