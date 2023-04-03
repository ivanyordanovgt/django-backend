import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
import rest_framework.exceptions as ex
from user_auth.models import User, Video
from user_auth.serializers import UserSerializer, VideoSerializer
import jwt, datetime
from django.core.serializers import serialize

def checkCookie(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        return jwt.decode(token, 'secret', algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class loginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        errors = {}
        if user is None:
            raise AuthenticationFailed('No users registered with that email!')
        elif not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        payload = checkCookie(request)
        userId = payload['id']
        user = User.objects.filter(id=userId).first()
        serializer = UserSerializer(user)
        return Response({
            'data': serializer.data
        })

    def put(self, request):
        payload = checkCookie(request)
        userId = payload['id']
        data = request.data
        user = User.objects.filter(id=userId).first()

        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        raise ValidationError

    def post(self, request):
        payload = checkCookie(request)
        if 'id' in request.data.keys():
            userId = request.data['id']
        else:
            return Response({'error': 'not found',
                             'data': 'empty'})
        user = User.objects.filter(id=userId).first()
        if (not user):
            return Response({'error': 'not found'})
        serializer = UserSerializer(user)
        return Response({'data': serializer.data,
                         'error': False
                         })

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response
    
class VideoView(APIView):

    def put(self, request):
        payload = checkCookie(request)
        userId = payload['id']
        data = request.data
        print(request.data['videoId'])
        videoId = request.data['videoId']
        video = Video.objects.filter(videoId=videoId)
        print(data)

        if not video:
            raise ValidationError('No video found!')
        video = video[0]
        if video.user.id != userId:
            raise ValidationError('You are not allowed to edit this video!')
        if data['user'] != userId:
            raise ValidationError('You are not authorized to change ownership of this video!')
        serializer = VideoSerializer(instance=video, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        raise ValidationError

    def post(self, request):

        if 'title' in request.data.keys():
            payload = checkCookie(request)
            request.data['user'] = payload['id']
            serializer = VideoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
        videoId = request.data['videoId']
        video = Video.objects.filter(videoId=videoId).first()
        serializer = VideoSerializer(video)
        return Response({
            'data': serializer.data
        })
    
    def get(self, request):
        payload = checkCookie(request)
        userId = payload['id']
        user = User.objects.filter(id=userId).first()
        videos = Video.objects.filter(user=user)
        print(videos, "!!!!!!")
        videoList = []

        for video in videos:
            serializer = VideoSerializer(video)
            videoList.append(serializer.data)
        
        return Response({
            'data': videoList
        })
