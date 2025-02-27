from django.urls import path

from . import views

app_name = 'submission'

urlpatterns = [
    path('submit/', views.submit_exam, name='submit_exam'),
    path('results/<uuid:submission_id>/', views.get_exam_result, name='exam_result'),

] 