from core.db import BaseModel
from django.db import models
from exam.models import Exam, ExamQuestion
from question.models import Alternative
from student.models import Student


class ExamSubmission(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        unique_together = ('student', 'exam')

    def __str__(self):
        return f"{self.student} - {self.exam}"


class QuestionAnswer(BaseModel):
    submission = models.ForeignKey(ExamSubmission, related_name='answers', on_delete=models.CASCADE)
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    selected_alternative = models.ForeignKey(Alternative, on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=True)

    class Meta:
        unique_together = ('submission', 'exam_question')

    def __str__(self):
        return f"{self.submission} - Question {self.exam_question.number}"

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_alternative.is_correct
        super().save(*args, **kwargs) 