from django.db import models
from courses.models import Course
import re


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    # 🔥 SAFE YouTube Embed URL Generator
    def get_embed_url(self):
        url = self.youtube_url.strip()

        # Extract video ID from any YouTube format
        patterns = [
            r"youtu\.be/([^?&]+)",
            r"youtube\.com/watch\?v=([^?&]+)",
            r"youtube\.com/embed/([^?&]+)",
            r"youtube\.com/shorts/([^?&]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1"

        return ""
