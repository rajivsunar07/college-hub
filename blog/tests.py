from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import *
from blog.models import *
from blog.forms import *
from django.contrib.auth.models import User
from group.models import Group
from datetime import datetime, date


class TestUrls(TestCase):

    def test_post_url_resolves(self):
        url = reverse('post', args=['home'])
        self.assertEquals(resolve(url).func, post)

    def test_post_detail_url_resolves(self):
        url = reverse('post_detail', args=['home', '17'])
        self.assertEquals(resolve(url).func, post_detail)

    def test_post_create_url_resolves(self):
        url = reverse('post_create', args=['home', 'post'])
        self.assertEquals(resolve(url).func, post_create)

    def test_post_update_url_resolves(self):
        url = reverse('post_update', args=['home', 'post', '17'])
        self.assertEquals(resolve(url).func, post_update)

    def test_post_delete_url_resolves(self):
        url = reverse('post_delete', args=['home'])
        self.assertEquals(resolve(url).func, post_delete)
    
    def test_post_requests_url_resolves(self):
        url = reverse('post_requests')
        self.assertEquals(resolve(url).func, post_requests)
    
    def test_comment_create_url_resolves(self):
        url = reverse('comment_create', args=['17'])
        self.assertEquals(resolve(url).func, comment_create)
    
    def test_comment_update_url_resolves(self):
        url = reverse('comment_update')
        self.assertEquals(resolve(url).func, comment_update)

    def test_comment_delete_url_resolves(self):
        url = reverse('comment_delete')
        self.assertEquals(resolve(url).func, comment_delete)
    
    def test_post_option_url_resolves(self):
        url = reverse('post_option')
        self.assertEquals(resolve(url).func, post_option)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # to make the client a superuser
        self.user =  User(username='user', is_superuser=True)
        self.user.set_password('testpassword123') 
        self.user.save()
        self.client.login(username='user', password='testpassword123')

        # test group and post
        self.group = Group.objects.create(name='26A', group_type='class')
        self.post = Post.objects.create(content='Default Post', group=self.group, author=self.user)
        
        # urls
        self.post_url = reverse('post', args=['26A'])
        self.post_create_url = reverse('post_create', args=['26A', 'post'])
        self.post_detail_url = reverse('post_detail', args=['26A', self.post.id])
        self.post_update_url = reverse('post_update', args=['26A', 'post', self.post.id,])
        self.post_delete_url = reverse('post_delete', args=['26A'])

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        self.post.delete()

    def test_post_GET(self):
        response = self.client.get(self.post_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post_detail_GET(self):
        response = self.client.get(self.post_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_create_POST(self):
        response = self.client.post(self.post_create_url, {
            'content': 'Test post',
            'author': self.user
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.all().count(), 2)
   
    def test_post_create_POST_no_data(self):
        response = self.client.post(self.post_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Post.objects.all().count(), 1) # only 1 default post is present

    def test_post_update_POST(self):
        response = self.client.post(self.post_update_url, {
            'content':'Changed content',
        })
        
        self.assertEquals(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEquals(self.post.content, 'Changed content')
    
    def test_post_delete_POST(self):
        response = self.client.post(self.post_delete_url, {
            'post-delete-id': self.post.id 
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Post.objects.all().count(), 0)

    def test_comment_create(self):
        response = self.client.post(reverse('comment_create', args=[self.post.id]), {
            'content': 'Test comment'
            # 'author': self.user
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Comments.objects.all().first().content, 'Test comment')

    def test_comment_update(self):
        comment = Comments.objects.create(
            content= 'Test comment1',
            author= self.user,
            post= self.post
        )

        response = self.client.post(reverse('comment_update'),  {
            'comment-update-id': comment.id,
            'comment-update-content': 'Changed comment'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Comments.objects.all().first().content, 'Changed comment')

    def test_comment_delete(self):
        comment = Comments.objects.create(
            content= 'Test comment1',
            author= self.user,
            post= self.post
        )

        response = self.client.post(reverse('comment_delete'),  {
            'comment-delete-id': comment.id,
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Comments.objects.all().count(), 0)

   

class TestModels(TestCase):

    def setUp(self):

        # a test user
        self.user =  User(username='user', is_superuser=True)
        self.user.set_password('testpassword123') 
        self.user.save()

        # a test group
        self.group = Group.objects.create(name='26A', group_type='class')

        self.post = Post.objects.create(content='Test Content', group=self.group, author=self.user)
    
    def test_post_verification_date_posted_type_added(self):
        self.assertEquals(self.post.verification, 'accepted')


class TestForms(TestCase):
    def setUp(self):
         # a test user
        self.user =  User(username='user', is_superuser=True)
        self.user.set_password('testpassword123') 
        self.user.save()

        # a test group
        self.group = Group.objects.create(name='26A', group_type='class')
        self.post = Post.objects.create(content='Test Content', group=self.group, author=self.user)
    
    def test_PostForm_is_valid(self):
        form = PostForm(data={
            'content': 'Test Content',
            'author': self.user,
            'group': self.group
        })

        self.assertTrue(form.is_valid())
    
    def test_PostForm_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())