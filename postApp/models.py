from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=150, unique=True)
    #number = models.IntegerField(max_lengt)
    image = models.ImageField(
        upload_to='static/image/user', default='static/image/user/userImage.txt')

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class PostImage(models.Model):
    image = models.ImageField(upload_to='static/image/post')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post)
