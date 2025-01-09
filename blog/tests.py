from .models import Blog
from django.db.models import Count, Q

# Check if any blogs meet the criteria
blogs = Blog.objects.annotate(
    num_likes=Count('blog_likes'),
    num_comments=Count('comments')
).filter(
    Q(num_likes__gt=0) | Q(num_comments__gt=0)
).order_by('-num_likes', '-num_comments')[:5]

for blog in blogs:
    print(f"Title: {blog.title}, Likes: {blog.num_likes}, Comments: {blog.num_comments}")
