from rest_framework import viewsets, permissions
from .models import Course, Module, Lesson
from .serializers import CourseListSerializer, CourseDetailSerializer, ModuleSerializer, LessonSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows courses to be viewed.
    Create/Update/Delete is restricted to Admin interface for now.
    """
    queryset = Course.objects.filter(is_published=True)
    lookup_field = 'slug' # Use slug for nicer URLs (e.g., /courses/ai-masterclass/)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    def get_permissions(self):
        # Allow any user (even guests) to view course list/details
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

# Optional: ViewSets for Modules/Lessons if you need to fetch them individually
class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]