from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post


def test_view(request):
    return HttpResponse("Hello World!")


def home_page_view(request):
    return render(request, "base.html")
    


def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", context = {"posts":posts})