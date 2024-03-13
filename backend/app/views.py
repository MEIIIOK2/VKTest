from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from.serializers import RegisterSerializer, LoginSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from .tasks import send_activation_email
from .models import CustomUser, Image
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
import base64
from .tokens import activation_token


from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

# Create your views here.
import os



@api_view(['GET'])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def get_csrf(request):
    return Response({'success':'CSRF Cookie Set'})


def urlinfo(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk = uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        return render(request,'link_activated.html')
    return HttpResponse('link expired')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user =  serializer.save()
        user.set_password(request.data['password'])
        user.save()
        encoded_uid = urlsafe_base64_encode(force_bytes(user.pk))
        encoded_uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = activation_token.make_token(user)
        url = f'https://mlgarden.dev/api/verify/{encoded_uid}/{token}'
        send_activation_email.delay(url,user.email)
        return(Response('Registration sucessfull'))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def user_login(request):    
    serializer = LoginSerializer(data= request.data)
    
    if serializer.is_valid():
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                print(type(request))
                login(request,user)
                return Response({'detail':'Logged in successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Email or Password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_protect
def user_logout(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_image(request):

    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        file = request.FILES.get('file')
        if file.size > 3 * 1024 * 1024: 
            return Response({"error": "File too large. Max size - 3MB"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        try:
            user = CustomUser.objects.get(pk=request.user.id)
        except:
            return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            image = Image.objects.get(owner = user.id)
            image.file = serializer.validated_data.get('file')
            image.save()
            return Response(status.HTTP_200_OK)
        except:
            serializer.save(owner=user)
            return Response(status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image(request):

    print('authorized')
    user = CustomUser.objects.get(pk=request.user.id)
    image = Image.objects.filter(owner=user.id).first()
    print(image)
    if image is None:
        with open(settings.MEDIA_ROOT + '/images/'+'missing.jpg', 'rb') as image_file:
            return HttpResponse(base64.b64encode(image_file.read()))
    path = str(image.file)
    print(path)
    full_path = settings.MEDIA_ROOT +'/' +path
    if os.path.exists(full_path):
            with open(full_path, 'rb') as image_file:
                return HttpResponse(base64.b64encode(image_file.read()))
    with open(settings.MEDIA_ROOT + '/images/'+'missing.jpg', 'rb') as image_file:
            return HttpResponse(base64.b64encode(image_file.read()))