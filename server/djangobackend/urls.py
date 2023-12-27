"""djangobackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(route='', view=views.get_dealerships, name='index'),
    path('dealer/<int:id>/', views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:id>/review', views.add_review, name='add_review'),
    path(route='about/', view=views.about, name='about'),
    path(route='contact/', view=views.contact, name='contact'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)