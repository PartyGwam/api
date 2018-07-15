from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.comments.models import Comment
from apps.parties.models import Party


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileUsernamePictureSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['party', 'is_active']


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']

    def validate(self, attrs):
        slug = self.context['request'].path_info.split('/')[3]
        party = Party.objects.get(slug=slug)
        author = self.context['request'].user.profile

        if author not in party.participants.all():
            raise PermissionDenied('파티 참여자만 댓글을 달 수 있습니다.')
        else:
            attrs['party'] = party
            return attrs

    def create(self, validated_data):
        party = validated_data.pop('party')
        author = self.context['request'].user.profile

        return Comment.objects.create_comment(
            party=party,
            author=author,
            **validated_data
        )

    def update(self, instance, validated_data):
        return Comment.objects.update_comment(instance, validated_data['text'])
