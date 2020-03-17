from django.urls import path
from .views import Apply, CandidateDetailView, CandidateListView, ScheduleListView, ScheduleDetailView, VerifyView

app_name = 'scheduler'
urlpatterns = [
    path('apply/', Apply.as_view(), name='apply'),
    path('verify/<str:token>', VerifyView.as_view(), name='verify'),
    path('candidate_list/', CandidateListView.as_view(), name='candidate_list'),
    path('candidate_detail/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('schedule_list/', ScheduleListView.as_view(), name='interviewer_schedule_list'),
    path('schedule_detail/<int:pk>/', ScheduleDetailView.as_view(), name='interviewer_schedule_detail'),
]