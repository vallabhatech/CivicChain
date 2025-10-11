from django.urls import path
from . import views as mainViews
urlpatterns = [ 
    path('',mainViews.index, name='index'),
    path('contact',mainViews.contact, name='contact')
]