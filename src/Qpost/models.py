from django.db import models
from django.contrib.auth.models import User

from accounts.models import CustomUser

from django_editorjs import EditorJsField
# Custom User Model


# Question Model
class Question(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    detail = EditorJsField(editorjs_config={
        'tools': {
            'Image': {
                "config": {
                    'endpoints': {
                        'byFile': '/imageUpload/',
                        'byUrl': '/imageUpload/',
                    },
                    'additionalRequestHeaders': [{"content-Type": 'multipart/form-data'}]}
            },
            "Attaches": {
                "config": {
                    "endpoint": '/fileUpload/'
                },

            }
        }
    })

    tags = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Answer Model


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    detail = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.detail

# Comment


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comment_user')
    comment = models.TextField(default='', blank=False)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

# UpVotes


class UpVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='upvote_user')

# DownVotes


class DownVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='downvote_user')
