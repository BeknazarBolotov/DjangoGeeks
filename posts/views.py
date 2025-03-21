from django.shortcuts import render
from django.http import HttpResponse


def test_view(request):
    return HttpResponse("Hello World!")


def html_view(request):
    return render(request, "posts/test.html")
    