from django.shortcuts import render,redirect
from .models import Blog,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateBlogForm,CommentForm
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
def index(request):
    keyword = request.GET.get("search")
    msg = None
    if keyword:
        blogs = Blog.objects.filter(Q(title__icontains =keyword) | Q(body__icontains= keyword)| Q(category__title__icontains=keyword))
        if blogs.exists():
            pass
        else:
            msg = "There is no article with the keyword!"
    
    blogs = Blog.objects.filter(featured = False)
    featured_blog = Blog.objects.get(featured = True)
    paginator = Paginator(blogs,4)
    page = request.GET.get("page")
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger: 
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)  

    context = {"blogs": blogs,"f_blog":featured_blog, "msg":msg , "paginator":paginator} 
    return render(request, "blogapp/index.html",context)

def details(request,slug):
    blog =Blog.objects.get(slug= slug)
    comments = Comment.objects.filter(blog=blog)
    form = CommentForm()
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect("details", slug = blog.slug)

    context = {"blog": blog, "form": form,"comments":comments,}
    return render(request, "blogapp/detail.html",context)

@login_required(login_url="signin")
def create_article(request):
    form = CreateBlogForm()
    if request.method == "POST":
        if request.user.is_authenticated:
           form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(request.POST['title'])
            blog.user = request.user
            blog.save()
            messages.success(request, "Article Created succesfully!")
            return redirect("profile")
    context = {"form": form}
    return render(request, "blogapp/create.html",context)

@login_required(login_url="signin")
def update_article(request, slug):
    blog = Blog.objects.get(slug = slug)
    form = CreateBlogForm(instance=blog)
    update = True
    if request.method == "POST":
        form = CreateBlogForm(request.POST, request.FILES,instance=blog)
        blog = form.save(commit=False)
        blog.slug =slugify(request.POST["title"])
        blog.save()
        messages.success(request, "Article Updated Successfully!")
        return redirect("profile")

    context = {"update": update, "form": form}
    return render(request, "blogapp/create.html",context) 

@login_required(login_url="signin")
def delete_article(request, slug):
    blog = Blog.objects.get(slug= slug)
    blogs = Blog.objects.filter(user=request.user)
    delete_article = True
    if request.method =="POST":
        blog.delete()
        messages.success(request, "Article deleted succesfully!")
        return redirect("profile")
    context = {"blog": blog, "delete": delete_article, "blogs":blogs}
    return render(request,"core/profile.html", context)