from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Author
from .serializers import PostSerializer, AuthorSerializer, PostSerializerWithAuthor, AuthorSerializerWithPosts

from rest_framework import views
from rest_framework import generics, mixins
from rest_framework import viewsets

from django.shortcuts import get_object_or_404


# <><><><><> FUNCTION-BASE VIEWS <><><><><>

@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        try:
            posts = Post.objects.all()
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# <><><><><> CLASS-BASE VIEWS <><><><><>


class PostListAPIView(views.APIView):
    authentication_classes = ([TokenAuthentication, SessionAuthentication, BasicAuthentication])
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        try:
            posts = Post.objects.all()
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(views.APIView):
    authentication_classes = ([TokenAuthentication, SessionAuthentication, BasicAuthentication])
    permission_classes = ([IsAuthenticated])

    def get_object(self, pk=None):
        try:
            return Post.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# <><><><><> GENERIC-CLASS-BASE VIEWS <><><><><>


class PostListGenericAPIVIew(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = ([TokenAuthentication, SessionAuthentication, BasicAuthentication])
    permission_classes = ([IsAuthenticated])
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class PostDetailGenericAPIVIew(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                               mixins.RetrieveModelMixin, ):
    authentication_classes = ([TokenAuthentication, SessionAuthentication, BasicAuthentication])
    permission_classes = ([IsAuthenticated])
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, pk=None):
        return self.retrieve(request, pk)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)


# <><><><><> CLASS-BASE VIEWSETS <><><><><>


class PostViewSetAPIView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            posts = Post.objects.all()
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# <><><><><> CLASS-BASE GENERIC VIEWSETS <><><><><>


class PostGenericViewSetAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# <><><><><> CLASS-BASE MODEL VIEWSETS <><><><><>


class PostModelViewSetAPIView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializerWithAuthor
    queryset = Post.objects.all()


class AuthorModelViewSetAPIView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorSerializerWithPosts
    queryset = Author.objects.all()








