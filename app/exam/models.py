from core.db import BaseModel
from django.db import models
from question.models import Question


class Exam(BaseModel):
    name = models.CharField(max_length=100)
    questions = models.ManyToManyField(Question, through='ExamQuestion', related_name='questions')

    def __str__(self):
        return self.name


class ExamQuestion(BaseModel):
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE,
        related_name='exam_questions'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('exam', 'number')
        ordering = ['number']

    def __str__(self):
        return f'{self.question} - {self.exam}'
