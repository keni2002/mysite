from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post,Comment
from django.core.mail import send_mail
from mysite import settings
# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def post_list(request):
    post_detail = Post.published.all()
    #Pagination with 3 posts per page
    paginator = Paginator(post_detail,3)
    page_number = request.GET.get('page',1)
    try:
        posts =paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'posts':posts})

#SEO friendly
def post_detail(request,post,year,month,day):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,'blog/post/detail.html',{'post':post})


##alternative to view function is Class based view
from django.views.generic import ListView
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


from .forms import EmailPostForm, CommentForm

def post_share(request,post_id):
    #retrieve post by id
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            #only clean the incorrect camp
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


from django.views.decorators.http import require_POST
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