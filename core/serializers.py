from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from core.models import User, Profile, Post, SocialMediaLink


class SocialMediaLinkSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('platform', 'url')

    def update(self, instance, validated_data):
        print('*****************************************************')
        print(instance)


class ProfileSerializer(DocumentSerializer):
    social_media_links = SocialMediaLinkSerializer(many=True)

    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(DocumentSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(DocumentSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'password', 'profile')

    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        # TODO validate profile data before creating profile
        user.create_profile(**profile_data)
        return user

    def update(self, instance, validated_data):
        # profile_data = validated_data.pop('profile')
        # instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
        # instance.update_profile(**profile_data)
        # instance.save()
        return validated_data
