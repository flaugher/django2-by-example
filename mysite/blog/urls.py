from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # Post views
    #path('', views.post_list, name='post_list'),
    # example: blog/
    path('', views.PostListView.as_view(), name='post_list'),
    # blog/2019/11/28/a-blog-post/
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # blog/25/share/
    path('<int:post_id/share/', views.post_share, name='post_share'),
]