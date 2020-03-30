from django.urls import path
from .views import Apply, CandidateDetailView, HRDashboardView, InterviewerDashboardView, ScheduleDetailView, VerifyView, \
    ProfileView, SuccessApply, ScheduleDeleteView, TechnicalView, PracticalView, Search

app_name = 'scheduler'
urlpatterns = [
    path('apply/', Apply.as_view(), name='apply'),
    path('verify/<str:token>/', VerifyView.as_view(), name='verify'),
    path('success_apply/<str:token>/', SuccessApply.as_view(), name='success_apply'),
    path('profile/<str:token>/', ProfileView.as_view(), name='profile'),
    path('hr_dashboard/', HRDashboardView.as_view(), name='hr_dashboard'),
    path('candidate_detail/<int:pk>/', CandidateDetailView.as_view(), name='candidate_detail'),
    path('interviewer_dashboard/', InterviewerDashboardView.as_view(), name='interviewer_dashboard'),
    path('schedule_detail/<int:pk>/', ScheduleDetailView.as_view(), name='schedule_detail'),
    path('technical_view/<int:pk>/', TechnicalView.as_view(), name='technical_view'),
    path('practical_view/<int:pk>/', PracticalView.as_view(), name='practical_view'),
    path('schedule_delete/<int:pk>/<int:candidate_id>/', ScheduleDeleteView.as_view(), name='schedule_delete'),
    path('search/', Search.as_view(), name='search'),
]