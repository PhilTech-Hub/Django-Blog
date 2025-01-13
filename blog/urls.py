from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('view_blog/<int:pk>/', views.view_blog, name='view_blog'),
    path('comment_blog/<int:pk>/', views.comment_blog, name='comment_blog'),
    path('view_blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('share_blog/<int:pk>/', views.share_blog, name='share_blog'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('blog/add/', views.add_blog_view, name='add_blog'),
    path('blog/<int:pk>/update/', views.update_blog_view, name='update_blog'),
    path('blog/<int:pk>/delete/', views.delete_blog_view, name='delete_blog'),
    # Other URL patterns
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/featured_blogs/', views.featured_blogs, name='featured_blogs_api'),
]
