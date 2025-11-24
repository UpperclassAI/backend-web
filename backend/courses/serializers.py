from rest_framework import serializers
from .models import Course, Module, Lesson, AlignmentStandard
from users.serializers import UserSerializer # Reuse your user serializer for author info

class AlignmentStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlignmentStandard
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'order', 'lesson_type', 
            'video_url', 'content_text', 'duration_minutes', 'is_preview'
        ]

class ModuleSerializer(serializers.ModelSerializer):
    # Nest lessons inside the module response
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lessons']

class CourseListSerializer(serializers.ModelSerializer):
    """
    Lighter serializer for listing courses (excludes heavy module/lesson data).
    """
    author = UserSerializer(read_only=True)
    alignments = AlignmentStandardSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'thumbnail', 'description', 
            'price', 'author', 'alignments', 'is_published'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer that includes the full curriculum tree.
    """
    author = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    alignments = AlignmentStandardSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail', 
            'price', 'is_published', 'created_at', 
            'author', 'alignments', 'modules'
        ]