from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import AuthorRequest, Post, Category
from .forms import PostForm, ProfileForm

def home(request):
    posts = Post.objects.all()
    show_modal = request.session.pop('show_modal', False)
    context = {
        'posts': posts,
        'show_modal': show_modal,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post,
    }
    return render(request, 'post_detail.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def request_author(request):
    if request.method == 'POST':
        AuthorRequest.objects.create(user=request.user)
        return redirect('profile')
    return render(request, 'request_author.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def create_post(request):
    if not request.user.is_author:
        request.session['show_modal'] = True
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.author:
        post.delete()
    return redirect('home')

def search_posts(request):
    category = request.GET.get('category')
    author = request.GET.get('author')
    posts = Post.objects.all()
    if category:
        posts = posts.filter(categories__name=category)
    if author:
        posts = posts.filter(author__username=author)
    return render(request, 'search_results.html', {'posts': posts})
