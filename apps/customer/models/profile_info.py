from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime


# ----------------------------
# ProfileInfo Manager
# ----------------------------
class ProfileInfoManager(models.Manager):

    def create_profile(self, user, **kwargs):
        profile = self.model(user=user, **kwargs)
        profile.save(using=self._db)
        return profile

    def get_public_profiles(self):
        return self.filter(is_profile_public=True, is_profile_archived=False)

    def get_featured_profiles(self):
        return self.filter(is_profile_featured=True, is_profile_archived=False)

    def get_archived_profiles(self):
        return self.filter(is_profile_archived=True)

    def get_suspended_profiles(self):
        return self.filter(is_profile_suspended=True)

    def update_profile(self, profile_id, **kwargs):
        profile = self.get(pk=profile_id)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        profile.save(using=self._db)
        return profile

    def delete_profile(self, profile_id):
        profile = self.get(pk=profile_id)
        profile.is_profile_archived = True
        profile.save(using=self._db)
        return profile

    def get_profile_by_user(self, user):
        return self.get(user=user)

    def get_profiles_by_type(self, profile_type):
        return self.filter(profile_type=profile_type, is_profile_archived=False)

    def search_profiles(self, search_term):
        return self.filter(
            models.Q(profile_name__icontains=search_term) |
            models.Q(profile_bio__icontains=search_term),
            is_profile_archived=False
        )

    def get_recent_profiles(self, days=30):
        date_threshold = timezone.now() - timezone.timedelta(days=days)
        return self.filter(profile_creation_time__gte=date_threshold,
                           is_profile_archived=False)

    def set_profile_status(self, profile_id, **kwargs):
        profile = self.get(pk=profile_id)
        allowed = [
            "is_profile_archived",
            "is_profile_public",
            "is_profile_featured",
            "is_profile_suspended",
        ]
        for key, value in kwargs.items():
            if key in allowed:
                setattr(profile, key, value)
        profile.save(using=self._db)
        return profile


# ----------------------------
# ProfileInfo Model
# ----------------------------
class ProfileInfo(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        primary_key=True
    )

    # ----------- Profile Identity -----------
    profile_name = models.CharField(
        max_length=70,
        blank=True,
        null=True,
        default="Anonymous"
    )
    

    def get_profile_name(self):
        return self.profile_name

    def set_profile_name(self, name):
        self.profile_name = name
        self.is_profile_name_exist = True
        self.save()

    def get_full_name(self):
        return self.profile_name if self.is_profile_name_visible else self.user.email_or_phone

    # ----------- Profile Slug -----------
    profile_name_slug = models.SlugField(unique=True, blank=True, null=True)

    # ----------- Bio -----------
    profile_address = models.TextField(max_length=101, blank=True, null=True)
    
    def set_profile_bio(self, value):
        self.profile_bio = value
        self.is_profile_bio_exist = True
        self.save()

    # ----------- Cover Photo -----------
    profile_cover_photo = models.ImageField(
        upload_to="cover-pics/",
        blank=True,
        null=True
    )
    def get_profile_cover_photo_url(self):
        if self.profile_cover_photo:
            return self.profile_cover_photo.url
        return "/static/defaults/default-cover-picture.png"

    def set_profile_cover_photo(self, value):
        self.profile_cover_photo = value
        
        self.save()

    # ----------- Profile Photo -----------
    profile_photo = models.ImageField(
        upload_to="profile-pics/",
        blank=True,
        null=True
    )
    def get_profile_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/defaults/default-profile-picture.png"

    def set_profile_photo(self, value):
        self.profile_photo = value
        
        self.save()

    # ----------- Gender -----------
    profile_gender = models.CharField(
        max_length=20,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other"),
        ],
        blank=True,
        null=True
    )
    
    def set_profile_gender(self, gender):
        self.profile_gender = gender
        
        self.save()

    # ----------- Date of Birth -----------
    profile_dob = models.DateField(blank=True, null=True)
    
    def set_profile_dob(self, dob):
        self.profile_dob = dob
        
        self.save()

    def get_age(self):
        if not (self.profile_dob):
            return None
        today = datetime.today()
        return (
            today.year
            - self.profile_dob.year
            - ((today.month, today.day) < (self.profile_dob.month, self.profile_dob.day))
        )

    # ----------- Language -----------
    profile_language = models.CharField(max_length=50, blank=True, null=True)
    
    def set_profile_language(self, value):
        self.profile_language = value
        
        self.save()

    # ----------- Timestamps -----------
    profile_creation_time = models.DateTimeField(auto_now_add=True)
    profile_updated_time = models.DateTimeField(auto_now=True)

    # ----------- Status Flags -----------
    is_profile_archived = models.BooleanField(default=False)
    is_profile_public = models.BooleanField(default=True)
    is_profile_verified = models.BooleanField(default=False)
    is_profile_featured = models.BooleanField(default=False)
    is_profile_suspended = models.BooleanField(default=False)

    # ----------- Followers / Following -----------
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="profile_followers",
        blank=True
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="profile_following",
        blank=True
    )

    # ----------- Soft Delete Override -----------
    def delete(self, *args, **kwargs):
        self.is_profile_archived = True
        self.save()

    # ----------- Profile Completion Checker -----------
    def is_profile_complete(self):
        required = [
            self.profile_name,
            self.profile_photo,
            self.profile_bio,
        ]
        return all(required)

    # ----------- String Representation -----------
    def __str__(self):
        return self.user.email_or_phone

    # ----------- Meta -----------
    class Meta:
        verbose_name = "Profile Info"
        verbose_name_plural = "Profile Infos"
        ordering = ["-profile_creation_time"]

    objects = ProfileInfoManager()

    # Bio
    def get_profile_bio(self):
        return self.profile_address

    # Gender
    def get_profile_gender(self):
        return self.profile_gender

    # DOB
    def get_profile_dob(self):
        return self.profile_dob

    # Language
    def get_profile_language(self):
        return self.profile_language

    # Account Category (Profile Type)
    def get_profile_type(self):
        return self.user.role     # because profile type = user role

        
