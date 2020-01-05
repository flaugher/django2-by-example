from django.urls import path

from . import views


app_name = 'shop'
urlpatterns = [
    # shop/
    path('', views.product_list, name='product_list'),
    # shop/sporting-apparel
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # shop/10/sporting-apparel
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]