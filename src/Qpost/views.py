from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from .models import Question, Answer, Comment, UpVote, DownVote
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import AnswerForm, QuestionForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count


from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage

# Home Page


def home(request):
    title = "AskNow - Home"
    if 'q' in request.GET:
        q = request.GET['q']
        quests = Question.objects.annotate(total_comments=Count(
            'answer__comment')).filter(title__icontains=q).order_by('-id')
    else:
        quests = Question.objects.annotate(
            total_comments=Count('answer__comment')).all().order_by('-id')
    paginator = Paginator(quests, 5)
    page_num = request.GET.get('page', 1)
    quests = paginator.page(page_num)
    return render(request, 'index.html', {'quests': quests, 'title': title})


# Detail
@login_required
def detail(request, id):

    quest = Question.objects.get(pk=id)
    tags = quest.tags.split(',')
    answers = Answer.objects.filter(question=quest)
    answerform = AnswerForm
    if request.method == 'POST':
        answerData = AnswerForm(request.POST)
        if answerData.is_valid():
            answer = answerData.save(commit=False)
            answer.question = quest
            answer.user = request.user
            answer.save()
            messages.success(request, 'Answer has been submitted.')
    return render(request, 'detail.html', {
        'quest': quest,
        'tags': tags,
        'answers': answers,
        'answerform': answerform,

    })


@login_required
def ask_form(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = QuestionForm
        else:
            question = Question.objects.get(pk=id)
            if question.user.id != request.user.id:
                raise Http404
            form = QuestionForm(instance=question)
        return render(request, 'ask-question.html', {'form': form})
    else:
        if id == 0:
            form = QuestionForm(request.POST)
        else:

            question = Question.objects.get(pk=id)
            if question.user.id != request.user.id:
                raise Http404
            form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

        return redirect('home')

# Save Comment


def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']

        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        Comment.objects.create(
            answer=answer,
            comment=comment,
            user=user
        )
        return JsonResponse({'bool': True})


# Save Upvote


def save_upvote(request):
    if request.method == 'POST':
        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        check = UpVote.objects.filter(answer=answer, user=user).count()
        if check > 0:
            return JsonResponse({'bool': False})
        else:
            UpVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool': True})


# Save Downvote

def save_downvote(request):
    if request.method == 'POST':
        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        check = DownVote.objects.filter(answer=answer, user=user).count()
        if check > 0:
            return JsonResponse({'bool': False})
        else:
            DownVote.objects.create(
                answer=answer,
                user=user
            )
            return JsonResponse({'bool': True})


# delete question
@login_required
def question_delete(request, id):
    question = Question.objects.get(pk=id)
    question.delete()
    return redirect('home')

# delete answer


def answer_delete(request, id):
    answer = Answer.objects.get(pk=id)
    if answer.user.id != request.user.id:
        raise Http404
    answer.delete()
    return redirect('home')

# delete comment


def delete_comment(request, id):
    comment = Comment.objects.get(pk=id)
    if comment.user.id != request.user.id:
        raise Http404
    comment.delete()
    return redirect('home')


# Questions according to tag
@login_required
def tag(request, tag):
    quests = Question.objects.annotate(total_comments=Count(
        'answer__comment')).filter(tags__icontains=tag).order_by('-id')
    paginator = Paginator(quests, 10)
    page_num = request.GET.get('page', 1)
    quests = paginator.page(page_num)
    return render(request, 'tag.html', {'quests': quests, 'tag': tag})


# Tags Page

@login_required
def tags(request):
    quests = Question.objects.all()
    tags = []
    for quest in quests:
        qtags = [tag.strip() for tag in quest.tags.split(',')]
        for tag in qtags:
            if tag not in tags:
                tags.append(tag)
    # Fetch Questions
    tag_with_count = []
    for tag in tags:
        tag_data = {
            'name': tag,
            'count': Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request, 'tags.html', {'tags': tag_with_count})


# upload image
@requires_csrf_token
def upload_image_view(request):
    f = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(f).split('.')[0]
    file = fs.save(filename, f)
    fileurl = fs.url(file)

    return JsonResponse({'success': 1, 'file': {'url': fileurl}})


# upload file
@requires_csrf_token
def upload_file_view(request):
    f = request.FILES['file']
    fs = FileSystemStorage()
    filename, ext = str(f).split('.')
    file = fs.save(filename, f)
    fileurl = fs.url(file)

    return JsonResponse({'success': 1, 'file': {'url': fileurl, 'size': fs.size(filename), "name": str(f), "extension": ext}})
