from django.urls import path
from .views import openai_chat, diagnose_disease, get_symptoms_list, get_diseases_by_department, demo_page

urlpatterns = [
    path('chat/', openai_chat, name='openai_chat'),
    path('diagnose/', diagnose_disease, name='diagnose_disease'),
    path('symptoms/', get_symptoms_list, name='get_symptoms_list'),
    path('diseases/', get_diseases_by_department, name='get_diseases_by_department'),
    path('demo/', demo_page, name='demo_page'),
]
