from django.conf.urls import url

from account.views import UserProfileView

urlpatterns = [
    url(r'^profile$',UserProfileView.as_view()),

]