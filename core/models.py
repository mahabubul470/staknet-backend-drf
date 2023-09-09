import jwt
from datetime import datetime, timedelta
from mongoengine import Document, EmbeddedDocument, fields, CASCADE, ReferenceField
from bson import ObjectId
from staknet.settings import SECRET_KEY


class SocialMediaLink(EmbeddedDocument):
    platform = fields.StringField(required=True)
    url = fields.URLField(required=True)


class Profile(Document):
    user = ReferenceField('User')
    profile_picture = fields.URLField()
    bio = fields.StringField()
    social_media_links = fields.EmbeddedDocumentListField(SocialMediaLink)

    def create_post(self, text, images):
        post = Post(user=self.user, text=text, images=images)
        post.save()
        return post

    def like_post(self, post_id):
        post = Post.objects(id=post_id).first()
        if post and self.user not in post.likes:
            post.likes.append(self.user)
            post.save()
            return post
        return None

    def comment_on_post(self, post_id, text):
        post = Post.objects(id=post_id).first()
        if post:
            comment = {'user': self.user, 'text': text}
            post.comments.append(comment)
            post.save()
            return comment


class Post(Document):
    user = ReferenceField('User')
    text = fields.StringField(required=True)
    images = fields.ListField(fields.URLField())
    likes = fields.ListField(ReferenceField('User'))
    comments = fields.ListField(fields.DictField())

    def add_like(self, user):
        if user not in self.likes:
            self.likes.append(user)
            self.save()

    def add_comment(self, user, text):
        comment = {'user': user, 'text': text}
        self.comments.append(comment)
        self.save()

    @classmethod
    def search_posts_by_keyword(cls, keyword):
        return cls.objects(text__icontains=keyword)


class User(Document):
    username = fields.StringField(max_length=100, unique=True, required=True)
    email = fields.EmailField(unique=True, required=True)
    password = fields.StringField(required=True)  # Store hashed password
    profile = fields.ReferenceField(Profile)

    def create_profile(self, profile_picture, bio, social_media_links):
        profile = Profile(user=self, profile_picture=profile_picture,
                          bio=bio, social_media_links=social_media_links)
        profile.save()
        self.profile = profile  # Link the profile to the user
        self.save()
        return profile

    def update_profile(self, profile_picture, bio, social_media_links):
        if self.profile:
            self.profile.profile_picture = profile_picture
            self.profile.bio = bio
            self.profile.social_media_links = social_media_links
            self.profile.save()
            return self.profile
        return None

    def view_other_user_profile(self, other_user_id):
        try:
            other_user = User.objects(id=ObjectId(other_user_id)).first()
            if other_user:
                return other_user.profile
        except User.DoesNotExist:
            return None

    def generate_jwt_token(self):
        payload = {
            'user_id': str(self.id),
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode_jwt_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            return User.objects(id=ObjectId(user_id)).first()
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.DecodeError:
            return None  # Token is invalid


class Connection(Document):
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    connected_user = ReferenceField(User, reverse_delete_rule=CASCADE)
