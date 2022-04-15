from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from .models import Post, Comments, PostOption, ClickedPost
from group.models import Group
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
# Create your views here.

def get_clicked_post_options(request):
    ''' 
    To get all posts and their options clicked by the request user
    '''
    clicked_options = ClickedPost.objects.filter(user=request.user)
    user_clicked_posts = []
    user_clicked_options = []
    for clicked_option in clicked_options:
        user_clicked_posts.append(clicked_option.option.post)
        user_clicked_options.append(clicked_option.option)

    return user_clicked_posts, user_clicked_options 

@login_required
def post(request, name):
    ''' To view all posts in a group '''
    # for first time login, creates a home page
    if Group.objects.all().count() == 0:
        Group.objects.create(name='home', group_type='home')
    
    current_group = Group.objects.get(name=name)

    #checks if the user belongs to the group
    if request.user in current_group.user.all() or request.user.is_superuser:
        groups = Group.objects.filter(user=request.user)
        posts  = Post.objects.filter(group=current_group)
        postOptions = PostOption.objects.all()

        # for pagination
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        comments = Comments.objects.all()

        user_clicked_posts, user_clicked_options = get_clicked_post_options(request)

        context = {
            'posts': posts,
            'name': name,
            'groups': groups,
            'comments': comments,
            'user_clicked_posts': user_clicked_posts,
            'user_clicked_options': user_clicked_options,
            'postOptions' : postOptions,
            'title': name.upper()
        }
        return render(request, 'blog/post.html', context)
    return redirect('post', 'home')

@login_required
def post_detail(request, name, pk):
    ''' To view a post in detail '''
    current_group = Group.objects.get(name=name)
    comment_form = CommentForm()

    if request.user in current_group.user.all() or request.user.is_superuser:
        post  = Post.objects.get(id=pk)
        comments = Comments.objects.filter(post=post)
        postOptions = PostOption.objects.filter(post=post)

        user_clicked_posts, user_clicked_options = get_clicked_post_options(request)
        
        context = {
            'post': post,
            'name': name,
            'pk':pk,
            'comments': comments,
            'user_clicked_posts': user_clicked_posts,
            'user_clicked_options': user_clicked_options,
            'comment_form': comment_form,
            'postOptions': postOptions,
            'title': name.upper(),
            'groups': Group.objects.filter(user=request.user)
        }

        
        return render(request, 'blog/post_detail.html', context)
    return redirect('post', name='home')


@login_required
def post_create(request, name, post_type):
    ''' To create a post in a group '''
    if (request.user in Group.objects.get(name=name).user.all()) or request.user.is_superuser:
        form = PostForm()
        
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            form.instance.image = None

            if form.is_valid():
                form.instance.author = request.user
                form.instance.group_id = Group.objects.filter(name=name).first().id
                form.instance.type = post_type

                # checks if the post is created in home page
                # if created in home page, then send to admin for verification
                if request.user.is_superuser:
                    form.instance.verification = 'accepted'
                elif name == 'home':
                    form.instance.verification = 'pending'
                form.save()

                #checks what type of post is created
                if post_type == 'poll':
                    # Gets all the option if it is a poll
                    options = request.POST.getlist('option')
                    for option in options:
                        if option != '':
                            optionObject = PostOption.objects.create(option=option,post=form.instance)
                            optionObject.save()
                elif post_type == 'invite':
                    optionObject1 = PostOption.objects.create(option='Yes',post=form.instance)
                    optionObject2 = PostOption.objects.create(option='No',post=form.instance)
                    optionObject1.save()
                    optionObject2.save() 
                return redirect('post', name=name)

        context = {
            'form': form,
            'name': name,
            'type': post_type,
            'title': name.upper() + " - Create Post",
            'groups': Group.objects.filter(user=request.user)
        }
        return render(request, 'blog/post_create.html', context)
    return redirect('post', name='home')


