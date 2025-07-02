from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, date

# models
from accounts.models import UserProfile, HairPhoto
from .models import HairAnalysis

# serializers
from .serializers import HairAnalysisSerializer, UserProfileHairDataSerializer


from django.utils import timezone

# AI module
from .ai import run_analyze_hair
from PIL import Image
import io



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_hair(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        return Response(
            {
                "Message": "User Profile Not Found."
            },
            status=400
        )
    
     # checking if the user has a valid subscription
    if user_profile.subsciption_expires_on and user_profile.subsciption_expires_on < timezone.now():
        return Response({"Message": "Your subscription has expired."}, status=403)
    
    
    user_analysis = HairAnalysis.objects.filter(user=user).order_by('-timestamp').first()
    if user_analysis:
        last_date = user_analysis.timestamp

        #checking if the user analyse less then seven days ago
        if last_date + timedelta(days=7) > timezone.now():
            return Response({"Message": "You have analyzed less than seven days ago."}, status=403)
  
    

    # grabbing the uploaded images
    flag = 0
    uploaded_images = {}
    hf = HairPhoto()
    if 'front' in request.FILES:
        hf.front = request.FILES['front']
        flag = 1
        uploaded_images['front'] = Image.open(request.FILES['front'])
    if 'back' in request.FILES:
        hf.back = request.FILES['back']
        flag = 1
        uploaded_images['back'] = Image.open(request.FILES['back'])
    if 'up_front' in request.FILES:
        hf.up_front = request.FILES['up_front']
        flag = 1
        uploaded_images['up_front'] = Image.open(request.FILES['up_front'])
    
    print(uploaded_images)
    # saving the reference in user profile
    if flag == 1:
        hf.save()
        user_profile.hair_photos.add(hf)
        user_profile.save()
    
    print(UserProfileHairDataSerializer(user_profile).data)
    # Calling ai
    data = run_analyze_hair(uploaded_images)


    # saving analysis report to db
    data['user'] = user.pk
    data['hair_photos'] = {
        "id": hf.pk,
        "front": hf.front.url if hf.front else None,
        "back": hf.back.url if hf.back else None,
        "up_front": hf.up_front.url if hf.up_front else None
    }
    serializer = HairAnalysisSerializer(data=data)
    if serializer.is_valid():
        if flag == 1:
            serializer.save()
        else:
            serializer.save()

    

    return Response(
        {
            "Data": serializer.data
        },
        status=200
    )



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_previous_analysis(request):
    user = request.user

    analysis_set = HairAnalysis.objects.filter(user=user)

    serializer = HairAnalysisSerializer(analysis_set, many=True)

    return Response(
        {
            "Data": serializer.data
        },
        status=200
    )


