from django.db import models
from django.conf import settings

# --- 1. Alignment Standard Model (FGN Curriculum) ---
class AlignmentStandard(models.Model):
    """
    Represents the Federal Government of Nigeria (FGN) revised subject structure standards.
    Example: Level='JSS 1', Subject='Digital Literacy', Code='DL-JSS1-01'
    """
    level = models.CharField(max_length=50, help_text="e.g., Primary 1, JSS 3, SSS 1")
    subject_area = models.CharField(max_length=100, help_text="e.g., Digital Literacy, AI & Robotics")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.level}: {self.subject_area}"

# --- 2. Course Model ---
class Course(models.Model):
    """
    The top-level container for a subject or masterclass.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    
    # Curriculum Alignment
    alignments = models.ManyToManyField(AlignmentStandard, blank=True, related_name='courses')
    
    # Instructor/Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='authored_courses',
        limit_choices_to={'role': 'TEACHER'} # Only teachers/admins can author courses
    )
    
    # Course Properties
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# --- 3. Module Model ---
class Module(models.Model):
    """
    A section or chapter within a course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(help_text="The sequence order of this module within the course")

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order'] # Ensures no two modules have the same order number in a course

    def __str__(self):
        return f"{self.course.title} - {self.title}"

# --- 4. Lesson Model ---
class Lesson(models.Model):
    """
    The actual content unit (Video, Text, or Project).
    """
    LESSON_TYPES = (
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('project', 'Project/Assignment'),
        ('quiz', 'Quiz'),
    )

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    
    # Content Fields
    video_url = models.URLField(blank=True, null=True, help_text="URL for video content (e.g., Vimeo, YouTube, S3)")
    content_text = models.TextField(blank=True, help_text="Markdown text for text-based lessons")
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Estimated time to complete")
    is_preview = models.BooleanField(default=False, help_text="If True, can be viewed without enrollment")

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"