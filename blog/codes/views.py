from django.shortcuts import render,get_object_or_404,redirect
from  .models import Post,Signup,Comments,Author,PostView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q, Count
from .forms import CommentForm,ContentForm
from django.urls import reverse

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    qs = Post\
        .objects\
            .values('categories__title')\
                .annotate(Count('categories__title'))
    return qs

def search(request):
    queryset = Post.objects.all()
    q = request.GET.get('q')
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q)|Q(overview__icontains=q)
        ).distinct()

    context = {
        'qs': queryset
    }
    return render(request,'search.html',context)


def home(request):
    featured =  Post.objects.filter(featured=True).order_by('-timestamp')[0:3]               
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        return redirect('home')
    context = {
        'object_list':featured,
    }
    return render(request, 'index.html',context)

def post(request,id):
    post = get_object_or_404(Post,id=id)
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[0:4]
    PostView.objects.create(user=request.user, post=post)
    form = CommentForm(request.POST or None)
    comment = Comments.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            # because i added a a foreign model 
            # form.instance.user = request.user
            form.instance.post = post
            form.save()
            form = CommentForm()
            return redirect(reverse('post', kwargs={
                'id':post.pk
            }))

    context = {
        'post': post,
        "category_count":category_count,
        'latest': latest,
        'form': form,
        'comment': comment,
    }
    return render(request, 'post.html',context)

def post_create(request):
    title = 'create'
    form = ContentForm(request.POST  or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={"id":form.instance.id}))
    context = {
        "title":title,
        "form": form
    }
    return render(request, 'create.html', context)
def post_update(request,id):
    title = 'update'
    post = get_object_or_404(Post,id=id)
    form = ContentForm(request.POST  or None, request.FILES or None,instance=post)
    author = get_author(request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post', kwargs={"id":form.instance.id}))
    context = {
        'title':title,
        "form": form
    }
    return render(request, 'create.html', context)
def post_delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('blog')



def blog(request):
    category_count = get_category_count()
    latest = Post.objects.order_by('-timestamp')[0:3]
    blog = Post.objects.order_by('-timestamp')
    paginator = Paginator(blog,4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_qs= paginator.page(page)
    except PageNotAnInteger:
        paginated_qs = paginator.page(1)
    except EmptyPage:
        paginated_qs =paginator.page(paginator.num_pages)
    context = {
        'latest': latest,
        "blogs": paginated_qs,
        'page_request_var': page_request_var,
        "category_count":category_count,
    }

    return render(request, 'blog.html',context)
