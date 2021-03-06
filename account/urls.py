from django.conf.urls import url

from account.views import RegisterUserProfileView, LoginView, LogoutView, UserProfileView

urlpatterns = [
    url(r'^register$', RegisterUserProfileView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^profile$', UserProfileView.as_view(), name='profile')
]
