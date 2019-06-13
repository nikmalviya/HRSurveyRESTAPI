from django.contrib.auth.models import User
from django.db import models

INPUT_TYPES = (
    ('short_answer', 'Short Answer'),
    ('multiple_choice', 'Multiple Choice'),
    ('check_boxes', 'Check Boxes'),
    ('paragraph', 'Paragraph')
)


class Question(models.Model):
    question = models.CharField(max_length=200)
    input_type = models.CharField(choices=INPUT_TYPES, max_length=50)
    is_multiple_choice_answer = models.BooleanField(default=False)
    is_multianswer_question = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 related_name='choices')
    option = models.CharField(max_length=50)

    def __str__(self):
        return self.option


class Survey(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    is_open = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question, through='SurveyQuestion')

    def __str__(self):
        return self.title


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey,
                               on_delete=models.CASCADE,
                               related_name='survey_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    required = models.BooleanField(default=False)

    @property
    def question_data(self):
        return self.question

    def __str__(self):
        return f'{self.survey} Q: {self.question}'


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_responses')

    def __str__(self):
        return f'Response for Survey {self.survey}'


class Response(models.Model):
    survey_response = models.ForeignKey(SurveyResponse,
                                        on_delete=models.CASCADE,
                                        related_name='responses',
                                        blank=True)
    question = models.ForeignKey(Question,
                                 related_name='responses',
                                 on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return f'Q:{self.question} Ans:{self.answer}'
