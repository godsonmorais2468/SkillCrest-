from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:pk>/', views.CreateOrderView.as_view(), name='buy-course'),
    path('verify/', views.VerifyPaymentView.as_view(), name='verify-payment'),
]
