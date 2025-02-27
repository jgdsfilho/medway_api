from rest_framework import serializers

from .models import QuestionAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question_content = serializers.CharField(source='exam_question.question.content')
    question_number = serializers.IntegerField(source='exam_question.number')
    selected_option = serializers.CharField(source='selected_alternative.content')
    correct_option = serializers.CharField(source='exam_question.question.correct_alternative.content')

    class Meta:
        model = QuestionAnswer
        fields = [
            'question_number',
            'question_content',
            'selected_option',
            'correct_option',
            'is_correct'
        ]
