"""
Implements CRUD in views. These are native to Django
"""
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Comment
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .forms import CommentForm


# def home(request):
#     context = {
#         "posts": Post.objects.all()
#     }
#     return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostsView(View):
    def get(self, request, pk):
        # post = Post.objects.filter(pk=pk).first()
        post = get_object_or_404(Post, pk=pk)
        comments = Paginator(Comment.objects.filter(post=post), 5)
        likes = post.likes.all()

        # fixme page_num approach doesn't work consider looking at templateView and pagination
        # https://docs.djangoproject.com/en/3.0/ref/class-based-views/base/#templateview
        page_num = self.kwargs.get("page")

        if page_num is None:
            page_num = 1

        comments = comments.page(page_num)

        context = {"post": post, "comments": comments, "likes": likes}

        if request.user.is_authenticated:
            comment_form = CommentForm()
            context["comment_form"] = comment_form

        return render(request, "blog/post_detail.html", context)

    def post(self, request, pk, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        comment_form.instance.author = self.request.user
        comment_form.instance.post_id = pk
        if comment_form.is_valid():
            comment_form.save()
            # context = {
            #     "comment_form": comment_form,
            #     "post": Post.objects.filter(pk=pk).first()
            # }
            # return render(request, "blog/post_detail.html", context)
            return redirect("post-detail", pk=pk)


class PostCommentListView(ListView):
    model = Comment
    paginate_by = 10
    context_object_name = "comment"

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        self.extra_context = {"post": self.post}
        return Comment.objects.filter(post=self.post).order_by("-date_posted")


"""
class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")
"""


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        """
        Used by CreateView to be called to verify if form is valid. This is used to
        set the post's author to the current user
        @param form: The form in question
        @return: Calls the CreateView form_valid method with the adjusted form
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        """
        Used by UpdateView to be called to verify if form is valid. This is used to
        set the post's author to the current user
        @param form: The form in question
        @return: Calls the UpdateView form_valid method with the adjusted form
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        """
        Required by UserPassesTestMixin. Used to determine if the user is the post's
        author
        @return: True if user is post's author, False if not
        @rtype: boolean
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        """
        Used by CreateView to be called to verify if form is valid. This is used to
        set the comment's author to the current user
        @param form: The form in question
        @return: Calls the CreateView form_valid method with the adjusted form
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
