import datetime
import uuid
from decimal import Decimal

from django.test import TransactionTestCase
from django.urls import reverse
from exam.models import Exam
from question.models import Alternative, Question
from rest_framework import status
from rest_framework.test import APIClient
from student.models import Student


class SubmissionAPITestCase(TransactionTestCase):
    reset_sequences = True  # Reseta sequências entre testes
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.client = APIClient()

        self.student = Student.objects.create(
            username="teststudent",
            email="test@example.com",
            password="testpassword"
        )
        
        self.exam = Exam.objects.create(name="Test Exam")
        
        self.question1 = Question.objects.create(content="What is 2+2?")
        self.alt1_1 = Alternative.objects.create(question=self.question1, content="3", option=1, is_correct=False)
        self.alt1_2 = Alternative.objects.create(question=self.question1, content="4", option=2, is_correct=True)
        self.alt1_3 = Alternative.objects.create(question=self.question1, content="5", option=3, is_correct=False)
        
        self.question2 = Question.objects.create(content="What is the capital of France?")
        self.alt2_1 = Alternative.objects.create(question=self.question2, content="London", option=1, is_correct=False)
        self.alt2_2 = Alternative.objects.create(question=self.question2, content="Paris", option=2, is_correct=True)
        self.alt2_3 = Alternative.objects.create(question=self.question2, content="Berlin", option=3, is_correct=False)
        
        self.exam_question1 = self.exam.exam_questions.create(question=self.question1, number=1)
        self.exam_question2 = self.exam.exam_questions.create(question=self.question2, number=2)
        
        
    def test_submit_exam_success(self):
        """Test successful exam submission"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.exam_question2.id),
                    'alternative_id': str(self.alt2_2.id)  # Correct answer
                }
            ]
        }
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
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
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.exam_question2.id),
                    'alternative_id': str(self.alt2_1.id)  # Wrong answer
                }
            ]
        }
        
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 50.0)  # 1 out of 2 correct
        
    def test_submit_exam_invalid_exam(self):
        """Test exam submission with invalid exam ID"""
        data = {
            'exam_id': str(uuid.uuid4()),  # Non-existent exam
            'student_id': str(self.student.id),
            'answers': []
        }
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_submit_exam_invalid_student(self):
        """Test exam submission with invalid student ID"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': 44,  # Non-existent student
            'answers': [
                {
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.exam_question2.id),
                    'alternative_id': str(self.alt2_1.id)  # Wrong answer
                }
            ]
        }
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
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
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_exam_result_success(self):
        """Test successful retrieval of exam results"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)  # Correct answer
                },
                {
                    'question_id': str(self.exam_question2.id),
                    'alternative_id': str(self.alt2_1.id)  # Wrong answer
                }
            ]
        }
        
        url = reverse('submission:submit_exam')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 50.0) 

        url = reverse('submission:exam_result', kwargs={'submission_id': response.data['submission_id']})
        response = self.client.get(url)
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


class SubmissionAPIResponseSchemaTestCase(TransactionTestCase):
    reset_sequences = True
    
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
        
        # Add questions to exam
        self.exam_question1 = self.exam.exam_questions.create(question=self.question1, number=1)
        
        
        # URLs
        self.submit_url = reverse('submission:submit_exam')
    
    def test_get_exam_result_response_schema(self):
        """Test that get exam result endpoint response structure is correct"""
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(self.student.id),
            'answers': [
                {
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)
                }
            ]
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        
        url = reverse('submission:exam_result', kwargs={'submission_id': response.data['submission_id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response structure
        self.assertIn('exam_name', response.data)
        self.assertIn('submission_date', response.data)
        self.assertIn('total_questions', response.data)
        self.assertIn('correct_answers', response.data)
        self.assertIn('score_percentage', response.data)
        self.assertIn('answers', response.data)
        
        # Verify data types
        self.assertTrue(isinstance(response.data['exam_name'], str))
        self.assertTrue(isinstance(response.data['submission_date'], datetime.datetime))
        self.assertTrue(isinstance(response.data['total_questions'], int))
        self.assertTrue(isinstance(response.data['correct_answers'], int))
        self.assertTrue(isinstance(response.data['score_percentage'], float))
        self.assertTrue(isinstance(response.data['answers'], list))
        
        # Verify answers structure
        if response.data['answers']:
            answer = response.data['answers'][0]
            self.assertIn('question_number', answer)
            self.assertIn('question_content', answer)
            self.assertIn('selected_option', answer)
            self.assertIn('correct_option', answer)
            self.assertIn('is_correct', answer)
            
            # Verify data types
            self.assertTrue(isinstance(answer['question_number'], int))
            self.assertTrue(isinstance(answer['question_content'], str))
            self.assertTrue(isinstance(answer['selected_option'], str))
            self.assertTrue(isinstance(answer['correct_option'], str))
            self.assertTrue(isinstance(answer['is_correct'], bool))
    
    def test_submit_exam_response_schema(self):
        """Test that submit exam endpoint response structure is correct"""
        new_student = Student.objects.create(
            username="newstudent",
            email="new@example.com",
            password="newpassword"
        )
        data = {
            'exam_id': str(self.exam.id),
            'student_id': str(new_student.id),
            'answers': [
                {
                    'question_id': str(self.exam_question1.id),
                    'alternative_id': str(self.alt1_2.id)
                }
            ]
        }
        
        response = self.client.post(self.submit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify response structure
        self.assertIn('message', response.data)
        self.assertIn('score', response.data)
        self.assertIn('submission_id', response.data)
        
        # Verify data types
        self.assertTrue(isinstance(response.data['message'], str))
        self.assertTrue(isinstance(response.data['score'], Decimal))
        self.assertTrue(isinstance(response.data['submission_id'], uuid.UUID))
