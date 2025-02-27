from drf_yasg import openapi

list_exams_parameters = [
    openapi.Parameter(
        'name',
        openapi.IN_QUERY,
        description="Filter by exact exam name",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'name__icontains',
        openapi.IN_QUERY,
        description="Filter by partial exam name (case insensitive)",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'page',
        openapi.IN_QUERY,
        description="Page number",
        type=openapi.TYPE_INTEGER,
        required=False
    ),
    openapi.Parameter(
        'page_size',
        openapi.IN_QUERY,
        description="Page size",
        type=openapi.TYPE_INTEGER,
        required=False
    ),
]

list_exams_responses = {
    200: openapi.Response(
        description="List of exams",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                'next': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                'previous': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'total_questions': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                )
            }
        )
    )
}

exam_detail_responses = {
    200: openapi.Response(
        description="Exam details",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'questions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                            'number': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'question_content': openapi.Schema(type=openapi.TYPE_STRING),
                            'alternatives': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                                        'option': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                )
                            )
                        }
                    )
                )
            }
        )
    ),
    404: 'Exam not found'
} 