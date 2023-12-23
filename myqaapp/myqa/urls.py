from django.urls import path
from . import views

app_name = 'myqa'

urlpatterns = [
    path('', views.index, name='index'),
    path('browse_file/', views.browse_file, name='browse_file'),
    path('answer_question/', views.answer_question, name='answer_question'),
]
