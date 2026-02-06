from django.urls import path
from . import views

urlpatterns = [
    path('course-list/', views.CourseListView.as_view(), name='course-list'),
    path('course-detail/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),

    path('course-add/', views.CourseCreateView.as_view(), name='course-add'),
    path('course-edit/<int:pk>/', views.CourseUpdateView.as_view(), name='course-edit'),
    path('course-delete/<int:pk>/', views.CourseDeleteView.as_view(), name='course-delete'),
]
