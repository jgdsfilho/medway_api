from decimal import Decimal

from core.logging import logging
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from docs.schemas.submission import (
    exam_result_response,
    submit_exam_request,
    submit_exam_responses,
)
from drf_yasg.utils import swagger_auto_schema
from exam.models import Exam, ExamQuestion
from question.models import Alternative
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from student.models import Student

from .models import ExamSubmission, QuestionAnswer
from .serializers import QuestionAnswerSerializer

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='get',
    operation_description="Get detailed results for a specific exam submission",
    responses=exam_result_response
)
@api_view(['GET'])
def get_exam_result(request, submission_id):
    """
    Get detailed results for a specific exam submission, including:
    - Exam name
    - Submission date
    - Total questions
    - Total correct answers
    - Score percentage
    - Detailed list of answers
    """
    try:
        submission = ExamSubmission.objects.select_related(
            'exam'
        ).prefetch_related(
            Prefetch(
                'answers',
                queryset=QuestionAnswer.objects.select_related(
                    'exam_question__question',
                    'selected_alternative',
                ).prefetch_related(
                    Prefetch(
                        'exam_question__question__alternatives',
                        queryset=Alternative.objects.all(),
                        to_attr='all_alternatives'
                    )
                )
            )
        ).annotate(
            correct_answers_count=Count(
                'answers',
                filter=Q(answers__is_correct=True)
            ),
            count_questions=Count('answers')
        ).get(
            id=submission_id,
        )
    except ExamSubmission.DoesNotExist:
        return Response(
            {'error': 'Submission not found or unauthorized'},
            status=status.HTTP_404_NOT_FOUND
        )

    answers = QuestionAnswerSerializer(submission.answers.all(), many=True).data

    response_data = {
        'exam_name': submission.exam.name,
        'submission_date': submission.created_at,
        'total_questions': submission.count_questions,
        'correct_answers': submission.correct_answers_count,
        'score_percentage': float(submission.score),
        'answers': answers
    }

    return Response(response_data)

@swagger_auto_schema(
    method='post',
    operation_description="Submit exam answers",
    request_body=submit_exam_request,
    responses=submit_exam_responses
)
@api_view(['POST'])
def submit_exam(request):
    """
    Submit exam answers.
    
    Required:
    - exam_id: Exam UUID
    - student_id: Student UUID
    - answers: List of answers containing:
        - question_id: Question UUID
        - alternative_id: Selected alternative UUID
    
    Returns:
    - Success message
    - Score obtained
    - Submission ID
    """
    exam_id = request.data.get('exam_id')
    answers = request.data.get('answers', [])
    student_id = request.data.get('student_id')

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response(
            {'error': 'Exam not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    exam_questions_count = exam.exam_questions.count()
    if len(answers) != exam_questions_count:
        logger.error(f"All questions must be answered: {len(answers)} != {exam_questions_count}")
        return Response(
            {'error': 'All questions must be answered'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            logger.error(f"Student not found: {student_id}")
            return Response(
                {'error': 'Student not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        submission = ExamSubmission.objects.create(
            student=student,
            exam=exam
        )

        correct_answers = 0

        for answer_data in answers:
            question_id = answer_data.get('question_id')
            alternative_id = answer_data.get('alternative_id')

            try:
                exam_question = ExamQuestion.objects.get(
                    exam=exam, 
                    id=question_id
                )
                alternative = Alternative.objects.get(
                    id=alternative_id,
                    question=exam_question.question
                )
            except (ExamQuestion.DoesNotExist, Alternative.DoesNotExist) as e:
                logger.error(f"Invalid question number or alternative ID: {e}")
                transaction.set_rollback(True)
                return Response(
                    {'error': f'Invalid question number or alternative ID {e}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            answer = QuestionAnswer.objects.create(
                submission=submission,
                exam_question=exam_question,
                selected_alternative=alternative
            )

            if answer.is_correct:
                correct_answers += 1

        submission.score = Decimal(correct_answers) / Decimal(exam_questions_count) * 100
        submission.save()

        return Response({
            'message': 'Exam submitted successfully',
            'score': submission.score,
            'submission_id': submission.id
        }, status=status.HTTP_201_CREATED) 