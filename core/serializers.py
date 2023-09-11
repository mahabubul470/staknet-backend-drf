from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from core.models import User, Profile, Post, SocialMediaLink, Connection


class SocialMediaLinkSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('platform', 'url')


class ProfileSerializer(DocumentSerializer):
    social_media_links = SocialMediaLinkSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(DocumentSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile')

    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        # TODO validate profile data before creating profile
        user.create_profile(**profile_data)
        return user

    def update(self, instance, validated_data):

        # TODO create separate serializer for updating profile,
        # make fileds required=False, and validate profile data before updating profile
        # return updated data

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.update_profile(**validated_data['profile'])
        instance.save()
        return instance


class ConnectionSerializer(DocumentSerializer):
    class Meta:
        model = Connection
        fields = '__all__'


class PostSerializer(DocumentSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    text = serializers.CharField()

class PostCommentSerializer(DocumentSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
