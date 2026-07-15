from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
]
