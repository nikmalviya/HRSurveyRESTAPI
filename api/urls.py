from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from api.views import ObtainUserAuthToken, UserRetrieveView
from .views import QuestionViewSet, SurveyViewSet, SurveyResponseViewSet, ResponseViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register('surveys', SurveyViewSet)
router.register('survey_responses', SurveyResponseViewSet)
router.register('responses', ResponseViewSet)
urls = [
    path('login/', ObtainUserAuthToken.as_view(), name='auth'),
    path('docs/', include_docs_urls(title='Hr Survey REST API')),
    path('users/<int:pk>/', UserRetrieveView.as_view())
]
urlpatterns = router.urls + urls
