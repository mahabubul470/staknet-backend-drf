from rest_framework_mongoengine import serializers
from core.models import User, Profile, Post, SocialMediaLink



class SocialMediaLinkSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('platform', 'url')


class ProfileSerializer(serializers.DocumentSerializer):
    social_media_links = SocialMediaLinkSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile')

    # Ensure the password field is write-only and hashed before saving
    extra_kwargs = {
        'password': {'write_only': True},
    }
