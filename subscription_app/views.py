from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# models import
from accounts.models import UserProfile

from django.conf import settings
from django.http import JsonResponse

import stripe
stripe.api_key = "sk_test_51ReHLiH6fkQlm6OO9pBJsy4A9TH9aHZqNjm6dXdz3Rka4tw4VI5p4AuS0rOMUit8XJNPP9DKPiYalfXneCfVg8F300P8KRrKOi"



prices = {
    'monthly': 'price_1Rea3gH6fkQlm6OOM9jVmv5l',
    'yearly': 'price_1ReyseH6fkQlm6OO9fqreTdq'
}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_subscription_on_app(request):
    import traceback

    user = request.user
    user_profile = UserProfile.objects.get(user=user)    
    subscription_plan = request.data.get('subscription_plan')

    if subscription_plan not in prices:
        return JsonResponse({'error': 'Invalid subscription plan'}, status=400)

    if user_profile.is_subscribed:
        return Response({"Message": "You are already subscribed! Please cancel your existing subscription If you wish to update it."}, status=status.HTTP_200_OK)
    
    if user_profile.subscription_status == "cancelled":
        return Response({"Message": "You already cancelled your subscription! Please wait until your current billing period ends."}, status=status.HTTP_200_OK)

    try:
        price_id = prices[subscription_plan]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://192.168.10.35:8000/api/subscription_app/success/',
            cancel_url='http://192.168.10.35:8000/api/subscription_app/cancel/',
            metadata={'user_id': str(user.pk), 'package': subscription_plan},
        )

        print("Checkout session:", checkout_session)

        return JsonResponse({'checkout_url': checkout_session.url})

    except Exception as e:
        print("Exception during Stripe session creation:", str(e))
        traceback.print_exc()
        return JsonResponse({'error': 'Stripe session creation failed', 'details': str(e)}, status=500)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def buy_subscription_on_app(request):
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)    
#     subscription_plan = request.data.get('subscription_plan')
    

#     if user_profile.is_subscribed:
#         return Response({"Message": "You are already subscribed! Please cancel your existing subscription If you wish to update it."}, status=status.HTTP_200_OK)
#     if user_profile.subscription_status == "cancelled":
#         return Response({"Message": "You already cancelled your subscription! Please wait untill your current billing period ends."}, status=status.HTTP_200_OK)

#     try:
#         # Predefined price ID (from settings or database)
#         price_id = prices[subscription_plan]  # This should be stored in the backend

#         # Create a checkout session
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price': price_id, 
#                 'quantity': 1,
#             }],
#             mode='subscription',  # This is for recurring subscriptions
#             success_url='http://192.168.10.210:2020/api/subscription_app/success/',  # Change to your success URL
#             cancel_url='http://192.168.10.210:2020/api/subscription_app/cancel/',  # Change to your cancel URL
#             metadata={'user_id': str(user.pk), "package": subscription_plan},
#         )

#         return JsonResponse({
#             'checkout_url': checkout_session.url
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def success(request):
    return Response({"Message": "Success"}, status=status.HTTP_200_OK)



@api_view(['GET'])
def cancel(request):
    return Response({"Message": "Cancel"}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    subscription_id = user_profile.subscription_id
    try:
        canceled_subscription = stripe.Subscription.delete(subscription_id)
        user_profile.subscription_status = "cancelled"
        user_profile.save()
        return Response({"Message": "Subscription Cancelled Successfully."}, status=status.HTTP_200_OK)
    except:
        return Response({"Message": "Subscription Already Cancelled."}, status=status.HTTP_200_OK)