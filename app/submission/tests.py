import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import ExamSubmission
from exam.models import Exam
from question.models import Question, Alternative
from student.models import Student


class SubmissionAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test data
        self.student = Student.objects.create(
            username="teststudent",
            email="test@example.com",
            password="testpassword"
        )
        
        self.exam = Exam.objects.create(name="Test Exam")
        
        # Create questions with alternatives
        self.question1 = Question.objects.create(content="What is 2+2?")
        self.alt1_1 = Alternative.objects.create(question=self.question1, content="3", option=1, is_correct=False)
        self.alt1_2 = Alternative.objects.create(question=self.question1, content="4", option=2, is_correct=True)
        self.alt1_3 = Alternative.objects.create(question=self.question1, content="5", option=3, is_correct=False)
        
        self.question2 = Question.objects.create(content="What is the capital of France?")
        self.alt2_1 = Alternative.objects.create(question=self.question2, content="London", option=1, is_correct=False)
        self.alt2_2 = Alternative.objects.create(question=self.question2, content="Paris", option=2, is_correct=True)
        self.alt2_3 = Alternative.objects.create(question=self.question2, content="Berlin", option=3, is_correct=False)
        
        # Add questions to exam
        self.exam_question1 = self.exam.exam_questions.create(question=self.question1, number=1)
        self.exam_question2 = self.exam.exam_questions.create(question=self.question2, number=2)
        
        # Create a submission for testing get_exam_result
        self.submission = ExamSubmission.objects.create(
            student=self.student,
            exam=self.exam
        )
        
        # Add answers to the submission
        self.submission.answers.create(
            exam_question=self.exam_question1,
            selected_alternative=self.alt1_2,  # Correct answer
            is_correct=True
        )
        self.submission.answers.create(
            exam_question=self.exam_question2,
            selected_alternative=self.alt2_1,  # Wrong answer
            is_correct=False
        )
        
        # URLs
        self.submit_url = reverse('submission:submit_exam')
        self.result_url = reverse('submission:exam_result', kwargs={'submission_id': self.submission.id})
        
    def test_submit_exam_success(self):
        """Test successful exam submission"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.question2.id),
                    'alternative_id': str(self.alt2_2.id)  # Correct answer
                }
            ]
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('submission_id', response.data)
        self.assertEqual(response.data['score'], 100.0)  # All answers correct
        
    def test_submit_exam_partial_correct(self):
        """Test exam submission with some correct answers"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.question2.id),
                    'alternative_id': str(self.alt2_1.id)  # Wrong answer
                }
            ]
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 50.0)  # 1 out of 2 correct
        
    def test_submit_exam_invalid_exam(self):
        """Test exam submission with invalid exam ID"""
        data = {
            'exam_id': str(uuid.uuid4()),  # Non-existent exam
            'student_id': str(self.student.id),
            'answers': []
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_submit_exam_invalid_student(self):
        """Test exam submission with invalid student ID"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(uuid.uuid4()),  # Non-existent student
            'answers': []
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_submit_exam_missing_answers(self):
        """Test exam submission with missing answers"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.question1.id),
                    'alternative_id': str(self.alt1_2.id)
                }
                # Missing answer for question2
            ]
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_exam_result_success(self):
        """Test successful retrieval of exam results"""
        response = self.client.get(self.result_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['exam_name'], "Test Exam")
        self.assertEqual(response.data['total_questions'], 2)
        self.assertEqual(response.data['correct_answers'], 1)
        self.assertEqual(response.data['score_percentage'], 50.0)
        self.assertEqual(len(response.data['answers']), 2)
        
    def test_get_exam_result_not_found(self):
        """Test exam result retrieval with non-existent ID"""
        non_existent_id = uuid.uuid4()
        url = reverse('submission:exam_result', kwargs={'submission_id': non_existent_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 