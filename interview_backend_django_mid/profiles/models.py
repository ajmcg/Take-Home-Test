from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserProfileManager(BaseUserManager):
    """
    Custom manager for UserProfile model that uses email for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the username for authentication.
    """
    email = models.EmailField(unique=True, help_text='Email address for the user')
    username = models.CharField(max_length=255, unique=True, help_text='Unique username for the user')
    first_name = models.CharField(max_length=255, blank=True, null=True, help_text='First name of the user')
    last_name = models.CharField(max_length=255, blank=True, null=True, help_text='Last name of the user')
    date_joined = models.DateTimeField(default=timezone.now, help_text='Date when the user joined')
    last_login = models.DateTimeField(null=True, blank=True, help_text='Last login time of the user')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active')
    is_admin = models.BooleanField(default=False, help_text='Designates whether the user is an admin')
    # pillow was used for the avatar field. Official requirement from django docs is to use pillow.
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, help_text='Thumbnail image of the user')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        """
        Return the full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def get_username(self):
        """
        Return the username (email) of the user.
        """
        return self.email

    def is_authenticated(self):
        """
        Return whether the user is authenticated.
        """
        return True

    def __str__(self):
        """
        Return string representation of the user, which is the email.
        """
        return self.email
