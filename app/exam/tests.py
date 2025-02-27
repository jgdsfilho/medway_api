import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Exam
from question.models import Question, Alternative


class ExamAPITestCase(TestCase):
    def setUp(self):
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
