from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    # URL to a page containing a test image:
    # http://127.0.0.1:8000/images/create/?title=%20Django%20and%20Duke&url=https://upload.wikimedia.org/wikipedia/commons/8/85/Django_Reinhardt_and_Duke_Ellington_%28Gottlieb%29.jpg
    # http://127.0.0.1:8000/images/create/?title=TITLE&url=URLOFIMAGE
    # 'url' must be the link to the image itself, not the page the image appears on!
    path('create/', views.image_create, name='create'),
    # images/detail/6/django-and-duke/
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    # images/like/
    path('like/', views.image_like, name='like'),
    path('', views.image_list, name='list'),
]