from rest_framework import serializers

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.comments.models import Comment
from apps.parties.models import Party


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileUsernamePictureSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['party', 'is_active']


class PartyCommentSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True, label='comments')

    class Meta:
        model = Party
        fields = ['title', 'place', 'description', 'comment_set']


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']

    def create(self, validated_data):
        party = self.context['view'].get_object()
        author = self.context['request'].user.profile

        return Comment.objects.create_comment(
            party=party,
            author=author,
            **validated_data
        )

    def update(self, instance, validated_data):
        return Comment.objects.update_comment(instance, validated_data['text'])
