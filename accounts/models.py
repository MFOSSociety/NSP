import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


# Custom User definition, making email as the default login
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='',

    )
    USERNAME_FIELD = 'email'    # Using email in the USERNAME_FIELD during login
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    skill_name = models.CharField(max_length=20, default="", blank=True)

    def __str__(self):
        return self.skill_name


class ProjectDetail(models.Model):
    project_name = models.CharField(max_length=50, default="", blank=False)
    initiated_by = models.CharField(max_length=50, default="", blank=True)
    mentor_name = models.CharField(max_length=50, default="", blank=False)
    branch = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=2500, blank=False)
    paid = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.project_name + " under " + self.mentor_name


class ProjectPeopleInterested(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE,)
    project = models.ForeignKey(ProjectDetail, related_name="project", on_delete=models.CASCADE)

    def __str__(self):
        return "{} is interested in {}".format(self.user, self.project)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    ratings = models.IntegerField(null=True, default=0, blank=True)
    photo = models.ImageField(upload_to="profile_image", null=True, blank=True)
    year = models.IntegerField(null=True, default=1, blank=True)
    branch = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    stream = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    gender = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    position = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)   # Student or Teacher
    bio = models.CharField(max_length=500, default="", blank=True)
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    class Meta:
        db_table = 'accounts_userprofile'

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return "{} started following {}".format(self.follower, self.following)


class Submissions(models.Model):
    user = models.ForeignKey(User, related_name="user_solution", on_delete=models.CASCADE)
    solution_link = models.CharField(max_length=100, default="", blank=True, null=True)

    def __str__(self):
        return self.solution_link
