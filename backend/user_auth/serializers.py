from rest_framework import serializers

from user_auth.models import User, Video


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'profileUsername']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['videoId', 'channelId', 'channelTitle', 'description', 'thumbnail', 'title', 'user']
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
