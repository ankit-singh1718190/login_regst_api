
from django.urls import path
from .views import userRegistration,userLoginView,UserProfileView,UserchangePassword,SendPasswordResetEmialview


urlpatterns = [
    path('register/', userRegistration.as_view(),name='register'),
    path('log/', userLoginView.as_view(),name='log'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('changePassword/', UserchangePassword.as_view(),name='changePassword'),
    path('sendemailPassword/', SendPasswordResetEmialview.as_view(),name='sendemailPassword'),

]