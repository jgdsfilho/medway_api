from core.db import BaseModel
from django.db import models
from question.utils import AlternativesChoices


class Question(BaseModel):
    content = models.TextField()

    @property
    def correct_alternative(self):
        return self.alternatives.get(is_correct=True)

    def __str__(self):
        return self.content


class Alternative(BaseModel):
    question = models.ForeignKey(Question, related_name='alternatives', on_delete=models.CASCADE)
    content = models.TextField()
    option = models.IntegerField(choices=AlternativesChoices)
    is_correct = models.BooleanField(null=True)
