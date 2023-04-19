from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PostListView, PostDetailApiView, PostUpdateApiView, PostDeleteAPIView, PostCreateAPIView, \
    LikeAPIView

urlpatterns = [
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path("posts", PostListView.as_view(), name='posts_list_api_view'),
    path('posts/<int:pk>', PostDetailApiView.as_view(), name='post_detail_api_view'),
    path('posts/update/<int:pk>', PostUpdateApiView.as_view(), name='post_update_api_view'),
    path('posts/delete/<int:pk>', PostDeleteAPIView.as_view(), name='post_delete_api_view'),
    path('posts/create', PostCreateAPIView.as_view(), name='post_create_api_view'),
    path('posts/<int:pk>/like', LikeAPIView.as_view(), name='post_like_api_view')
]
