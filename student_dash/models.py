# models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from classroom.models import CustomUser, Lecture as Course



class Playlist(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(blank=True, null=True, help_text="Paste unlisted YouTube video URL")
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='lecture', null=True, blank=True)

    def __str__(self):
        return self.title

class LectureNote(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='lecture_notes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.lecture.title}"


class LectureAccess(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accessible_lectures')
    lecture = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allowed_students')
    access_granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.lecture.title}"

