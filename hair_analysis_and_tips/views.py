from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta

from accounts.models import UserProfile, HairPhoto

from .ai import run_analyze_hair

from django.utils import timezone
from PIL import Image
from .models import HairPhoto, HairType, Characteristics, HairCondition, AnalysisReport, HairTip, RoutineStep, HairRoutine, HairAnalysis
from .serializers import HairAnalysisSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_hair(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except:
        return Response({"Message": "User Profile Not Found."}, status=400)

    if user_profile.subsciption_expires_on and user_profile.subsciption_expires_on < timezone.now():
        return Response({"Message": "Your subscription has expired."}, status=403)

    # user_analysis = HairAnalysis.objects.filter(user=user).order_by('-created_at').first()
    # if user_analysis and user_analysis.created_at + timedelta(days=7) > timezone.now():
    #     return Response({"Message": "You have analyzed less than seven days ago."}, status=403)

    flag = 0
    uploaded_images = {}
    hf = HairPhoto()
    if 'front' in request.FILES:
        hf.front = request.FILES['front']
        uploaded_images['front'] = Image.open(request.FILES['front'])
        flag = 1
    if 'back' in request.FILES:
        hf.back = request.FILES['back']
        uploaded_images['back'] = Image.open(request.FILES['back'])
        flag = 1
    if 'up_front' in request.FILES:
        hf.up_front = request.FILES['up_front']
        uploaded_images['up_front'] = Image.open(request.FILES['up_front'])
        flag = 1

    if flag:
        hf.save()
        user_profile.hair_photos.add(hf)
        user_profile.save()

    data = run_analyze_hair(uploaded_images)
    print(data)

    # Save submodels
    ht = HairType.objects.create(**data['analysis_report']['hair_type'])
    ch = Characteristics.objects.create(**data['analysis_report']['characteristics'])

    conditions_objs = []
    for cname, cvalue in data['analysis_report']['conditions'].items():
        condition = HairCondition.objects.create(name=cname, level=cvalue['level'], insight=cvalue['insight'])
        conditions_objs.append(condition)

    report = AnalysisReport.objects.create(hair_type=ht, characteristics=ch, health_score=data['analysis_report']['health_score'])
    report.conditions.set(conditions_objs)
    report.save()

    tips_objs = [HairTip.objects.create(content=tip) for tip in data['tips']]

    washday_steps = [RoutineStep.objects.create(**step) for step in data['routine']['washday']]
    routine = HairRoutine.objects.create(
        daily_routine=data['routine']['daily_routine'],
        monthly_routine=data['routine']['monthly_routine']
    )
    routine.washday_steps.set(washday_steps)
    routine.save()

    analysis = HairAnalysis.objects.create(
        user=user,
        analysis_report=report,
        routine=routine,
        hair_photos=hf
    )
    analysis.tips.set(tips_objs)
    analysis.save()

    serialized = HairAnalysisSerializer(analysis)
    return Response({"Data": serialized.data}, status=200)




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def analyze_hair(request):
#     user = request.user
#     try:
#         user_profile = UserProfile.objects.get(user=user)
#     except:
#         return Response(
#             {
#                 "Message": "User Profile Not Found."
#             },
#             status=400
#         )
    
#      # checking if the user has a valid subscription
#     if user_profile.subsciption_expires_on and user_profile.subsciption_expires_on < timezone.now():
#         return Response({"Message": "Your subscription has expired."}, status=403)
    
    
#     user_analysis = HairAnalysis.objects.filter(user=user).order_by('-timestamp').first()
#     if user_analysis:
#         last_date = user_analysis.timestamp

#         #checking if the user analyse less then seven days ago
#         if last_date + timedelta(days=7) > timezone.now():
#             return Response({"Message": "You have analyzed less than seven days ago."}, status=403)
  
    

#     # grabbing the uploaded images
#     flag = 0
#     uploaded_images = {}
#     hf = HairPhoto()
#     if 'front' in request.FILES:
#         hf.front = request.FILES['front']
#         flag = 1
#         uploaded_images['front'] = Image.open(request.FILES['front'])
#     if 'back' in request.FILES:
#         hf.back = request.FILES['back']
#         flag = 1
#         uploaded_images['back'] = Image.open(request.FILES['back'])
#     if 'up_front' in request.FILES:
#         hf.up_front = request.FILES['up_front']
#         flag = 1
#         uploaded_images['up_front'] = Image.open(request.FILES['up_front'])
    
#     print(uploaded_images)
#     # saving the reference in user profile
#     if flag == 1:
#         hf.save()
#         user_profile.hair_photos.add(hf)
#         user_profile.save()
    
#     print(UserProfileHairDataSerializer(user_profile).data)
#     # Calling ai
#     data = run_analyze_hair(uploaded_images)


#     # saving analysis report to db
#     data['user'] = user.pk
#     data['hair_photos'] = {
#         "id": hf.pk,
#         "front": hf.front.url if hf.front else None,
#         "back": hf.back.url if hf.back else None,
#         "up_front": hf.up_front.url if hf.up_front else None
#     }
#     serializer = HairAnalysisSerializer(data=data)
#     if serializer.is_valid():
#         if flag == 1:
#             serializer.save()
#         else:
#             serializer.save()

    

#     return Response(
#         {
#             "Data": serializer.data
#         },
#         status=200
#     )



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_previous_analysis(request, id=None):
    user = request.user
    if id:
        analysis_set = HairAnalysis.objects.filter(user=user, pk=id)
    else:
        analysis_set = HairAnalysis.objects.filter(user=user)

    serializer = HairAnalysisSerializer(analysis_set, many=True)

    return Response(
        {
            "Data": serializer.data
        },
        status=200
    )


