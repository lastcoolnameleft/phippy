""" URL router """
from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
#    path('toy/', views.toy_list, name='toy_list'),
#    path('faq/', views.faq, name='faq'),
#    path('mark/', views.mark, name='mark'),
#    # ex: /view/toy/5/
#    path('view/toy/<int:toy_id>', views.detail, name='toy_list'),
#    path('toy/<int:toy_id>', views.detail, name='detail'),
#    # ex: /view/location/500/
#    path('view/location/<int:toy_location_id>', views.location, name='location'),
#    path('location/<int:toy_location_id>', views.location, name='location'),
#    # Auth
#    path('profile', views.profile, name='profile'),
#    path('login', views.login, name='login'),
#    path('logout', views.logout, name='logout'),
#    path('oauth/', include('social_django.urls', namespace='social'), name='logthru'),
]
