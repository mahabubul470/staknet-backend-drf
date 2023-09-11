from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
from core.models import User, AuthSession, Post, Connection
from core.serializers import UserSerializer, PostSerializer, ConnectionSerializer, PostCommentSerializer
from core.auth import AuthPermission, TokenAuthentication


class UserApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.password = make_password(request.data.get('password'))
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user and check_password(password, user.password):
            token = user.generate_jwt_token()
            AuthSession().create_session(token=token, user=user.id)
            response_data = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "token": token
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileApiView(APIView):
    permission_classes = [AuthPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        user = User.objects.get(username=request.user.username)
        if serializer.is_valid():
            serializer.update(instance=user,
                              validated_data=serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(APIView):
    permission_classes = [AuthPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostCommentSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostLikeView(APIView):
    permission_classes = [AuthPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostCommentSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user not in post.likes:
            post.add_like(user)
            return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "Post already liked by the user."}, status=status.HTTP_400_BAD_REQUEST)


class PostCommentView(APIView):
    permission_classes = [AuthPermission]
    authentication_classes = [TokenAuthentication]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment_text = request.data.get("comment_text")

        if comment_text:
            user = request.user
            post.add_comment(user, comment_text)
            return Response({"detail": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)


class ConnectionView(APIView):
    permission_classes = [AuthPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        connections = Connection.objects.filter(user=user)
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = ConnectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        try:
            connection = Connection.objects.get(user=user)
            connection.delete()
            return Response({"detail": "Connection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Connection.DoesNotExist:
            return Response({"detail": "Connection not found."}, status=status.HTTP_404_NOT_FOUND)
