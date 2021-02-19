from django.urls import path
from . import views

handler404 = 'Qpost.views.handler404'


urlpatterns = [
    path('', views.home, name="home"),
    path('detail/<int:id>', views.detail, name='detail'),
    path('save-comment', views.save_comment, name='save-comment'),
    path('save-upvote', views.save_upvote, name='save-upvote'),
    path('save-downvote', views.save_downvote, name='save-downvote'),
    # Profile

    # Ask Question
    path('ask-question/', views.ask_form, name='ask-question'),
    path('ask-question/<int:id>/', views.ask_form, name='question-update'),
    path('ask-question/delete/<int:id>/',
         views.question_delete, name='question-delete'),
    # Tag Page
    path('tag/<str:tag>/', views.tag, name='tag'),
    # Tags Page
    path('tags/', views.tags, name='tags'),


]
