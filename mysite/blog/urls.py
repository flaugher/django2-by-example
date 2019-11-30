from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    # Post views
    # The next two paths both call the post_list view but are named differently
    # because they have different url patterns.
    # example: blog/
    path('', views.post_list, name='post_list'),
    #path('', views.PostListView.as_view(), name='post_list'),
    # blog/tag/great-musicians/
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # blog/2019/11/28/a-blog-post/
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # blog/25/share/
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]