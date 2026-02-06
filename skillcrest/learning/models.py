from django.db import models
from courses.models import Course


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

    # 🔥 Convert normal YouTube link → embed link
    def get_embed_url(self):
        url = self.youtube_url

        if "watch?v=" in url:
            return url.replace("watch?v=", "embed/")
        elif "youtu.be/" in url:
            return url.replace("youtu.be/", "www.youtube.com/embed/")
        return url
