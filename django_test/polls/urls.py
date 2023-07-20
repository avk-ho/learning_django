from django.urls import path

from . import views

app_name = "polls"
# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"), # route "", view (views.py), kwargs, name
#     # ex: /polls/2
#     path("<int:question_id>/", views.detail, name="detail"),
#     # ex: /polls/2/results/
#     path("<int:question_id>/results/", views.results, name="results"),
#     # ex: /polls/2/vote
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]
# les names sont repris dans les templates pour les redirections

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]