from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from like.models import Like

"""
This is the bane of my existence. Here are some resources to help you along

Using ajax in django views
https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html

Implementing a like system without any ajax help
https://github.com/domenikjones/django-like-system/blob/master/like_system/views.py

"""


# todo the CreateLikeView.get() method should create a new like object
# todo the RemoveLikeView.get() method should remove a like object


class CreateLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pass
