from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobListCreate.as_view(), name='joblistcreate'),
    path('jobs/<int:pk>/', views.JobRetrieve.as_view(), name='jobretrieve'),
    
]
