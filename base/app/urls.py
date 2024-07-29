from django.urls import path,include
from . import views
from .views import top10hits, contact
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('download/<str:file_name>/', views.download_video, name='download_video'), 
    path('accounts/', include('allauth.urls')),  # Includes login, signup, etc.
    path('top10hits/', top10hits, name='top10hits'),
    path('contact/', contact, name='contact'),
   
]

