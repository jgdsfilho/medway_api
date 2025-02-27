from drf_yasg import openapi

exam_result_response = {
    200: openapi.Response(
        description="Submission details",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'exam_name': openapi.Schema(type=openapi.TYPE_STRING),
                'submission_date': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                'total_questions': openapi.Schema(type=openapi.TYPE_INTEGER),
                'correct_answers': openapi.Schema(type=openapi.TYPE_INTEGER),
                'score_percentage': openapi.Schema(type=openapi.TYPE_NUMBER),
                'answers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question_number': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'question_content': openapi.Schema(type=openapi.TYPE_STRING),
                            'selected_option': openapi.Schema(type=openapi.TYPE_STRING),
                            'correct_option': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_correct': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        }
                    )
                )
            }
        )
    ),
    404: 'Submission not found'
}

# Submit Exam
submit_exam_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['exam_id', 'student_id', 'answers'],
    properties={
        'exam_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
        'student_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
        'answers': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['question_id', 'alternative_id'],
                properties={
                    'question_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
                    'alternative_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid')
                }
            )
        )
    }
)

submit_exam_responses = {
    201: openapi.Response(
        description="Submission created successfully",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                'submission_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid')
            }
        )
    ),
    400: 'Invalid or incomplete data',
    404: 'Exam or student not found'
} 