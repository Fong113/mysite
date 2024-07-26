from django.urls import path
from . import views
from django.views.i18n import set_language

urlpatterns = [
    path('', views.index, name='index'),
    path('i18n/', set_language, name='set_language'),
]
