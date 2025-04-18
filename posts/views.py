from django.shortcuts import render, redirect 
from django.http import HttpResponse
from posts.models import Post
from posts.forms import PostCreateForm, PostCreateForm2, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
import random
from django.views.generic import ListView, DetailView, CreateView



def test_view(request):
    return HttpResponse("Hello World!")


class TestView(View):
    def get(self, request):
        return HttpResponse("Hello World!", {random.randint(1, 100)})


def home_page_view(request):
    return render(request, "base.html")
    

@login_required(login_url="/login/")
def post_list_view(request):
    posts = Post.objects.all()
    limit = 3 
    if request.method == "GET":
        search = request.GET.get("search")
        category = request.GET.get("category")
        ordering = request.GET.get("ordering")
        page = int(request.GET.get("page")) if request.GET.get("page") else 1
        form = SearchForm(request.GET)
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

        if category:
            posts = posts.filter(category=int(category ))
        
        if ordering:
            posts = posts.order_by(ordering)

        max_pages = posts.count() / limit
        if round(max_pages) < max_pages:
            max_pages = round(max_pages) + 1
        else:
            max_pages = round(max_pages)
  
        start = (page - 1) * limit
        end =  page * limit
        posts = posts[start:end]
        context_data = {"posts":posts, 
                        "form":form, 
                        "max_pages": range(1, max_pages + 1)} 
        return render(request, "posts/post_list.html", context = context_data)
    



class PostListView2(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"



@login_required(login_url="/login/")
def post_detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "posts/post_detail.html", context={"post":post}) 


@login_required(login_url="/login/")
def post_create_view(request):
    if request.method == "GET":
        form = PostCreateForm2()
        return render(request, "posts/post_create.html", context={"form":form})
    if request.method == "POST":
        form = PostCreateForm2(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form":form})
        elif form.is_valid():
            form.save()
            # title = form.cleaned_data.get("title")
            # content = form.cleaned_data.get("content")
            # image = form.cleaned_data.get("image")
            # post = Post.objects.create(title=title, content=content, image=image)
        # if post :
            return redirect("/posts/")
        
@login_required(login_url="/login/")
def post_update_view(request, post_id):
    post = Post.objects.filter(id=post_id, author=request.user).first()
    if not post:
        return HttpResponse("Post not found")
    if request.method == "GET":
        form = PostCreateForm2(instance=post)
        return render (
            request, "posts/post_update.html", context={"form":form}
        )
    if request.method == "POST":
        form = PostCreateForm2(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form":form})
        elif form.is_valid():
            form.save()
            return redirect("/profile/")