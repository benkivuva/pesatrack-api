from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """
    Custom manager for the User model. This manager provides methods for creating and managing users.
    """
    def create_user(self, username, email, password=None):
        """
        Create and save a new regular user with the given username, email, and password.

        Args:
            username (str): The username for the new user.
            email (str): The email for the new user.
            password (str): The user's password (optional).

        Returns:
            User: The newly created user object.
        """
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        """
        Create and save a new superuser with the given username, email, and password.

        Args:
            username (str): The username for the new superuser.
            email (str): The email for the new superuser.
            password (str): The superuser's password (optional).

        Returns:
            User: The newly created superuser object.
        """
        if password is None:
            raise TypeError('Password should not be None')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that extends AbstractBaseUser and includes additional fields.
    """
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def tokens(self):
        """
        Get user tokens.

        Returns:
            str: User tokens.
        """
        return ''  # Customize as needed

    def __str__(self):
        """
        String representation of the User model.

        Returns:
            str: The email address of the user.
        """
        return self.email