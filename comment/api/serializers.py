from comment.models import Comment
from rest_framework import serializers


class CommentCreateSerializer(serializers.ModelSerializer):
	object_id = serializers.IntegerField()
	class Meta:
		model = Comment
		fields = ['object_id', 'full_name', 'rate', 'body']


class CommentSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Comment
		exclude = ['object_id', 'content_type']
		read_only_fields = [
			'user',
			'content_type',
			'object_id',
			'create',
			'update',
			'rate'
			]
