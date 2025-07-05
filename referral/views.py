from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from .models import Referral
from django.core.mail import EmailMessage

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def referralView(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        return Response({"Message": "User Profile Not Found."}, status=400)
    
    email = request.data.get('email')
    atb = Referral.objects.create(referred_by=user_profile)
    


    try:        
        
        subject = 'Here is your referral code'
        message = f'Hello, you got a referral code for Hair Analysis app, here is your code: {atb.referral_code}'
        from_email = 'pialzoad@gmail.com'
        recipient_list = [email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

        return Response(
            {
                "Message": "Successfully Sent Referral Code."
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