from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from blog.models import Post
from like.models import Like

"""
This is the bane of my existence. Here are some resources to help you along

Using ajax in django views
https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html

Implementing a like system without any ajax help
https://github.com/domenikjones/django-like-system/blob/master/like_system/views.py

"""


class CreateLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):

        # post = Post.objects.filter(pk=pk).first()
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        not_liked = Like.objects.filter(post=post.id, user=user.id).first() is None

        if not_liked:
            new_like = Like(post=post, user=user)
            new_like.save()
            messages.success(request, f"Successfully liked {post.title}!")
        else:
            raise Exception("Failed to like post")

        return redirect("post-detail", pk=pk)


class RemoveLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):

        post = get_object_or_404(Post, pk=pk)
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()
        like.delete()

        return redirect("post-detail", pk=pk)
