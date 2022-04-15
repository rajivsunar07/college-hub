from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CreateGroupForm
from .models import Group
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

@staff_member_required(login_url="/blog/home")
def group_create(request):
    ''' To create a group '''
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        form.instance.name = request.POST['group-name']

        # to check whether the posted name already exists
        group_names = list(Group.objects.values_list('name', flat=True))
        if request.POST['group-name'] in group_names:
            messages.error(request, 'Group Name already exists')
            return redirect('group_create')
        elif form.is_valid():
            form.save()
            return redirect('group_create')
            
    context = {
        'form': form,
        'groups': Group.objects.all(),
        'title': 'Create Group'
    }
    return render(request, 'group/group_create.html', context)

@staff_member_required(login_url="/blog/home")
def group_update(request, id):
    ''' To update a group details '''
    group = Group.objects.get(id=id)
    form = CreateGroupForm(instance=group)

    if request.method == 'POST':
        form = CreateGroupForm(request.POST, instance=group)
        form.instance.name = request.POST['group-name']
        if form.is_valid():
            form.save()
            return redirect('group_create')

    context={
        'form': form,
        'group': group,
        'title': 'Update Group'
    }
    return render(request, 'group/group_update.html', context)


@staff_member_required(login_url="/blog/home")
def group_delete(request):
    ''' To delete a group '''
    if request.method == 'POST' and request.user.is_superuser:
        group_id = request.POST['group-delete-id']
        group = Group.objects.get(id=group_id)
        group.delete()
        return redirect('group_create')
    return redirect('post', name='home')

@staff_member_required(login_url="/blog/home")
def add_user_group(request, name):
    ''' To add users to a group '''
    if request.method == 'POST':
        users = request.POST.getlist('user')
        for user in users:
            Group.objects.get(name=name).user.add(User.objects.get(id=user))

        return redirect('add_user_group', name)
    context = {
        'users': User.objects.all().exclude(is_superuser=True),
        'groups': Group.objects.all(),
        'group_users': Group.objects.get(name=name).user.all().exclude(is_superuser=True),
        'name': name,
        'title': 'Add User to a Group'
    }

    return render(request, 'group/add_user_group.html', context)

@staff_member_required(login_url="/blog/home")
def remove_user_group(request, name):
    ''' To remove users from a group '''
    if request.method == 'POST':
        
        user = request.POST['user']
        Group.objects.get(name=name).user.remove(int(user))
        return redirect('remove_user_group', name)
    context = {
        'groups': Group.objects.all(),
        'present_users': Group.objects.get(name=name).user.all(),
        'name': name,
        'title': 'Remove User from a Group'
    }

    return render(request, 'group/remove_user_group.html', context)

