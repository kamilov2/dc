from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import AsyncExample, Example

urlpatterns = [
    path('async_example/', AsyncExample.as_view(), name='async_example'),
    path('example/' , Example.as_view(), name="example"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
