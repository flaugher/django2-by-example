from pdb import set_trace as debug

from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .forms import CommentForm, EmailPostForm
from .models import Comment, Post

from taggit.models import Tag


def post_detail(request, year, month, day, post):
    """Get a post's details."""
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)

    # List of active comments for the post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save it to the database yet.
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment.
            new_comment.post = post
            # Save the comment to the database.
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Retrieve list of similar posts.
    # Note: post.tags gets all tags for the given post. Posts and tags
    # have a many-many relationship.
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get all posts that contain any of the tags associated with this post.
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    # Count generates a calculated field 'same_tags' which contains the
    # number of tags a post shares with the given post.  similar_posts
    # is a query set. Therefore similar_posts[0].same_tags tells you how
    # many tags the post in similar_posts[0] shares with the given post.
    # See https://shrtm.nu/FYrV
    # Display the first four posts that share the largest number of tags
    # with the given post.
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]

    # django-taggit includes a similar_objects() manager that you can use to retrieve objects by shared tags.
    # See these:
    # https://shrtm.nu/PaNj
    # https://shrtm.nu/fSDY
    # https://shrtm.nu/lfqv

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})

def post_list(request, tag_slug=None):
    """List published posts."""
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Since posts and tags have a many-to-many relationship
        # we have to filter by tags contained in the given list
        # which, in this case, contains only one tag element.
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})

def post_share(request, post_id):
    """Retrieve post by id."""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation.
            cd = form.cleaned_data
            # Send email.  build_absolute_uri builds a complete email including
            # the HTTP schema and hostname.
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = '{} ({}) recommends you reading " {}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments']
            )
            send_mail(subject, message, 'flaugher@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

#class PostListView(ListView):
#    """List published posts."""
#    queryset = Post.published.all()
#    context_object_name = 'posts'
#    paginate_by = 3
#    template_name = 'blog/post/list.html'