from django.shortcuts import render,redirect
from django.http import HttpResponse
from Post.forms import SignUpForm,LoginForm,ArticleForm,CommentForm,ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from .models import Blog,Comment,Profile
from django.utils.html import strip_tags
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request,'Post/index.html')

def signup(request):
    if(request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email,email=email,password=password)
            user.save()
            return redirect('/')
        else:
            return redirect('/signup')
    return render(request,'Post/signup.html')

def login(request):
    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email,password=password)
            if user is not None:
                request.session['email'] = email
                return redirect('/',email=email)
            else:
                print("wrong user")
                return redirect('/login')
        else:
            pass    
    return render(request,'Post/login.html')


def createArticle(request):
    if(request.method == 'POST'):
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = strip_tags(form.cleaned_data['content'])
            username = request.session['email']
            user = User.objects.get(username=username)
            if user is not None:
                print(user)
                blog = Blog.objects.create(title=title,body=body,creator=user)
                blog.save()
                return redirect('/')
            else:
                return redirect('/login')
        else:
            return redirect('/create/article')
    return render(request,'Post/articlesForm.html')


def getArticles(request):
    blogs = Blog.objects.all()
    newBlog = []
    for blog in blogs:
        if(Comment.objects.filter(blog_id=blog.id)):
            blog.totalComment = len(Comment.objects.filter(blog_id=blog.id))
            blog.save()
            newBlog.append(blog)
        else:
            newBlog.append(blog)

    context = {
        'blogs':newBlog
    }
    return render(request,'Post/allarticles.html',context=context)

def getArticle(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    comment = Comment.objects.filter(blog_id=blog_id)
    if blog is not None:
        context = {
            'blog':blog,
            'comments':comment,
        }
        return render(request,'Post/article.html',context=context)
    else: 
        return redirect('/articles')

def postComment(request,blog_id):
    if(request.method == 'POST'):
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            blog = Blog.objects.get(id=blog_id)
            username = request.session['email']
            user = User.objects.get(username=username)
            if(user and blog is not None):
                comment = Comment.objects.create(body=body,creator=user,blog=blog)
                comment.save()
                return redirect('article',blog_id=blog_id)
            else:
                print('cant save')
        else:
            return HttpResponse('hi')
       
def increaseLike(request,blog_id):
    blog = Blog.objects.get(id=blog_id)
    if(blog is not None):
        if(blog.totalLikes is not None):
            blog.totalLikes = blog.totalLikes + 1
        else:
            blog.totalLikes = 1
        blog.save()
        return redirect('articles')
    
def getProfile(request):
    username = request.session['email']
    user = User.objects.get(username=username)
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = None        
    if user and profile is not None:
        context = {
            'profile':profile
         }
        return render(request,'Post/profile.html',context=context)
    else:
        return redirect('editprofile',profile_id=user.id)
    
def editProfile(request,user_id):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            try:
                profile = Profile.objects.get(user_id=user_id)
            except Profile.DoesNotExist:
                profile = None    
            if(user and profile is not None):
                birthday = form.cleaned_data['birthday']
                bio = form.cleaned_data['bio']
                profilePicture = form.cleaned_data['profilePicture']
                profile.birthday = birthday
                profile.bio = bio
                profile.profilePicture = profilePicture
                profile.save()
                return redirect('userprofile')
            else:
                birthday = form.cleaned_data['birthday']
                bio = form.cleaned_data['bio']
                profilePicture = form.cleaned_data['profilePicture']
                profile = Profile.objects.create(user=user,profilePicture=profilePicture,birthday=birthday,bio=bio)
                return redirect('userprofile')

        else:
            return HttpResponse('sth wrong')
    else:
        try:
            profile = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None:
            context = {
                'profile':profile
            }
            return render(request,'Post/edit_profile.html',context=context)
        else:
            return render(request,'Post/edit_profile.html')


        

def log_out(request):
    logout(request)
    return redirect('/')
