# Generated by Django 5.0.6 on 2024-11-04 22:36

import sys

from django.db import migrations
from question.utils import AlternativesChoices

exams = [
    {
        'name': 'Prova Falsa 1',
        'questions': [
            {
                'content': 'Qual parte do corpo usamos para ouvir?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Dentes', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Cabelos', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Ouvidos', 'is_correct': True},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Braços', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para ver?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Pés', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Olhos', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Mãos', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Ouvidos', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para cheirar?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Nariz', 'is_correct': True},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Língua', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Braços', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Pés', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para falar?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Ouvidos', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Mãos', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Boca', 'is_correct': True},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Pernas', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para andar?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Braços', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Pés', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Olhos', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Dentes', 'is_correct': False}
                ]
            }
        ]
    },
    {
        'name': 'Prova Falsa 2',
        'questions': [
            {
                'content': 'Qual órgão é responsável por bombear o sangue?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Pulmões', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Estômago', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Coração', 'is_correct': True},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Fígado', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para segurar objetos?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Pés', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Cabeça', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Mãos', 'is_correct': True},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Nariz', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual é o maior órgão do corpo humano?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Cérebro', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Pele', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Coração', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Pulmões', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual órgão é essencial para a digestão?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Fígado', 'is_correct': True},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Cérebro', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Olhos', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Mãos', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual órgão usamos para pensar?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Cérebro', 'is_correct': True},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Coração', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Estômago', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Pés', 'is_correct': False}
                ]
            }
        ]
    },
    {
        'name': 'Prova Falsa 3',
        'questions': [
            {
                'content': 'Qual parte do corpo usamos para sentir o gosto dos alimentos?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Dentes', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Língua', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Mãos', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Pés', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo é usada para respirar?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Olhos', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Nariz', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Pés', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Mãos', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo usamos para chutar uma bola?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Braços', 'is_correct': False},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Pés', 'is_correct': True},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Cabeça', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Dedos', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual parte do corpo é coberta de cabelo?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Cabeça', 'is_correct': True},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Pés', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Dentes', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Língua', 'is_correct': False}
                ]
            },
            {
                'content': 'Qual órgão é essencial para a respiração?',
                'alternatives': [
                    {'alternative': AlternativesChoices.A.value, 'content': 'Pulmões', 'is_correct': True},
                    {'alternative': AlternativesChoices.B.value, 'content': 'Estômago', 'is_correct': False},
                    {'alternative': AlternativesChoices.C.value, 'content': 'Cérebro', 'is_correct': False},
                    {'alternative': AlternativesChoices.D.value, 'content': 'Fígado', 'is_correct': False}
                ]
            }
        ]
    }
]


def populate_exam_data(apps, schema_editor):
    if 'test' in sys.argv:
        return
    Exam = apps.get_model('exam', 'Exam')
    Question = apps.get_model('question', 'Question')
    Alternative = apps.get_model('question', 'Alternative')
    ExamQuestion = apps.get_model('exam', 'ExamQuestion')

    exam_question_relations = []
    alternatives = []
    for exam_data in exams:
        exam = Exam.objects.create(name=exam_data['name'])

        for index, question_data in enumerate(exam_data['questions']):
            question = Question.objects.create(content=question_data['content'])

            for alternative_data in question_data['alternatives']:
                alternatives.append(Alternative(
                    question=question,
                    content=alternative_data['content'],
                    option=alternative_data['alternative'],
                    is_correct=alternative_data['is_correct']
                ))

            exam_question_relations.append(ExamQuestion(
                exam=exam,
                question=question,
                number=index + 1
            ))

    Alternative.objects.bulk_create(alternatives)
    ExamQuestion.objects.bulk_create(exam_question_relations)

class Migration(migrations.Migration):
    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_exam_data, reverse_code=migrations.RunPython.noop),
    ]
