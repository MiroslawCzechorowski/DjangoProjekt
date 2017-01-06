from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext

def handler404(request):
    msg = EmailMessage(
        sender='admin@your-app.com',
        to='miroslawczechorowski@gmail.com',
        subject='500 ERROR ALERT',
        html='A 500 error has occurred. Check your app’s logs for more information.')
    msg.send()
    response = render_to_response('blog/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    msg = EmailMessage(
        sender='admin@your-app.com',
        to='miroslawczechorowski@gmail.com',
        subject='500 ERROR ALERT',
        html='A 500 error has occurred. Check your app’s logs for more information.')
    msg.send()
    response = render_to_response('blog/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

#def newsletter(request):
#    return render(request, 'newsletter/newsletter_list.html', None)

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 12)# Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,  instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return register_success(request)
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form' : form})


def register_success(request):
    return render(request, 'blog/success.html')


def logout_page(request):
    return HttpResponseRedirect('/')


@login_required
def home(request):
    return render(
        '/',
        {'user': request.user}
    )