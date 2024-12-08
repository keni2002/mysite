from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.decorators.http import require_POST,require_GET
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post,Comment
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector
from mysite import settings
from taggit.models import Tag
# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# Create your views here.

def post_list(request,tag_slug=None):
    post_list = Post.published.all()
    tag = None
    #Pagination with 3 posts per page
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1) # key,default
    try:
        posts =paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'posts':posts,'tag':tag})

#SEO friendly
def post_detail(request,post,year,month,day):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    #form for users to comment
    form = CommentForm()
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   'form':form,
                   'similar_posts':similar_posts})


##alternative to view function is Class based view
from django.views.generic import ListView
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'




def post_share(request,post_id):
    #retrieve post by id
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #sending email
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,settings.EMAIL_HOST_USER, [cd['to']])
            sent = True

    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,'form':form,'sent':sent})



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    #a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
         # Assign the post to the comment
        comment.post  = post
        #save
        comment.save()
    return render(request, 'blog/post/comment.html', {'post':post,'form':form,'comment':comment})

def post_search(request):
    form = SearchForm
    query = None
    results = []
    if 'query' in request.GET:
        form  = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title','body'),).filter(search=query)

    return render(request,'blog/post/search.html',{'form':form,
                                                       'query':query,
                                                       'results':results})
