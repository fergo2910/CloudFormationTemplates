from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home', views.HomePageView.as_view()),
    url(r'^elements', views.elements),
]
