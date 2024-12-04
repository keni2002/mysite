from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post

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