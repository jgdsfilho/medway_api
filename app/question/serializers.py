from exam.models import ExamQuestion
from question.models import Alternative
from rest_framework import serializers


class AlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternative
        fields = ['id', 'content', 'option']

class ExamQuestionSerializer(serializers.ModelSerializer):
    question_content = serializers.CharField(source='question.content')
    alternatives = AlternativeSerializer(source='question.alternatives', many=True)

    class Meta:
        model = ExamQuestion
        fields = ['id','number', 'question_content', 'alternatives']