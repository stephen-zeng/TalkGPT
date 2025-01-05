from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('audio/<str:filename>/', views.audioFile, name='audioFile'),   
]
