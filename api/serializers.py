from collections import OrderedDict
from itertools import zip_longest
from pprint import pprint as print
from typing import Any

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Question, QuestionChoice, Survey, SurveyQuestion, SurveyResponse, Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
        )


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ('id', 'option')


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)

    def create(self, validated_data: Any):
        print(validated_data)
        choices = validated_data.pop('choices', None)
        question = Question.objects.create(**validated_data)
        for choice in choices:
            question.choices.create(**choice)
        return question

    def update(self, instance: Question, validated_data):
        instance.question = validated_data.get('question', instance.question)
        instance.input_type = validated_data.get('input_type', instance.input_type)
        instance.is_multiple_choice_answer = validated_data.get('is_multiple_choice_answer',
                                                                instance.is_multiple_choice_answer)
        instance.is_multianswer_question = validated_data.get('is_multianswer_question',
                                                              instance.is_multianswer_question)
        for choice, value in zip_longest(instance.choices.all(),
                                         validated_data.get('choices', None)):
            if choice is not None and value is not None:
                choice.option = value.get('option', choice.option)
                choice.save()
            elif choice is None:
                instance.choices.create(**value)
            elif value is None:
                instance.choices.remove(choice)
        instance.save()
        return instance

    class Meta:
        model = Question
        fields = '__all__'


class SurveyQuestionSerializer(serializers.ModelSerializer):
    question_data = QuestionSerializer(read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data: Any):
        if data['question'] is None:
            raise ValidationError('question required')
        data['question'] = Question.objects.get(id=data['question'])
        if isinstance(data['answer'], dict):
            return_value = []
            for k, v in data['answer'].items():
                if v:
                    return_value.append(dict(question=data['question'],
                                             answer=k))
            return return_value
        else:
            return data

    class Meta:
        model = Response
        fields = '__all__'


class SurveyResponseSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True)

    def create(self, validated_data: Any):
        responses = validated_data.pop('responses', None)
        survey_response = SurveyResponse.objects.create(**validated_data)
        for response in responses:
            if isinstance(response, list):
                for sub_response in response:
                    survey_response.responses.create(**sub_response)
            else:
                survey_response.responses.create(**response)
        return survey_response

    def to_representation(self, instance: SurveyResponse) -> Any:
        dict_repr: OrderedDict = super().to_representation(instance)
        responses = []
        responses_done = []
        for response in dict_repr.get('responses'):
            if response.get('id') in responses_done:
                continue
            if Response.objects.get(id=response['id']).question.input_type == 'check_boxes':
                resps = instance.responses.filter(question=response.get('question'))
                new_res = OrderedDict(id=[],
                                      answer=[],
                                      survey_response=response.get('survey_response'),
                                      question=response.get('question'))
                for resp in resps:
                    new_res['id'].append(resp.id)
                    new_res['answer'].append(resp.answer)
                responses.append(new_res)
                responses_done.extend(new_res['id'])
            else:
                responses.append(response)
                responses_done.append(response['id'])
        dict_repr['responses'] = responses
        return dict_repr

    class Meta:
        model = SurveyResponse
        fields = '__all__'
