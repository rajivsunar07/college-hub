from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    ''' For additional infomation of the user '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(default='default.jpg', upload_to='profile_pics')
    college_id = models.CharField(max_length=100, null=True, unique=True)
    user_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    class Meta:
        db_table = "Profile"

# Signal to create a profile object whenever a user object is created
def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
