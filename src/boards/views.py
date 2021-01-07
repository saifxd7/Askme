from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Board, Topic, Post
from .forms import CreateTopicForm, PostForm


@login_required
def home(request):
    boards = Board.objects.all()
    return render(request, 'blog/board.html', {'boards': boards})


@login_required
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'blog/topics.html', {'board': board, 'topics': topics})


@login_required
def create_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # get the currently logged in user
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            # redirect to the created topic page
            return redirect('blog/board_topics', pk=board.pk)
    else:
        form = CreateTopicForm()
    return render(request, 'blog/create_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'blog/topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'blog/reply_topic.html', {'topic': topic, 'form': form})


@login_required
def create_question(request):
    # board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # get the currently logged in user
    if request.method == 'POST':
        form = CreateTopicForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            # topic.board = board
            topic.starter = user
            question.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                question=question,
                created_by=user
            )
            # redirect to the created topic page
            return redirect('board_topics')
    else:
        form = CreateTopicForm()
    return render(request, 'create_question.html', {'form': form})
