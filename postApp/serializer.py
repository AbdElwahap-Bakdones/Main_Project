from rest_framework import serializers
from .models import PostImage, User, Post
import json


def getImage(path: str) -> str:
    try:
        print('getImage function')
        f = open(path, 'r')
        return f.read()
    except Exception as e:
        print('Error in getImage function')
        print(e)
        return ''


def insertImage(id: int, image: str, type: str) -> str:
    try:
        print('in insert image')
        print(id)
        path = 'static/'+'image/'+type+'/'+str(id)+'.txt'
        f = open(path, 'w')
        f.write(str(image))
        return path
    except Exception as e:
        print('Error in insertImage function')
        print(e)
        return 'static/image/user/userImage.txt'


class UserSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=55)
    last_name = serializers.CharField(max_length=55)
    email = serializers.CharField(max_length=150, required=True)
    image = serializers.SerializerMethodField(method_name='get_image')

    def get_image(self, id):
        print(id.image)
        return getImage(str(id.image))

    def validate_email(self, attrs):

        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError('email already exists!')

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        user.image = insertImage(user.id, user.image, 'user')
        user.save()
        return user


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    deleted = serializers.BooleanField()
    date = serializers.DateTimeField()
    images = serializers.SerializerMethodField(method_name='get_images')

    def get_images(self, id):
        image_objects = PostImage.objects.filter(post=id.pk)
        return PostImageSerializer(image_objects, many=True).data

    def create(self, validated_data):
        post = Post(**validated_data)
        Post.save()
        return post


class PostImageSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(method_name='get_image')

    def get_image(self, id):
        return getImage(str(id.image))

    def create(self, validated_data):
        post = PostImage(**validated_data)
        Post.save()
        return post
