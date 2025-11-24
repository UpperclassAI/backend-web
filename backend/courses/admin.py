from django.contrib import admin
from .models import Course, Module, Lesson, AlignmentStandard

# --- Inlines for Nested Editing ---

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1 # Number of empty forms to display
    ordering = ['order']

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    ordering = ['order']
    show_change_link = True # Allow jumping to the module edit page

# --- Admin Views ---

@admin.register(AlignmentStandard)
class AlignmentStandardAdmin(admin.ModelAdmin):
    list_display = ('level', 'subject_area', 'description')
    list_filter = ('level',)
    search_fields = ('subject_area', 'level')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'alignments')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title
    inlines = [ModuleInline] # Edit modules directly inside the course page

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline] # Edit lessons directly inside the module page

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'order', 'duration_minutes', 'is_preview')
    list_filter = ('lesson_type', 'is_preview', 'module__course')
    search_fields = ('title', 'content_text')