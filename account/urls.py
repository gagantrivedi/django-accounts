from django.conf.urls import url

from account.views import RegisterUserProfileView, LoginView

urlpatterns = [
    url(r'^register$', RegisterUserProfileView.as_view()),
    url(r'^login$', LoginView.as_view())

]
