from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:q_ID>/vote/", views.vote, name="vote"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results")
]