from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import CreateUserForm, ProfileUpdateForm, UserUpdateForm, PictureUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.models import Post
from group.models import Group
from .models import Profile
from django.utils import timezone
from datetime import datetime
# Create your views here.


@staff_member_required(login_url="/blog/home")
def user_create(request):
    ''' To create users by the admin'''
    user_form = CreateUserForm()
    groups = Group.objects.all()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST or None)
        user_ids = list(Profile.objects.values_list('college_id', flat=True))
        emails = list(User.objects.values_list('email', flat=True))
        # to validate the posted data
        if request.POST['college_id'] in user_ids:
            messages.error(request, 'College ID already exists!')
            return redirect('user_create')
        elif request.POST['email'] in emails:
            messages.error(request, 'User with the email already exists')
            return redirect('user_create')
        elif user_form.is_valid():
            user_form.save()
            profile = Profile.objects.get(user=user_form.instance)
            profile.college_id = request.POST['college_id']
            profile.user_type = request.POST['user_type']
            profile.save()
            
            # to add the user to a group, if selected
            if 'group-select' in request.POST:
                group_id = request.POST['group-select']
                Group.objects.get(id=group_id).user.add(user_form.instance)
            
            user = user_form.cleaned_data.get('username')
            Group.objects.get(name="home").user.add(user_form.instance)
            messages.success(request, 'Account was created for '+ user)
            return redirect('user_create')

    context = {
        'user_form': user_form,
        'users': User.objects.all(),
        'groups': groups,
        'title': 'Create User'
    }
    return render(request, 'users/user_create.html', context)

@staff_member_required(login_url="/blog/home")
def user_update(request, id):
    ''' To update users by the admin '''
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateForm(instance=profile)
    user_form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.instance.user = user_form.instance
            profile_form.save()
            return redirect('user_create')
        
    context={
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Update User'

    }
    return render(request, 'users/user_update.html', context)

@staff_member_required(login_url="/blog/home")
def user_delete(request):
    ''' To delete a user by the admin '''
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST['user-delete-id']
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('user_create')
    return redirect('post', name='home')


@login_required
def profile(request, id):
    ''' To view profile of others as well as yourself '''
    profile_user = User.objects.get(id=id)
    accepted_posts = Post.objects.filter(author=profile_user, verification='accepted')
    posts = Post.objects.filter(author=profile_user).exclude(verification='accepted')
    profile = Profile.objects.get(user=profile_user)
    profile_groups = Group.objects.filter(user=profile_user).exclude(name="home")
    request_user_groups = Group.objects.filter(user=request.user)
    if request.method == "POST":
        declined_posts = Post.objects.filter(author=request.user, verification='declined')
        for post in declined_posts:
            post.delete()
    context = {
        'accepted_posts': accepted_posts,
        'profile_user': profile_user,
        'posts': posts,
        'profile': profile,
        'groups': Group.objects.filter(user=request.user),
        'profile_groups': profile_groups,
        'request_user_groups': request_user_groups,
        'title': 'Profile ' + profile_user.first_name + ' ' + profile_user.last_name
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_update(request):
    ''' To update profile pictuer of user '''
    if request.method == 'POST':
        profile_form = PictureUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', request.user.id)

    else:
        profile_form = PictureUpdateForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
        'title': 'Update Profile: ' + request.user.first_name + ' ' + request.user.last_name,
        'groups': Group.objects.filter(user=request.user)
        
    }

    return render(request, 'users/profile_update.html', context)


@staff_member_required(login_url="/blog/home")
def dashboard(request):
    ''' To view the dashboard by the admin '''
    recent_posts = Post.objects.all()[:5]
    last_login_users = User.objects.all().order_by('-last_login')[:5]
    context = {
        'recent_posts': recent_posts,
        'last_login_users': last_login_users,
        'title': 'Dashboard'
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def password_change(request):
    ''' To change the password of a user '''
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile', id=request.user.id)
    context = {
        'form': form,
        'title': 'Change Password',
        'groups': Group.objects.filter(user=request.user)
    }
    return render(request, 'users/password_change.html',context)

@staff_member_required
def recent_posts(request, name):
    ''' To view posts from all groups '''
    groups = Group.objects.all()
    posts = Post.objects.filter(group=Group.objects.get(name=name))
    today = datetime.now()
    context ={
        'groups': groups,
        'posts': posts,
        'today': today,
        'name': name,
        'title': 'Recent Posts'
    }

    return render(request, 'users/recent_posts.html', context)

@staff_member_required
def recent_logins(request, name):
    
    ''' To view the recently logged in users '''

    groups = Group.objects.all()
    users = Group.objects.get(name=name).user.all()
    context = {
        'groups': groups,
        'users': users,
        'name': name
    }
    return render(request, 'users/recent_logins.html', context)