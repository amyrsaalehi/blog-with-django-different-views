from django.urls import path, include
from .views import post_list, post_detail, PostListAPIView, PostDetailAPIView, PostListGenericAPIVIew, PostDetailGenericAPIVIew, PostViewSetAPIView, PostGenericViewSetAPIView, PostModelViewSetAPIView, AuthorModelViewSetAPIView


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', PostViewSetAPIView, basename='post')

generic_router = DefaultRouter()
generic_router.register('post', PostGenericViewSetAPIView, basename='post')

model_router = DefaultRouter()
model_router.register('post', PostModelViewSetAPIView, basename='post')

model_router2 = DefaultRouter()
model_router2.register('author', AuthorModelViewSetAPIView, basename='author')

urlpatterns = [
    path('function-base/post/', post_list),
    path('function-base/post/<int:pk>/', post_detail),

    path('class-base/post/', PostListAPIView.as_view()),
    path('class-base/post/<int:pk>/', PostDetailAPIView.as_view()),

    path('generic/post/', PostListGenericAPIVIew.as_view()),
    path('generic/post/<int:pk>/', PostDetailGenericAPIVIew.as_view()),

    path('viewsets/', include(router.urls)),

    path('generic-viewsets/', include(generic_router.urls)),

    path('model-viewsets/', include(model_router.urls)),

    path('model-viewsets/', include(model_router2.urls)),
]
