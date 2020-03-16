from django.urls import path
from .views import CandidateDetailView, CandidateListView

app_name = 'scheduler'
urlpatterns = [
    path('candidate_list/', CandidateListView.as_view(), name='candidate_list'),
    path('candidate_detail/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
]