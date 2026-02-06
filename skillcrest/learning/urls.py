from django.urls import path
from .views import CourseLessonsView

urlpatterns = [
    path('course/<int:pk>/lessons/', CourseLessonsView.as_view(), name='course-lessons'),
]
