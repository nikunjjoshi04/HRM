from django.urls import path
from .views import Apply, CandidateDetailView, HRDashboardView, ScheduleListView, ScheduleDetailView, VerifyView, \
    ProfileView

app_name = 'scheduler'
urlpatterns = [
    path('apply/', Apply.as_view(), name='apply'),
    path('verify/<str:token>', VerifyView.as_view(), name='verify'),
    path('profile/<str:token>', ProfileView.as_view(), name='profile'),
    path('hr_dashboard/', HRDashboardView.as_view(), name='hr_dashboard'),
    path('candidate_detail/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('schedule_list/', ScheduleListView.as_view(), name='interviewer_schedule_list'),
    path('schedule_detail/<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
]