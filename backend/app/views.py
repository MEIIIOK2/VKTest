from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from.serializers import RegisterSerializer, LoginSerializer, ImageSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .tasks import send_activation_email
from .models import CustomUser, Image
from rest_framework import status
import base64
from .tokens import activation_token


from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from django.contrib.auth import authenticate
# Create your views here.
import os




def urlinfo(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk = uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return(redirect('/'))
    return HttpResponse('link expired')



@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user =  serializer.save()
        user.set_password(request.data['password'])
        user.save()
        encoded_uid = urlsafe_base64_encode(force_bytes(user.pk))
        encoded_uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = activation_token.make_token(user)
        url = f'http://127.0.0.1/api/verify/{encoded_uid}/{token}'
        send_activation_email.delay(url,user.email)
        return(Response('Registration sucessfull'))
    return Response(serializer.errors)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data= request.data)
    
    print(serializer.is_valid())
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email = email, password = password)
        if user is None:
            return Response('incorrect email or password', status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh':str(refresh), 'token':str(refresh.access_token)})
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):

    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        print('valid')
        file = request.FILES.get('file')
        if file.size > 3 * 1024 * 1024: 
            print('size mismatch') 
            return Response({"error": "File too large. Max size - 3MB"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        try:
            user = CustomUser.objects.get(pk=request.user.id)
            print('owner found') 
        except:
            return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            print('updating') 
            image = Image.objects.get(owner = user.id)
            image.file = serializer.validated_data.get('file')
            image.save()
            return Response(status.HTTP_200_OK)
        except:
            print('save as new') 
            serializer.save(owner=user)
            return Response(status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image(request):
    user = CustomUser.objects.get(pk=request.user.id)
    image = Image.objects.filter(owner=user.id).first()
    if image is None:
        with open(settings.MEDIA_ROOT + '/images/'+'missing.jpg', 'rb') as image_file:
            return HttpResponse(base64.b64encode(image_file.read()))
    path = str(image.file)
    full_path = settings.MEDIA_ROOT +'/' +path
    if os.path.exists(full_path):
            with open(full_path, 'rb') as image_file:
                return HttpResponse(base64.b64encode(image_file.read()))
    return Response('Internal error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)