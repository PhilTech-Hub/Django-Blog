from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, UserProfile, Comment, Like
from .forms import UserProfileForm, BlogForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Count, Q


# Home Page View
# Home Page View
def home_view(request):
    # Get all blogs ordered by creation date
    blogs = Blog.objects.all().order_by('-created_at')

    # Fetch blogs with at least one like or one comment
    featured_blogs = Blog.objects.annotate(
        num_likes=Count('blog_likes'),
        num_comments=Count('comments')
    ).filter(
        Q(num_likes__gt=0) | Q(num_comments__gt=0)
    ).order_by('-num_likes', '-num_comments')[:5]

    # Add total likes and comments for each blog
    for blog in blogs:
        blog.total_likes = blog.blog_likes.count()  # Count all likes
        blog.total_comments = blog.comments.count()  # Count all comments

    return render(request, 'home.html', {'blogs': blogs, 'featured_blogs': featured_blogs})



# View to display blog details and its comments
def view_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()
    like_count = blog.blog_likes.count()  # Total likes
    # Check if the user has already liked the blog
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = blog.blog_likes.filter(user=request.user).exists()

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

    return render(request, 'view_blog.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
        'like_count': like_count,
        'user_has_liked': user_has_liked,
    })


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

    return redirect('view_blog', pk=blog.pk)


# Like or Unlike Blog
@login_required
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    existing_like = blog.blog_likes.filter(user=request.user).first()

    if existing_like:
        existing_like.delete()  # Unlike the blog
        messages.info(request, 'You unliked the blog.')
    else:
        Like.objects.create(blog=blog, user=request.user)  # Like the blog
        messages.success(request, 'You liked the blog.')

    return redirect('view_blog', pk=pk)


# Share Blog
@login_required
def share_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # Placeholder logic for sharing
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
