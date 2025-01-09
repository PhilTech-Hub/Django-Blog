from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, UserProfile, Comment
from .forms import UserProfileForm, BlogForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages


# Create your views here.

# Home Page View
def home_view(request):
    # Fetch all blogs, ordered by the most recent
    blogs = Blog.objects.all().order_by('-created_at')  # Order blogs by 'created_at' descending
    return render(request, 'home.html', {'blogs': blogs})

# View to display blog details and its comments
def view_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()  # Using the 'comments' related name

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('view_blog', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'view_blog.html', {'blog': blog, 'comments': comments, 'form': form})

# Comment on Blog
@login_required
def comment_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        if comment_content:
            Comment.objects.create(blog=blog, user=request.user, content=comment_content)
            messages.success(request, 'Comment posted successfully.')
            return redirect('view_blog', pk=blog.pk)
        else:
            messages.error(request, 'Please write something before posting your comment.')
    
    return redirect('view_blog', pk=blog.pk)  # If GET, just redirect back to the blog view

# Like Blog
@login_required
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # Logic for liking the blog, for simplicity, just increment a like counter
    blog.likes += 1
    blog.save()
    messages.success(request, 'You liked the blog.')
    return redirect('view_blog', pk=blog.pk)

# Share Blog
@login_required
def share_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # Logic to share the blog (this could be sending an email, sharing to social media, etc.)
    # For simplicity, we'll just show a success message
    messages.success(request, 'Blog shared successfully.')
    return redirect('view_blog', pk=blog.pk)

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Profile View
@login_required
def profile_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

# Add Blog View
@login_required
def add_blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.userprofile
            blog.save()
            messages.success(request, 'Blog post created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})

# Update Blog View
@login_required
def update_blog_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user.userprofile)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'update_blog.html', {'form': form, 'blog': blog})

# Delete Blog View
@login_required
def delete_blog_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user.userprofile)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted successfully.')
        return redirect('home')
    return render(request, 'delete_blog.html', {'blog': blog})
