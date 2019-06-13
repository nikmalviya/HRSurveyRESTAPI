from typing import Any

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import UserSerializer
from .models import Question, QuestionChoice, Survey, SurveyQuestion, SurveyResponse, Response as _Response
from .serializers import QuestionSerializer, QuestionChoiceSerializer, SurveySerializer, SurveyQuestionSerializer, \
    SurveyResponseSerializer, ResponseSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=['GET'])
    def choices(self, _, pk=None):
        """
        Returns All the choices available for a question
        """
        choices = QuestionChoice.objects.filter(question_id=pk)
        serializer = QuestionChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        """
        This Endpoint is Used to Create Questions in bulk.
        """
        serializer = QuestionSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @action(detail=False, methods=['GET'], url_path=r'active_surveys')
    def get_active_surveys(self, _request):
        """
        Get List of All active Surveys
        """
        active_surveys = Survey.objects.filter(is_open=True)
        serializer = SurveySerializer(active_surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'POST'])
    def questions(self, request, pk=None):
        """
        get:
        Returns List of all questions available in a survey
        post:
        Used to Add Questions To a Survey
        """
        if request.method == 'GET':
            survey = Survey.objects.get(id=pk)
            questions = survey.survey_questions.order_by('order')
            serializer = SurveyQuestionSerializer(questions, many=True)
            return Response(serializer.data)
        else:
            for question in request.data:
                question['survey'] = int(pk)
            serializer = SurveyQuestionSerializer(data=request.data, many=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], url_path=r'required/(?P<question_id>\d+)')
    def required(self, _, pk, question_id):
        """
        Returns whether the question is required or not in a survey
        """
        survey_question = SurveyQuestion.objects.filter(survey_id=pk, question_id=question_id).first()
        return Response(dict(required=survey_question.required))

    @action(detail=True, methods=['GET'], url_path=r'graph_data/(?P<question_id>\d+)')
    def get_graph_data(self, _, pk, question_id):
        """
         Returns the graph data for specified question id for a survey if the question
         type is multiple choice or check boxes
        """
        question = Question.objects.get(id=question_id)
        if question.input_type not in ('multiple_choice', 'check_boxes'):
            return Response(dict(error='only multi choice questions are allowed'), status=status.HTTP_400_BAD_REQUEST)
        response = dict.fromkeys(map(lambda choice: choice.option, question.choices.all()))
        survey = Survey.objects.get(id=pk)
        for key in response.keys():
            response[key] = survey.survey_responses.filter(responses__question_id=question_id,
                                                           responses__answer=key).count()
        return Response(
            [dict(name=key, value=value) for key, value in response.items()],
            status=status.HTTP_200_OK
        )


class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

    @action(detail=False, methods=['GET'], url_path=r'survey=(?P<survey_id>\d+)')
    def survey_responses(self, _, survey_id):
        """
        Get All the SurveyResponses of a survey
        """
        survey_responses = SurveyResponse.objects.filter(survey_id=survey_id)
        serializer = SurveyResponseSerializer(survey_responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = _Response.objects.all()
    serializer_class = ResponseSerializer


class ObtainUserAuthToken(ObtainAuthToken):

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        gets username and password for login and returns user details and token
        if valid data is passed
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })


class UserRetrieveView(RetrieveAPIView):
    """
    retrieve:
    Returns User details for a specific user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
