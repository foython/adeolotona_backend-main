from django.contrib import admin
from django.urls import path, include


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),


    # accounts
    path('api/auth/', include('accounts.urls')),
    path('api/subscription_app/', include('subscription_app.urls')),
    path('api/analysis/', include('hair_analysis_and_tips.urls')),
    path('api/referral/', include('referral.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
