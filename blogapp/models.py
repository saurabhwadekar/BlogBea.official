from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
import random 
import string
import time



     
from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone


def generate_random_string(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))






class Blog(models.Model):
    slug = models.SlugField(max_length=60, unique=True, null=True, blank=True)

    title = models.CharField(max_length=50)

    description = models.TextField()

    blog_image = models.ImageField(upload_to='blog_image/', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    custom_date = models.DateTimeField(null=True, blank=True)

    custom_choices = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            timestamp = str(int(time.time()))
            random_str = generate_random_string(6)

            complex_slug = f"{base_slug}-{timestamp}-{random_str}"

            while Blog.objects.filter(slug=complex_slug).exists():
                random_str = generate_random_string(6)
                complex_slug = f"{base_slug}-{timestamp}-{random_str}"

            self.slug = complex_slug

        super().save(*args, **kwargs)


    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        if self.user:
            name = self.user.get_full_name()
            if name:
                return f"{self.title} - {name}"
            return f"{self.title} - {self.user.username}"
        return self.title


    class Meta:
        db_table = "Blogs"
        ordering = ['-created_at']
        
        
        
# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    create_at = models.DateTimeField(default=timezone.now) 


    def __str__(self):
        return self.user.username

    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/img/default.jpg'  # Added a method to get the profile picture URL

        
 
 
        

    






#  for comment
class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class Savedblog(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{blog.title}"
    def __str__(self):
        return f"{self.user.username} saved {self.blog.title}"
    
    


    


        
        

        