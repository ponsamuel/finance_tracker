from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_transaction, name='add_transaction'),
    path('update/<int:pk>/', views.update_transaction, name='update_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('', views.view_transactions, name='view_transactions'),
]
