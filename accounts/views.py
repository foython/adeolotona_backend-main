from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile, HairPhoto
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer
from django.core.mail import EmailMessage





@api_view(['POST'])
def normal_register(request):
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if email is None or password is None:
        return Response(
            {
                "Message": "Both Email and Passwords are required."
            },
            status=400
        )

    if User.objects.filter(username=email).count() > 0:
        return Response(
            {
                "Message": "The email is already used by another user."
            },
            status=400
        )
    
    user = User()
    user.username = email
    user.email = email
    user.set_password(password)
    user.save()

    user_profile = UserProfile()
    user_profile.user = user
    user_profile.save()

    otp = user_profile.generate_otp()

    subject = 'Here is your verification code'
    message = f'Hello, please verify your account with the OTP: {otp}'
    from_email = 'support@gameplanai.co.uk'
    recipient_list = [email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()


    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token


    return Response(
        {
            'refresh': str(refresh),
            'access': str(access_token),
            'profile_data': UserProfileSerializer(user_profile).data,
            'message': 'Signed Up Successfully.'
        }, 
        status=201
    )


@api_view(['POST'])
def normal_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"Message": "Both Username and password are required."}, status=400)
    
    user = authenticate(username=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'user_profile': UserProfileSerializer(UserProfile.objects.get(user=user)).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({"Message": "Invalid credentials."}, status=401)
    


@api_view(['POST'])
def verify_otp(request):
    otp = request.data.get('otp')
    email = request.data.get('email')

    try:
        user = User.objects.get(username=email)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.otp == otp:
            user_profile.is_verified = True
            user_profile.save()
            return Response(
                {
                    "Message": "Successfully verified your OTP."
                },
                status=200
            )
        else:
            return Response(
                {
                    "Message": "Invalid OTP, please try again."
                },
                status=400
            )
    except Exception as e:
        print(e)
        return Response(
            {
                "Message": "No account found with that email address."
            },
            status=400
        )
    

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'GET':
        return Response(
            {
                "data": UserProfileSerializer(user_profile).data
            },
            status=200
        )
    elif request.method == 'PATCH':
        flag = 0
        hf = HairPhoto()
        if 'front' in request.FILES:
            hf.front = request.FILES['front']
            flag = 1
        if 'back' in request.FILES:
            hf.back = request.FILES['back']
            flag = 1
        if 'up_front' in request.FILES:
            hf.up_front = request.FILES['up_front']
            flag = 1
        
        if flag == 1:
            hf.save()
            user_profile.hair_photos.add(hf)
            user_profile.save()
        
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "Message": "Successfully updated user profile."
                },
                status=200
            )
        else:
            return Response(
                {
                    "Message": str(serializer.errors)
                },
                status=400
            )


@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(username=email)
        user_profile = UserProfile.objects.get(user=user)

        otp = user_profile.generate_otp()
        subject = 'Here is your verification code'
        message = f'Hello, you have requested an OTP for verification, her is your otp: {otp}'
        from_email = 'pialzoad@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

        return Response(
            {
                "Message": "Successfully Resent OTP."
            },
            status=200
        )

    except:
        return Response(
            {
                "Message": "No account found with the given email address"
            },
            status=400
        )


@api_view(['POST'])
def change_password(request):
    otp = request.data.get('otp')
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=email)
        user.set_password(password)
        user.save()

        return Response(
            {
                "Message": "Successfully Changed your password."
            },
            status=200
        )

    except:
        return Response(
            {
                "Message": "No account found with the given email address"
            },
            status=400
        )


@api_view(['POST'])
def social_login_register(request):
    email = request.data.get('email')

    if User.objects.filter(username=email).count() == 0:
        user = User()
        user.username = email
        user.email = email
        user.save()

        user_profile = UserProfile()
        user_profile.user = user
        user_profile.is_verified = True
        user_profile.auth_provider = "social"
        user_profile.save()
    else:
        user = User.objects.filter(username=email)[0]
        user_profile = UserProfile.objects.get(user=user)

        if user_profile.auth_provider == "normal":
            return Response(
                {
                    "Message": "Please use email/password based login!"
                },
                status=400
            )


    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    return Response({
        'refresh': str(refresh),
        'access': str(access_token),
        'user_profile': UserProfileSerializer(UserProfile.objects.get(user=user)).data
    }, status=status.HTTP_200_OK)