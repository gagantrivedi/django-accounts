from django.conf.urls import url

from account.views import RegisterUserProfileView, LoginView, LogoutView

urlpatterns = [
    url(r'^register$', RegisterUserProfileView.as_view()),
    url(r'^login$', LoginView.as_view()),
    url(r'^logout$', LogoutView.as_view())

]
