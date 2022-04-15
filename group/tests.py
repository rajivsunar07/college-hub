from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import *
from .views import *
from .forms import *
from django.contrib.auth.models import User

# Create your tests here.
class TestUrls(TestCase):

    def test_group_create_url_resolves(self):
        url = reverse('group_create')
        self.assertEquals(resolve(url).func, group_create)
    
    def test_group_update_url_resolves(self):
        url = reverse('group_update', args=['2'])
        self.assertEquals(resolve(url).func, group_update)

    def test_group_delete_url_resolves(self):
        url = reverse('group_delete')
        self.assertEquals(resolve(url).func, group_delete)

    def test_add_user_group_url_resolves(self):
        url = reverse('add_user_group', args=['26A'])
        self.assertEquals(resolve(url).func, add_user_group)
    
    def test_remove_user_group_url_resolves(self):
        url = reverse('remove_user_group', args=['26A'])
        self.assertEquals(resolve(url).func, remove_user_group)
  

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # to make the client a superuser
        self.user =  User(username='user', is_superuser=True, is_staff=True)
        self.user.set_password('testpassword123') 
        self.user.save()
        self.client.login(username='user', password='testpassword123')

        # test group and post
        self.group = Group.objects.create(name='26A', group_type='class')
        
        # urls
        self.group_create_url = reverse('group_create')
        self.group_update_url = reverse('group_update', args=[self.group.id])
        self.group_delete_url = reverse('group_delete')
        self.add_user_group_url = reverse('add_user_group', args=['26A'])
        self.remove_user_group_url = reverse('remove_user_group', args=['26A'])

    def tearDown(self):
        self.user.delete()
        self.group.delete()

    def test_group_create_GET(self):
        response = self.client.get(self.group_create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'group/group_create.html')

    def test_group_create_POST(self):
        response = self.client.post(self.group_create_url, {
            'group-name': '26B',
            'group_type': 'class'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Group.objects.all().count(), 2)
    
   
    def test_post_create_POST_no_data(self):
        response = self.client.post(self.group_create_url, {
            'group-name' : ''
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(Group.objects.all().count(), 1) # only 1 default group is present

    def test_group_update_GET(self):
      
        response = self.client.post(self.group_update_url, {
            'group-name': '26C',
            'group_type': self.group.group_type
        })
        self.assertEquals(response.status_code, 302)
        self.group.refresh_from_db()
        
        self.assertEquals(self.group.name, '26C')
    
    def test_group_delete_POST(self):
        test_group = Group.objects.create(name='test', group_type='test')

        response = self.client.post(self.group_delete_url, {
            'group-delete-id': test_group.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Group.objects.all().count(), 1)

    def test_add_user_group_POST(self):
        test_user = User.objects.create(username='test')
        test_user.password = 'testpassword'

        response  = self.client.post(self.add_user_group_url, {
            'user': test_user.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            self.group.user.all().first().username,
            test_user.username
        )
    
    def test_remove_user_group_POST(self):
        test_user = User.objects.create(username='test')
        test_user.password = 'testpassword'

        response = self.client.post(self.remove_user_group_url, {
            'user': test_user.id
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.group.user.all().count(),0)

class TestModels(TestCase):

    def test_post_verification_date_posted_type_added(self):
        self.group = Group.objects.create(name='26A', group_type='class')
        test_user = User.objects.create(username='test')
        test_user.password = 'testpassword'

        self.group.user.add(test_user)
        self.assertEquals(self.group.user.first().username, 'test')


class TestForms(TestCase):
        

    def test_CreateGroupForm_is_valid(self):
        form = CreateGroupForm(data={
            'name': 'Test',
            'group_type': 'Test Type'
        })

        self.assertTrue(form.is_valid())
    
    def test_PostForm_no_data(self):
        form = CreateGroupForm(data={})

        self.assertFalse(form.is_valid())