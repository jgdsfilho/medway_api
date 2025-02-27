from django.core.paginator import Paginator
from docs.schemas.exam import (
    exam_detail_responses,
    list_exams_parameters,
    list_exams_responses,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Exam
from .serializers import ExamDetailSerializer, ExamListSerializer


@swagger_auto_schema(
    method='get',
    operation_description="List all exams with pagination and filtering",
    manual_parameters=list_exams_parameters,
    responses=list_exams_responses
)
@api_view(['GET'])
def list_exams(request):
    """
    List all exams with pagination and filtering.
    
    Query parameters:
    - name: Filter by exact exam name
    - name__icontains: Filter by partial exam name
    - page: Page number
    """
    queryset = Exam.objects.all()
    
    # Filtering
    name = request.query_params.get('name')
    name_contains = request.query_params.get('name__icontains')
    if name:
        queryset = queryset.filter(name=name)
    if name_contains:
        queryset = queryset.filter(name__icontains=name_contains)
    
    # Pagination
    page_size = request.query_params.get('page_size', 10)
    page_number = request.query_params.get('page', 1)
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page_number)
    
    serializer = ExamListSerializer(page_obj, many=True)
    
    return Response({
        'count': paginator.count,
        'next': page_obj.has_next() and page_number + 1 or None,
        'previous': page_obj.has_previous() and page_number - 1 or None,
        'results': serializer.data
    })

@swagger_auto_schema(
    method='get',
    operation_description="Get detailed information about a specific exam",
    responses=exam_detail_responses
)
@api_view(['GET'])
def get_exam_detail(request, exam_id):
    """
    Get detailed information about a specific exam, including all questions and alternatives.
    """
    try:
        exam = Exam.objects.prefetch_related(
            'exam_questions__question__alternatives'
        ).get(id=exam_id)
    except Exam.DoesNotExist:
        return Response(
            {'error': 'Exam not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ExamDetailSerializer(exam)
    return Response(serializer.data)
