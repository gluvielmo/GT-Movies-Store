from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_feedback, name='feedback.submit'),
    path('view/', views.view_feedback, name='feedback.view'),
]
