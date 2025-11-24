from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.mail import send_mail

# --- 1. School Model ---
class School(models.Model):
    """
    Represents a school or organization associated with users.
    """
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Schools"

    def __str__(self):
        return self.name

# --- 2. Custom User Manager ---
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN) # Assign ADMIN role

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# --- 3. Custom User Model ---
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model supporting different roles (Student, Teacher, Admin)
    and using email as the primary authentication field.
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        TEACHER = 'TEACHER', 'Teacher/Instructor'
        STUDENT = 'STUDENT', 'Student'
    
    # Core fields for authentication
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    # Custom fields for EdTech platform
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text='Designates the user role on the platform.'
    )
    school = models.ForeignKey(
        School, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    
    # Fields required for Django Auth System
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
                'Unselect this instead of deleting accounts.'
    )
    date_joined = models.DateTimeField(default=timezone.now)

    # Use the custom manager
    objects = CustomUserManager()

    # Specify the field used for authentication
    USERNAME_FIELD = 'email'
    
    # Fields that must be entered when creating a user via createsuperuser
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role'] 

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Registered users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN