from django.conf.urls import url

from account.views import RegisterUserProfileView

urlpatterns = [
    url(r'^register$',RegisterUserProfileView.as_view()),

]