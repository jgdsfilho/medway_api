import uuid

from django.test import TransactionTestCase
from django.urls import reverse
from exam.models import Exam
from question.models import Alternative, Question
from rest_framework import status
from rest_framework.test import APIClient


class ExamAPITestCase(TransactionTestCase):
    reset_sequences = True  # Reseta sequências entre testes
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.client = APIClient()
        # Create test data
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
        self.exam.exam_questions.create(question=self.question1, number=1)
        self.exam.exam_questions.create(question=self.question2, number=2)
        
        # URLs
        self.list_url = reverse('exam:exam-list')
        self.detail_url = reverse('exam:exam-detail', kwargs={'exam_id': self.exam.id})
    
    def test_list_exams_success(self):
        """Test successful retrieval of exam list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Test Exam")
        self.assertEqual(response.data['results'][0]['total_questions'], 2)
    
    def test_list_exams_with_filter_success(self):
        """Test successful filtering of exam list"""
        # Create another exam for testing filters
        Exam.objects.create(name="Another Exam")
        
        # Test exact name filter
        response = self.client.get(f"{self.list_url}?name=Test Exam")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
        # Test partial name filter
        response = self.client.get(f"{self.list_url}?name__icontains=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
    def test_get_exam_detail_success(self):
        """Test successful retrieval of exam details"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Exam")
        self.assertEqual(len(response.data['questions']), 2)
        
        # Check first question
        question1 = response.data['questions'][0]
        self.assertEqual(question1['number'], 1)
        self.assertEqual(question1['question_content'], "What is 2+2?")
        self.assertEqual(len(question1['alternatives']), 3)
        
    def test_get_exam_detail_not_found(self):
        """Test exam detail retrieval with non-existent ID"""
        non_existent_id = uuid.uuid4()
        url = reverse('exam:exam-detail', kwargs={'exam_id': non_existent_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIResponseSchemaTestCase(TransactionTestCase):
    reset_sequences = True
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test data
        self.exam = Exam.objects.create(name="Test Exam")
        
        # Create questions with alternatives
        self.question1 = Question.objects.create(content="What is 2+2?")
        self.alt1_1 = Alternative.objects.create(question=self.question1, content="3", option=1, is_correct=False)
        self.alt1_2 = Alternative.objects.create(question=self.question1, content="4", option=2, is_correct=True)
        self.alt1_3 = Alternative.objects.create(question=self.question1, content="5", option=3, is_correct=False)
        
        # Add questions to exam
        self.exam.exam_questions.create(question=self.question1, number=1)
        
        # URLs
        self.list_url = reverse('exam:exam-list')
        self.detail_url = reverse('exam:exam-detail', kwargs={'exam_id': self.exam.id})
    
    def test_list_exams_response_schema(self):
        """Test that list exams endpoint response structure is correct"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response structure
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Verify results structure
        results = response.data['results']
        self.assertTrue(isinstance(results, list))
        
        if results:
            exam = results[0]
            self.assertIn('id', exam)
            self.assertIn('name', exam)
            self.assertIn('total_questions', exam)
            
            # Verify data types
            self.assertTrue(isinstance(exam['id'], str))
            self.assertTrue(isinstance(exam['name'], str))
            self.assertTrue(isinstance(exam['total_questions'], int))
            
            # Verify UUID format
            try:
                uuid.UUID(exam['id'])
            except ValueError:
                self.fail("Exam ID is not a valid UUID")
    
    def test_exam_detail_response_schema(self):
        """Test that exam detail endpoint response structure is correct"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response structure
        self.assertIn('id', response.data)
        self.assertIn('name', response.data)
        self.assertIn('questions', response.data)
        
        # Verify data types
        self.assertTrue(isinstance(response.data['id'], str))
        self.assertTrue(isinstance(response.data['name'], str))
        self.assertTrue(isinstance(response.data['questions'], list))
        
        # Verify UUID format
        try:
            uuid.UUID(response.data['id'])
        except ValueError:
            self.fail("Exam ID is not a valid UUID")
        
        # Verify questions structure
        if response.data['questions']:
            question = response.data['questions'][0]
            self.assertIn('id', question)
            self.assertIn('number', question)
            self.assertIn('question_content', question)
            self.assertIn('alternatives', question)
            
            # Verify data types
            self.assertTrue(isinstance(question['id'], str))
            self.assertTrue(isinstance(question['number'], int))
            self.assertTrue(isinstance(question['question_content'], str))
            self.assertTrue(isinstance(question['alternatives'], list))
            
            # Verify alternatives structure
            if question['alternatives']:
                alternative = question['alternatives'][0]
                self.assertIn('id', alternative)
                self.assertIn('content', alternative)
                self.assertIn('option', alternative)
                
                # Verify data types
                self.assertTrue(isinstance(alternative['id'], str))
                self.assertTrue(isinstance(alternative['content'], str))
                self.assertTrue(isinstance(alternative['option'], int))
