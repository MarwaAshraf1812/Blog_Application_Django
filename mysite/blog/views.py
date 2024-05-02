from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

# def post_list(request):
#     from django.core.paginator import Paginator, EmptyPage,\
#     PageNotAnInteger
#     posts = Post.published.all()
#     Paginator = Paginator(posts, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = Paginator.get_page(page_number)
#     except PageNotAnInteger:
#         # If page_number is not an integer deliver the first page
#         posts = Paginator.get_page(1)
#     except EmptyPage :
#         # If page_number is out of range deliver last page of results
#         posts = Paginator.get_page(Paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'posts': posts})
class PostListView(ListView):
    """
    Alternative to the post_list view function.
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    """
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(request, 'blog/post/details.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'ashrafmarwa987@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
