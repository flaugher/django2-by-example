from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    # images/create/?title=TITLE&url=URLOFIMAGE
    # Example:
    # http://127.0.0.1:8000/images/create/?title=%20Django%20and%20Duke&url=https://upload.wikimedia.org/wikipedia/commons/8/85/Django_Reinhardt_and_Duke_Ellington_%28Gottlieb%29.jpg
    # 'url' must be the link to the image itself, not the page the image appears on!
    path('create/', views.image_create, name='create'),
]