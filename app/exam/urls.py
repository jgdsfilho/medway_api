from django.urls import path

from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.list_exams, name='exam-list'),
    path('<uuid:exam_id>/', views.get_exam_detail, name='exam-detail'),
]