@login_required
def post_update(request, name, post_type, pk):
    ''' To update a post '''
    post = Post.objects.get(id=pk)
    if post.author == request.user: 
        options = PostOption.objects.filter(post=post)
        form = PostForm(instance=post)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                if post_type == 'poll' or post_type == 'invite':
                    for option in options:
                        option_change = request.POST[str(option.id)]
                        optionObject = PostOption.objects.get(id=option.id)
                        optionObject.option = option_change
                        optionObject.save()
                return redirect('post_detail', name=name, pk=pk)
        context = {
            'form': form,
            'options': options,
            'type': post_type,
            'title': name.upper() + " - Update Post",
            'groups': Group.objects.filter(user=request.user)
        }
        return render(request, 'blog/post_update.html', context)
    return redirect('post', name='home')


@login_required
def post_delete(request, name):
    ''' To delete a post '''
    if request.method == "POST":
        post_id = request.POST['post-delete-id']
        post = Post.objects.get(id=post_id)
        if post.author == request.user or request.user.is_superuser: 
            post.delete()
            return redirect('post', name=name)
    return redirect('post', name='home')


# comments
@login_required
def comment_create(request, pk):
    ''' To create a comment for a post '''
    if request.method == "POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comment.instance.author = request.user
            comment.instance.post = Post.objects.get(id=pk)
            comment.save()
    return redirect('post_detail', name=Post.objects.get(id=pk).group.name, pk=pk )



@login_required
def comment_update(request):
    ''' To update a comment ''' 
    if request.method == "POST":
        comment_id = request.POST.get('comment-update-id')
        comment_content = request.POST.get('comment-update-content')
        
        comment = Comments.objects.get(id=comment_id)
        if comment.author == request.user: 
            comment.content = comment_content
            comment.save()
            return redirect('post_detail', name=comment.post.group.name, pk=comment.post.id)
    return redirect('post', name='home')

@login_required
def comment_delete(request):
    ''' To delete a comment '''
    if request.method == "POST":
        comment_id = request.POST['comment-delete-id']
        comment = Comments.objects.get(id=comment_id)
        name = comment.post.group.name
        pk = comment.post.id
        if comment.author == request.user: 
            comment.delete()
            return redirect('post_detail', name=name, pk=pk)
    return redirect('post', name='home')

@staff_member_required(login_url="/blog/home")
def post_requests(request):
    ''' To view requested posts for the home page '''
    posts = Post.objects.filter(verification='pending')
    postOptions = PostOption.objects.all()
    if request.method == 'POST':
        post_id = request.POST['post-id']
        post = Post.objects.get(id=post_id)
        if 'accept' in request.POST:
            post.verification = 'accepted'
            post.save()
        elif 'decline' in request.POST:
            post.verification = 'declined'
            post.save()
        return redirect('post_requests')
    context = {
        'posts': posts,
        'title': 'Post Requests',
        'postOptions': postOptions,
        'groups': Group.objects.filter(user=request.user)
    }
    return render(request, 'blog/post_requests.html', context)

def post_option(request):
    ''' To handle ajax requests, when options in a post is clicked '''
    if request.is_ajax and request.method == "POST":
        if 'option' in request.POST:
            #change the clicked value of the option
            option = PostOption.objects.get(id=request.POST.get('option'))
            option.clicked_value = option.clicked_value + 1
            option.save()

            #create a relation between the clicked option and the request user
            clicked_post = ClickedPost.objects.create(option=option, user=request.user)
            clicked_post.save()
            
            # change the clicked percentage
            options = PostOption.objects.filter(post=option.post)
            total_clicked_value = 0
            for current_option in options:
                total_clicked_value += current_option.clicked_value
            for current_option in options:
                current_option.clicked_percent = (current_option.clicked_value/total_clicked_value)*100
                current_option.save()
            
            clicked_options = ClickedPost.objects.filter(user=request.user)
            user_clicked_posts = []
            user_clicked_options = []
            for clicked_option in clicked_options:
                user_clicked_posts.append(clicked_option.option.post)
                user_clicked_options.append(clicked_option.option)
            
            post  = Post.objects.get(id=request.POST.get('pk'))
            postOptions = PostOption.objects.filter(post=post)
            
            context = {
                'post': post,
                'user_clicked_posts': user_clicked_posts,
                'user_clicked_options': user_clicked_options,
                'postOptions': postOptions,
            }

            html = render_to_string('blog/post_option.html', context, request=request)
            return JsonResponse({'form':html, 'pk':str(post.id)}, status=200)
    return JsonResponse({"error": ""}, status=400)
            

                

            