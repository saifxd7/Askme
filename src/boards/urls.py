from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('categories/<int:pk>/', views.board_topics, name='board_topics'),
    path('categories/<int:pk>/create_topic/',
         views.create_topic, name="new_topic"),
    path('create_question/',
         views.create_question, name="new_question"),
    path('categories/<int:pk>/topics/<str:topic_pk>/',
         views.topic_posts, name="topic_posts"),

    path('categories/<int:pk>/topics/<str:topic_pk>/reply/',
         views.reply_topic, name="reply_topic"),
]
