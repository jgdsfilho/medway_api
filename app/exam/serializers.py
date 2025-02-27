from question.serializers import ExamQuestionSerializer
from rest_framework import serializers

from .models import Exam


class ExamListSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'name', 'total_questions']

    def get_total_questions(self, obj):
        return obj.exam_questions.count()

class ExamDetailSerializer(serializers.ModelSerializer):
    questions = ExamQuestionSerializer(source='exam_questions', many=True)

    class Meta:
        model = Exam
        fields = ['id', 'name', 'questions']