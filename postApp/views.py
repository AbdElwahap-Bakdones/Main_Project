from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, PostImageSerializer, PostSerializer,insertImage,getImage
from .models import User, Post ,PostImage
import jwt
import json


def encoder_token(id: int, email: str) -> str:
    
    return jwt.encode({'id': id, 'email': email}, 'Abd', algorithm='HS256')


def check_token(token: str) -> map:
    try:
        m = jwt.decode(token, 'Abd', algorithms=['HS256'])
        id = m['id']
        email = m['email']
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            return {'state': True, 'id': id, 'email': email, 'user_obj': user_obj}
        raise Exception('Invalid token')
    except Exception as e:
        print('Error checkToken functions')
        print(e)
        return {'state': False}


def validationEmptyValue( data: map) -> bool:
    try:
        return bool(sum(list(map(lambda item: True if data[item] == None else False, data))))
    except Exception as e:
        print(e)
        return False



class SignUp(APIView):
    def get(self, request):
        return Response(UserSerializer(User.objects.all(),  many=True).data, status=status.HTTP_200_OK)
    def post(self, request):
        print(request.data)
        addUser = UserSerializer(data=request.data)
        addUser.is_valid(raise_exception=True)
        addUser.save()
        return Response(addUser.data, status=status.HTTP_201_CREATED)


class posts(APIView):
    def get(self,request, pk):
        try:
            #data = request.data
            #token = check_token(data['token'])
            posts = Post.objects.filter(
                user=pk, deleted=False, id=pk)
            return Response(PostSerializer(posts, many=True).data, status=status.HTTP_200_OK)
        except e:
            return Response({'message': 'npt found'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request,pk):
        try:
            data=request.data
            token=check_token(data['token'])
            user=User.objects.filter(pk=token['id']).get()
            add_post=Post(content=data['content'],
                    title=data['title'], user=user)
            add_post.save()
            indexImge=0
            for i in data['images']:
                path = insertImage(str(add_post.pk)+'_'+str(indexImge), i, 'post')
                PostImage(post=add_post,image=path).save()
                indexImge+=1
            return Response(PostSerializer(add_post).data,status=status.HTTP_201_CREATED)
        except e:
            return Response({'message': 'some thing wrong'}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        #check_token(request.DELETE['token'])
        try:
            Post.objects.filter(pk=pk).update(deleted=True)
            return Response({'message':'post has deleted'},status=status.HTTP_200_OK)
        except e:
            return Response({'message':'the id not found'},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:
            data = request.data
            token = check_token(data['token'])
            pust_update=Post.objects.filter(pk=pk).update(content=data['content'],title=data['title'])
            indexImge = 0
            print('000000000')
            if data['image_updated']:
                PostImage.objects.filter(post=pk).delete()
                for i in data['images']:
                    print(i)
                    print('3123131')
                    path = insertImage(str(pk)+'_'+str(indexImge), i, 'post')
                    PostImage(post=Post.objects.get(pk=pk), image=path).save()
                    indexImge+=1
            return Response({'message':'updated'},status=status.HTTP_200_OK)
        except e:
            return Response({'message': 'the id not found'},status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getAllPost(request,pk,index):
    try:
        #data = request.data
        #token = check_token(data['token'])
        posts=Post.objects.filter(
            user=pk,deleted=False, id__gte=index)[:10]
        print(posts)
        return Response(PostSerializer(posts, many=True).data, status=status.HTTP_200_OK)
    except e:
        return Response({'message': 'some things wrong'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        user=User.objects.filter(email=request.data['email'])
        if user.exists():
            print('dasasd')
            return Response({'token':encoder_token(user.get().pk, user.get().email)},status=status.HTTP_200_OK)
        return Response({'message':'email not found'},status=status.HTTP_401_UNAUTHORIZED)
    except e:
        return Response({'message': 'some things wrong'}, status=status.HTTP_400_BAD_REQUEST)
######